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


class StyledToken:
    """tokenize.TokenInfo compatible object with extended attributes.
    """

    @classmethod
    def tokenize(cls, readline, style: dict = None) -> list:
        """
        """

        style = style or {}

        tokens = [None]
        for token_info in original_tokenize(readline):
            tokens.append(cls(*list(token_info._asdict().values()), prev=tokens[-1]))

        for token in tokens[1:]:
            token.apply_style(style)
            yield token

    @staticmethod
    def untokenize(tokens) -> str:
        """
        """
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
        if self.exact_type == TOKEN.EQUAL:
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
        msg = "type={}[{:2d}], et={:2d}, name='{}', string='{}', prev={}, style={}"
        return msg.format(
            tok_name[self.type],
            self.type,
            self.exact_type,
            self.name,
            self.string if "\n" not in self.string else "...",
            self.prev.name if self.prev else "None",
            self.style,
        )

    def __str__(self) -> str:
        return self.string

    def _resolve_upstream(self):

        lvals = []

        pt = self.prev
        while pt:
            cur_tok, pt = pt, pt.prev

            if cur_tok.exact_type in [TOKEN.COLON, TOKEN.COMMA]:
                lvals = []
                break

            if cur_tok.exact_type in [TOKEN.DOT] or cur_tok.type == TOKEN.OP:
                continue

            if cur_tok.type == TOKEN.NAME:
                lvals.append(cur_tok)
                continue
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
