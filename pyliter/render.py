""" python rendering pyglet Window
"""
import pyglet
from .document import PythonDocument
from .color import Color


class PythonRender(pyglet.window.Window):
    def __init__(
        self,
        fileobj,
        start_line,
        line_count,
        style_book: dict = None,
        preview: bool = False,
        output_path: str = None,
    ):
        """Render syntax-highlighted Python code to a window using
        the supplied style_book.

        :param fileobj:     file-like object containing Python text
        :param start_line:  line to begin rendering
        :param line_count:  number of lines to render
        :param style_book:  dictionary of style dictionaries
        :param output_path: save rendered text to path
        :param preview:     controls whether the render text is displayed

        """
        self.output_path = output_path
        self.preview = preview

        self.document = PythonDocument(fileobj, start_line, line_count, style_book)

        width, height = self.document.dimensions

        try:
            caption = fileobj.name
        except AttributeError:
            caption = "stdin"

        super().__init__(
            width=width + (self.margin * 2),
            height=height + (self.margin * 2),
            visible=preview,
            caption=caption,
        )

        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        pyglet.gl.glClearColor(*Color(*self.document.background_color).rgba_f)

        if (self.width, self.height) != self.get_viewport_size():
            # EJO - this is magic
            pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
            pyglet.gl.glLoadIdentity()
            width, height = self.get_viewport_size()
            pyglet.gl.glOrtho(0, width, 0, height, -1, 1)
            pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)
            # EOM - end of magic

        self.layout.x = self.margin
        self.layout.y = self.margin

    @property
    def margin(self):
        """The width of the margin around the TextLayout widget;
        top, bottom and sides.
        """
        try:
            return self._margin
        except AttributeError:
            pass
        self._margin = self.document.font.height // 2
        return self._margin

    @property
    def layout(self):
        """A pyglet.text.layout.TextLayout widget configured to be
        rendered in the window's batch in the foreground group.
        """
        try:
            return self._layout
        except AttributeError:
            pass

        self._layout = pyglet.text.layout.TextLayout(
            self.document,
            self.width - (self.margin * 2),
            self.height - (self.margin * 2),
            multiline=True,
            wrap_lines=False,
        )
        return self._layout

    def on_draw(self):
        """Clear the window and draw it's contents (again).
        """
        self.clear()
        self.layout.draw()
        self._save()

    def _save(self):
        """Saves the contents of this window to self.output_path.
        """

        if not self.output_path:
            return

        image = pyglet.image.get_buffer_manager().get_color_buffer()

        if (self.width, self.height) != self.get_viewport_size():
            image = image.get_region(0, 0, self.width, self.height)

        image.save(self.output_path)

    def run(self):
        """
        """
        if not self.preview:
            self.on_draw()
            return

        pyglet.app.run()
