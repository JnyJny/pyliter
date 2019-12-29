import pyglet

from .token import ExtendedToken as PythonTokens
from .token import DOCSTRING


class PythonDocument(pyglet.text.document.FormattedDocument):
    def __init__(
        self, fileobj, start: int = 0, line_count: int = -1, style_book: dict = None
    ):

        self.style_book = style_book or {
            "DEFAULT": {
                "font_name": "Source Code Pro",
                "font_size": 18,
                "color": (255, 255, 255, 255),
                "background_color": (0, 0, 0, 255),
                "line_numbers": False,
            }
        }
        self.first = start
        self.last = start + line_count

        self.tokens, self.raw_text = PythonTokens.from_file(fileobj, start, line_count)

        super().__init__(self.raw_text.translate(str.maketrans({"{": "{{", "}": "}}"})))

        self.line_count = len(self.text.splitlines()) + 1
        # FormattedDocument does some messing about with newlines in the source
        # text which results in the loss of the terminal newline. This in turn
        # causes an off-by-one bug when counting the number of lines in the text.

        self.set_style(
            start=0, end=len(self.text), attributes=self.style_book["DEFAULT"]
        )

        self._apply_token_styles()

        if self.style_book["DEFAULT"].get("line_numbers", False):
            self._insert_line_numbers(start)

    def _insert_line_numbers(self, start):
        """
        """
        p = 0
        line_num = start
        attributes = {
            "color": (0xA0, 0xA0, 0xA0, 0xFF),
            "underline": None,
            "bold": None,
            "italic": None,
        }
        while True:
            try:
                self.insert_text(p, f"{line_num:>4d} ", attributes=attributes)
                p = self.text.index("\n", p) + 1
                line_num += 1
            except ValueError:
                break

    def _apply_token_styles(self, tokens: list = None) -> None:
        """
        """
        tokens = tokens or self.tokens

        p = 0

        for token in tokens:
            if not token.category in self.style_book:
                continue

            try:
                if token.exact_type == DOCSTRING:
                    p = self.text.index('"""', p)
                    l = self.text.index('"""', p + 1) + 3
                else:
                    p = self.text.index(token.string, p)
                    l = len(token.string)
            except ValueError:
                print("F", p, token.string)
                print(repr(token))
                continue

            self.set_style(p, p + l, self.style_book[token.category])
            p += l

    @property
    def background_color(self) -> tuple:
        """
        """
        return self.style_book["DEFAULT"]["background_color"]

    @property
    def color(self) -> tuple:
        """
        """
        return self.style_book["DEFAULT"]["color"]

    @property
    def dimensions(self) -> tuple:
        """
        """
        try:
            return self._dimensions
        except AttributeError:
            pass
        self._dimensions = (
            self.max_column * self.font.size,
            self.line_count * self.font.height,
        )

        return self._dimensions

    @property
    def max_column(self) -> int:
        """
        """
        try:
            return self._max_column
        except AttributeError:
            pass
        self._max_column = max(len(l.strip()) for l in self.raw_text.splitlines())
        return self._max_column

    @property
    def font(self):
        """
        """
        try:
            return self._font
        except AttributeError:
            pass

        self._font = self.get_font(0)

        self._font.height = self._font.ascent - self._font.descent

        return self._font
