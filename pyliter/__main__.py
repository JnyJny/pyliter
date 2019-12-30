""" python syntax highlighting tool

"""

import click
import io
import sys
import yaml


from . import VERSION
from .render import PythonRender
from .style_book import StyleBook


# Fun comment here
#


@click.command()
@click.argument("input-file", type=click.File(mode="rb"), default=sys.stdin)
@click.option("-o", "--output-file", type=click.Path(), default=None)
@click.option("-l", "--start-line", default=0, help="line to begin displaying")
@click.option("-n", "--line-count", default=10, help="number of lines to display")
@click.option("-p", "--preview", is_flag=True, default=False)
@click.option("-t", "--transparent", is_flag=True, default=False)
@click.option("-s", "--style-name", type=click.STRING, default="default")
@click.option("--list-styles", is_flag=True, default=False)
@click.option("-d", "--debug", is_flag=True, hidden=True, default=False)
@click.version_option(VERSION)
def pyliter_cli(
    input_file,
    output_file,
    start_line,
    line_count,
    preview,
    transparent,
    style_name,
    list_styles,
    debug,
):
    """Python syntax highlighting

    Renders syntax-highlighted text to PNG file and optional previews
    the render in a window before saving.

    Examples:

    $ pyliter awesome_snippet.py -o awesome_snippet.png

    $ pyliter -o awesome_snippet.png < awesome_snippet.py

    $ pyliter awesome_snippet.py -p

    $ pyliter awesome_snippet.py -p -l 11 -n 27

    """

    if not output_file:
        preview = True

    stylebook = StyleBook.by_name(style_name)

    if input_file == sys.stdin:
        input_file = io.BytesIO(sys.stdin.buffer.read())

    render = PythonRender(
        input_file, start_line, line_count, stylebook, preview, transparent
    )

    render.run(output_file)
