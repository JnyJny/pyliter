"""
"""

import click
import token as TOKEN
import builtins
import keyword

import tokenize
from dataclasses import dataclass, field
from pprint import pformat

_BUILTINS = dir(builtins)


KEYWORD = 1101
BUILTIN = 1102
DEFINITIONS = 1103
DOCSTRING = 1104
FNAME = 1105
CNAME = 1106
INAME = 1107
LVAL = 1108
HIDDEN = 1109
SELF = 1110


@dataclass
class ExtendedToken:
    type: int
    string: str
    start: tuple
    end: tuple
    line: str
    exact_type: int = 0
    category: str = field(default="", init=False, repr=True)
    attributes: dict = field(default_factory=dict, init=False, repr=False)

    @classmethod
    def from_file(
        cls, input_file, start_line: int, line_count: int, classifier=None
    ) -> tuple:

        try:
            classifier = classifier()
        except TypeError:
            classifier = TokenClassifier()

        tokens = []

        for t in tokenize.tokenize(input_file.readline):
            tokens.append(cls(*t._asdict().values(), t.exact_type))
            classifier(tokens[-1], tokens[:-1])

        text = tokenize.untokenize(tokens).decode("utf-8")

        if line_count == -1:
            end_line = line_count
        else:
            end_line = start_line + line_count

        text = "\n".join(text.splitlines()[start_line:end_line])

        # TokenInfo.start is a tuple of (line number, offset), line number
        # starts at one instead of zero so subtract one to avoid a one-off bug.
        tokens = [t for t in tokens if start_line <= (t.start[0] - 1) < end_line]

        return tokens, text

    def __len__(self):
        return 4

    def __iter__(self):
        return iter([self.type, self.string, self.start, self.end, self.line])

    def __str__(self):
        return f"{self!r}\nA:\n{pformat(self.attributes)}"


class TokenClassifier:
    @property
    def builtins(self):
        try:
            return self._builtins
        except AttributeError:
            pass
        self._builtins = dir(builtins)
        return self._builtins

    @property
    def categories(self):
        try:
            return self._categories
        except AttributeError:
            pass

        self._categories = {}
        self._categories.update(tokenize.tok_name)
        self._categories[KEYWORD] = "KEYWORD"
        self._categories[BUILTIN] = "BUILTIN"
        self._categories[DEFINITIONS] = "DEFINITIONS"
        self._categories[DOCSTRING] = "DOCSTRING"
        self._categories[FNAME] = "FNAME"
        self._categories[CNAME] = "CNAME"
        self._categories[INAME] = "INAME"
        self._categories[LVAL] = "LVAL"
        self._categories[HIDDEN] = "HIDDEN"
        self._categories[SELF] = "SELF"

        return self._categories

    def __call__(self, token, prev_tokens):
        self.classify(token, prev_tokens)

    def classify(self, token, prev_tokens):

        while True:
            if keyword.iskeyword(token.string):
                token.exact_type = KEYWORD
                break

            if token.string in self.builtins:
                token.exact_type = BUILTIN
                break

            if token.string.startswith(('"""', "'''")):
                token.exact_type = DOCSTRING
                break

            if token.string.startswith("_"):
                token.exact_type = HIDDEN
                break

            if token.string == "self":
                token.exact_type = SELF
                break

            try:
                if prev_tokens[-1].string == "def":
                    token.exact_type = FNAME
                    break

                if prev_tokens[-1].string == "class":
                    token.exact_type = CNAME
                    break

                if prev_tokens[-1].string == "import":
                    token.exact_type = INAME
                    break
            except IndexError:
                pass
            break

        # need to backtrack for LVAL classification
        if token.type != TOKEN.OP:
            token.category = self.categories[token.exact_type]
        else:
            token.category = self.categories[token.type]
