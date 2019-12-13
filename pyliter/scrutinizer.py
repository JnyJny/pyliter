"""
"""

from .token import ANSIStyledToken


class Scrutinizer:
    def __init__(self, input_file, style: dict = None):
        """
        :param file-like input_file:
        :param dict style:
        """
        self.input = input_file
        self.style = style or {}

    def __str__(self):
        return ANSIStyledToken.untokenize(self.tokens)

    @property
    def tokens(self) -> list:
        """List of transformed/styled tokens.
        """
        try:
            return self._tokens
        except AttributeError:
            pass

        self._tokens = list(ANSIStyledToken.tokenize(self.input.readline, self.style))

        return self._tokens
