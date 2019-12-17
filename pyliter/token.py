"""
"""

import click
import token as TOKEN
import builtins
import keyword

from tokenize import tokenize as original_tokenize
from tokenize import untokenize as original_untokenize
from tokenize import EXACT_TOKEN_TYPES, tok_name

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

tok_name[KEYWORD] = "KEYWORD"
tok_name[BUILTIN] = "BUILTIN"
tok_name[DEFINITIONS] = "DEFINITIONS"
tok_name[DOCSTRING] = "DOCSTRING"
tok_name[FNAME] = "FNAME"
tok_name[CNAME] = "CNAME"
tok_name[INAME] = "INAME"
tok_name[LVAL] = "LVAL"
tok_name[HIDDEN] = "HIDDEN"
tok_name[SELF] = "SELF"


class TokenizedFile:
    def __init__(self, path: str, style: dict = None, token_factory=None):
        self.path = path
        self.style = style or {}
        self.token_factory = token_factory or ANSIStyledToken

    def __str__(self) -> str:
        return self.token_factory.untokenize(self.tokens, self.style)

    @property
    def file(self):
        try:
            return self._file
        except AttributeError:
            pass
        try:
            self._file = open(self.path, "rb")
        except TypeError:
            self._file = self.path

        return self._file

    @property
    def tokens(self) -> list:
        try:
            return self._tokens
        except AttributeError:
            pass

        self._tokens = list(self.token_factory.tokenize(self.file.readline))
        return self._tokens


class StyledToken:
    """tokenize.TokenInfo compatible object with extended attributes.
    """

    @classmethod
    def tokenize(cls, readline) -> list:
        """
        """
        prev = None
        for token_info in original_tokenize(readline):
            prev = cls(*list(token_info._asdict().values()), prev=prev)
            yield prev

    @staticmethod
    def untokenize(tokens, style: dict = None) -> str:
        """
        """

        style = style or {}
        for token in tokens:
            token.apply_style(style)

        return original_untokenize(tokens).decode()

    def __init__(
        self, type: int, string: str, start: tuple, end: tuple, line: str, prev=None
    ):
        self.type = type
        self.raw_string = string
        self.start = start
        self.end = end
        self.line = line
        self.prev = prev
        self._resolve_upstream()

    @property
    def exact_type(self) -> int:
        try:
            return self._exact_type
        except AttributeError:
            pass
        self._exact_type = self.type
        if self.type == TOKEN.OP:
            try:
                self._exact_type = EXACT_TOKEN_TYPES[self.raw_string]
                return self._exact_type
            except KeyError:
                pass

        if keyword.iskeyword(self.raw_string):
            self._exact_type = KEYWORD

        if self.raw_string in _BUILTINS:
            self._exact_type = BUILTIN

        if self.raw_string.startswith(('"""', "'''")):
            self._exact_type = DOCSTRING

        if self.raw_string.startswith("_"):
            self._exact_type = HIDDEN

        try:
            if self.prev.raw_string == "def":
                self._exact_type = FNAME

            if self.prev.raw_string == "class":
                self._exact_type = CNAME

            if self.prev.raw_string == "import":
                self._exact_type = INAME
        except AttributeError:
            pass

        return self._exact_type

    @exact_type.setter
    def exact_type(self, new_type: int) -> None:
        self._exact_type = new_type

    @property
    def string(self) -> str:
        try:
            return self._string
        except AttributeError:
            pass
        self._string = self.raw_string
        return self._string

    @string.setter
    def string(self, new_string: str) -> None:
        self._string = new_string

    def __repr__(self) -> str:
        msg = "type={}[{:2d}], et={}[{:2d}], string='{}', prev={}, style={}"
        return msg.format(
            tok_name[self.type],
            self.type,
            self.name,
            self.exact_type,
            self.raw_string if "\n" not in self.raw_string else "...",
            self.prev.name if self.prev else "None",
            self.style,
        )

    def __str__(self) -> str:
        return self.string

    def _resolve_upstream(self):
        """Starting at the current token, back track through previous
        tokens and build a list of lvals (left hand side of assignment
        statement). If we spot a comma or a colon upstream, we're probably
        in an argument default assignment clause so abort the lval search.
        If we collect some set of NAME tokens interspersed with other operator
        """

        if self.exact_type != TOKEN.EQUAL:
            return

        lvals = []

        pt = self.prev
        while pt:
            cur_tok, pt = pt, pt.prev

            if cur_tok.type == TOKEN.NAME:
                lvals.append(cur_tok)
                continue

            if cur_tok.exact_type in [TOKEN.LSQB, TOKEN.RSQB, TOKEN.DOT]:
                continue

            if cur_tok.exact_type in [TOKEN.COLON, TOKEN.COMMA]:
                lvals = []

            break

        for lval in lvals:
            lval.exact_type = LVAL

    @property
    def name(self):
        try:
            return self._name
        except AttributeError:
            pass

        try:
            self._name = tok_name[self.exact_type]
        except KeyError as error:
            print(f"missing exact type name {self.exact_type}")
            raise
        return self._name

    @property
    def style(self):
        try:
            return self._style
        except AttributeError:
            pass
        self._style = {}
        return self._style

    @property
    def prev(self):
        try:
            return self._prev
        except AttributeError:
            pass
        self._prev = None
        return self._prev

    @prev.setter
    def prev(self, previous_token):
        self._prev = previous_token

    def apply_style(self, style):
        self.style.update(style.get(self.name, {}))

    def __len__(self):
        return 5

    def __iter__(self):
        return iter([self.type, self.string, self.start, self.end, self.line])


class ANSIStyledToken(StyledToken):
    @property
    def string(self):

        if self.type not in [TOKEN.OP, TOKEN.NAME, TOKEN.STRING, TOKEN.COMMENT]:
            return self.raw_string

        return click.style(self.raw_string, **self.style)
