import pyglet

from .token import ExtendedToken as PythonTokens
from .token import DOCSTRING


class PythonDocument(pyglet.text.document.FormattedDocument):
    def __init__(
        self,
        fileobj,
        start: int = 0,
        line_count: int = -1,
        style_book: dict = None,
        number_lines: bool = False,
        transparent: bool = False,
        debug: bool = False,
    ):

        # The Order of Operations:
        # 1. setup subclass-specific attributes
        # 2. call __init__ of superclass
        # 3. set the default document style
        # 4. style documents with token derived attributes
        # 5. insert line numbers if requested
        # 6. trim document to keep lines in range [start, start+line_count]

        self.style_book = style_book or {
            "DEFAULT": {
                "font_name": "Source Code Pro",
                "font_size": 18,
                "color": (255, 255, 255, 255),
                "background_color": (0, 0, 0, 255),
                "line_numbers": False,
            }
        }

        if transparent:
            r, g, b, a = self.style_book["DEFAULT"]["background_color"]
            self.style_book["DEFAULT"]["background_color"] = (r, g, b, 0)

        self.tokens, self.raw_text = PythonTokens.from_file(fileobj)

        super().__init__(self.raw_text.translate(str.maketrans({"{": "{{", "}": "}}"})))

        self.set_style(start=0, end=self.eot, attributes=self.style_book["DEFAULT"])

        self._apply_token_styles()

        if number_lines:
            self._insert_line_numbers()

        if debug:
            # EJO - styles each line with a green underscore at the front and a
            #       red underscore at the end
            for i, (b, e) in enumerate(self._line_extents):
                self.set_style(b, b + 1, attributes={"underline": (0, 255, 0, 255)})
                self.set_style(e - 1, e, attributes={"underline": (255, 0, 0, 255)})

        self._keep(start, line_count)

    @property
    def eot(self):
        """End Of Text: integer position of the last character in self.text."""
        return len(self.text) + 1

    def _keep(self, start, line_count) -> None:
        """Keep the lines in the range of [start, start+line_count]."""
        self._trim_lines(0, start)
        off = 0 if start == 0 else 1
        self._trim_lines(line_count + off, len(self.text.splitlines()))

    def _trim_lines(self, from_line: int, to_line: int) -> None:
        """Removes the lines from self.text in the range of [from_line, to_line]"""
        if from_line == to_line:
            return
        extents = self._line_extents
        self.delete_text(extents[from_line][0], extents[to_line - 1][1])

    @property
    def _line_extents(self) -> list:
        """A list of tuples, each tuple is the starting and ending
        index into self.text of a line. Line 0 is the first tuple and
        so on. Lines are defined as a substring ending in a newline
        character '\n'.  Note: line extents change after text insert
        and delete options, so don't hang onto this list between
        operations.
        """
        p = 0
        extents = []
        while True:
            try:
                e = self.text.index("\n", p)
                extents.append((p, e))
                p = e + 1
            except ValueError:
                e = self.eot
                extents.append((p, e))
                break
        return extents

    def _insert_line_numbers(self, color: tuple = None) -> None:
        """Adds line numbers to the beginning of each line
        starting at line zero. Line numbers are four digits
        right justified and rendered with the given color.

        :param tuple color: 4-tuple of integers [0,255]
        """

        color = color or (0xA0, 0xA0, 0xA0, 0xA0)  # dark gray

        p = 0
        line_num = 0
        attributes = {
            "color": color,
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

    def _apply_token_styles(self, tokens: list = None, style_book: dict = None) -> None:
        """Using the token category as a key into the style book, look for
        the starting position of each token and apply the appropriate style.

        :param list tokens:
        :param dict style_book:
        """

        tokens = tokens or self.tokens
        style_book = style_book or self.style_book

        p = 0

        for token in tokens:
            if not token.category in style_book:
                continue

            if token.exact_type == DOCSTRING:
                try:
                    p = self.text.index('"""', p)
                except ValueError:
                    pass
                try:
                    e = self.text.index('"""', p + 1) + 3
                except ValueError:
                    e = self.eot
            else:
                try:
                    p = self.text.index(token.string, p)
                    e = p + len(token.string)
                except ValueError:
                    print("F", "pos", p, "str", token.string, repr(token))
                    continue

            self.set_style(p, e, style_book[token.category])
            p = e

    @property
    def background_color(self) -> tuple:
        """Convenience accessor for self.style_book['DEFAULT']['background_color']."""
        return self.style_book["DEFAULT"]["background_color"]

    @property
    def color(self) -> tuple:
        """Convenience accessor for self.style_book['DEFAULT']['color']."""
        return self.style_book["DEFAULT"]["color"]

    @property
    def dimensions(self) -> tuple:
        """A 2-tuple of width and height expressed in pixels."""

        lines = self.text.splitlines()
        maxc = max(len(l) for l in lines)
        nlines = len(lines) + 1

        return (
            maxc * self.font.size,
            nlines * self.font.height,
        )

    @property
    def font(self):
        """Convenience accessor for self.get_font() whose side-effect
        is setting a "height" attribute on font calculated with the
        sum of the font's ascent and abs(descent) values.
        """
        try:
            return self._font
        except AttributeError:
            pass

        self._font = self.get_font(0)

        self._font.height = self._font.ascent - self._font.descent

        return self._font
