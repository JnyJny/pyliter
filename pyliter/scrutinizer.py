"""
"""

import click
import tokenize
import keyword

import builtins


class Scrutinizer:
    def __init__(self, input_file, style: dict = None):
        """
        :param file-like input_file:
        :param dict style:
        """
        self.input = input_file
        self.style = style

    def __str__(self):
        return tokenize.untokenize(self.tokens).decode()

    @property
    def builtins(self) -> list:
        """List of strings that are considered builtins.
        """
        try:
            return self._builtins
        except AttributeError:
            pass
        self._builtins = dir(builtins)
        return self._builtins

    @property
    def definitions(self) -> list:
        """List of python strings which constitue "definitions".
        """
        try:
            return self._definitions
        except AttributeError:
            pass
        self._definitions = ["def", "class"]
        return self._definitions

    def classify(self, token: tokenize.TokenInfo, previous: tokenize.TokenInfo) -> None:
        """Attaches a 'name' attribute to token based.

        :param tokenize.TokenInfo token: 
        :param tokenize.TokenInfo previous: 
        """

        token.name = tokenize.tok_name[token.type]

        if token.exact_type == tokenize.EQUAL:
            try:
                previous.name = "LVAL"
            except AttributeError:
                pass

        if token.exact_type == tokenize.COMMENT:
            token.name = "COMMENT"
            return

        if keyword.iskeyword(token.string):
            token.name = "KEYWORD"

        if token.string in self.builtins:
            token.name = "BUILTINS"

        if token.string.startswith('"""') or token.string.startswith("'''"):
            token.name = "DOCSTRING"

        if token.string.startswith("_"):
            token.name = "PRIVATE"

        try:
            if previous.string in self.definitions:
                token.name = "DEFINITION"
        except AttributeError:
            pass

    def transform(self, token) -> tokenize.TokenInfo:
        """Given a token, the scrutinizer checks to see if the token
        matches configured style classifications. If it does, a new
        token with updated string attribute is created and returned.
        Otherwise, the original unchanged token is returned.

        :param tokenize.TokenInfo token:
        :return: tokenize.TokenInfo
        """

        style = {}
        for classifier in [token.name, token.string]:
            style.update(self.style.get(classifier, {}))

        if not style:
            return token

        styled_token = token._replace(string=click.style(token.string, **style))
        styled_token.name = token.name
        return styled_token

    @property
    def tokens(self) -> list:
        """List of transformed/styled tokens.
        """
        try:
            return self._tokens
        except AttributeError:
            pass

        tokens = [None]
        for token in tokenize.tokenize(self.input.readline):
            self.classify(token, tokens[-1])
            tokens.append(token)

        self._tokens = []
        for token in tokens[1:]:
            if token.type != tokenize.ENCODING:
                token = self.transform(token)
            self._tokens.append(token)

        return self._tokens
