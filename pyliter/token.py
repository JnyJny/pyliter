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
    def from_file(cls, input_file, classifier=None) -> tuple:
        """
        :param input_file: file-like object with a readline
        :param classifier: pyliter.token.TokenClassifier

        """
        try:
            classifier = classifier()
        except TypeError:
            classifier = TokenClassifier()

        tokens = []
        for t in tokenize.tokenize(input_file.readline):
            tokens.append(cls(*t._asdict().values(), t.exact_type))
            classifier.classify(tokens[-1])

        text = tokenize.untokenize(tokens).decode("utf-8")

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

    def classify(self, token) -> None:
        """
        :param ExtendedToken token:
        """

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

            if token.type == TOKEN.NAME:
                if token.line.strip().startswith("def"):
                    token.exactType = FNAME
                    break

                if token.line.strip().startswith("class"):
                    token.exact_type = CNAME
                    break

                if token.line.strip().startswith(("import", "from", "as")):
                    token.exact_type = INAME
                    break

                try:
                    eq = token.line.index(" = ")
                    tok = token.start[1]
                    if tok < eq and ":" not in token.line:
                        token.exact_type = LVAL
                        break
                except ValueError:
                    pass

            break

        # need to backtrack for LVAL classification
        if token.type != TOKEN.OP:
            token.category = self.categories[token.exact_type]
        else:
            token.category = self.categories[token.type]
