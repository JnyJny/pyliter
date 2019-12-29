""" pyglet application
"""
import pyglet
from .document import PythonDocument

# Comment goes here
#         some more


class OnscreenRender(pyglet.window.Window):
    def __init__(
        self,
        fileobj,
        start_line,
        line_count,
        style_book: dict = None,
        debug: bool = False,
    ):

        self.debug = debug
        self.document = PythonDocument(fileobj, start_line, line_count, style_book)

        width, height = self.document.dimensions

        config = pyglet.gl.Config(sample_buffers=8, samples=8, double_buffer=True)

        super().__init__(
            width=width + self.margin,
            height=height + self.margin,
            config=config,
            visible=True,
        )

        pyglet.gl.glClearColor(*self.document.background_color)

        self.layout.x = self.margin
        self.layout.y = self.margin

        if self.debug:
            self.batch.add(
                8,
                pyglet.gl.GL_LINES,
                self.background,
                ("v2i", self.text_bounds),
                ("c3B", (255, 0, 0) * 8),
            )

    @property
    def margin(self):
        try:
            return self._margin
        except AttributeError:
            pass
        self._margin = self.document.font.height * 2
        return self._margin

    @property
    def batch(self):
        try:
            return self._batch
        except AttributeError:
            pass
        self._batch = pyglet.graphics.Batch()
        return self._batch

    @property
    def foreground(self):
        try:
            return self._foreground
        except AttributeError:
            pass
        self._foreground = pyglet.graphics.OrderedGroup(0)
        return self._foreground

    @property
    def background(self):
        try:
            return self._background
        except AttributeError:
            pass
        self._background = pyglet.graphics.OrderedGroup(1)
        return self._background

    @property
    def layout(self):
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
            batch=self.batch,
            group=self.foreground,
        )
        return self._layout

    def on_draw(self):
        self.clear()

        if self.debug:
            pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
            pyglet.gl.glBlendFunc(
                pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA
            )
            pyglet.gl.glColor4f(1, 0, 0, 1)
            pyglet.gl.glLineWidth(3)
        self.batch.draw()
        self.save()

    def save(self, filename: str = None) -> None:

        filename = filename or "output.png"
        pyglet.image.get_buffer_manager().get_color_buffer().save(filename)

    @property
    def text_bounds(self):
        try:
            return self._text_bounds
        except AttributeError:
            pass

        x = self.layout.x
        y = self.layout.y
        w = x + self.layout.width
        h = x + self.layout.height + 1

        self._text_bounds = (x, y, x, h, x, h, w, h, w, h, w, y, w, y, x, y)
        return self._text_bounds

    def run(self):
        pyglet.app.run()
