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
@click.argument(
    "input-file", type=click.File(mode="rb"), default=sys.stdin,
)
@click.option(
    "-o",
    "--output-file",
    type=click.Path(),
    default=None,
    help="Creates a PNG with the supplied path.",
)
@click.option(
    "-l",
    "--start-line",
    default=0,
    help="Line number to begin display.",
    show_default=True,
)
@click.option(
    "-n",
    "--line-count",
    default=10,
    help="Number of lines to display.",
    show_default=True,
)
@click.option(
    "-N",
    "--no-line-numbers",
    is_flag=True,
    default=False,
    help="Disable line numbers in output.",
    show_default=True,
)
@click.option(
    "-p",
    "--preview",
    is_flag=True,
    default=False,
    help="Previews output in window.",
    show_default=True,
)
@click.option(
    "-t",
    "--transparent",
    is_flag=True,
    default=False,
    help="Write output PNG with transparency.",
    show_default=True,
)
@click.option(
    "-s",
    "--style-name",
    type=click.STRING,
    default="default",
    help="Style to apply to input file.",
    show_default=True,
)
@click.option(
    "-f",
    "--font-name",
    type=click.STRING,
    default="courier",
    help="Font name.",
    show_default=True,
)
@click.option(
    "-S",
    "--font-size",
    type=click.INT,
    default=24,
    help="Font size",
    show_default=True,
)
@click.option(
    "-L",
    "--list-styles",
    is_flag=True,
    default=False,
    help="List available styles and exits.",
)
@click.option("-d", "--debug", is_flag=True, hidden=True, default=False)
@click.version_option(VERSION)
def pyliter_cli(
    input_file,
    output_file,
    start_line,
    line_count,
    no_line_numbers,
    preview,
    transparent,
    style_name,
    font_name,
    font_size,
    list_styles,
    debug,
):
    """Python syntax highlighting

    Renders syntax-highlighted text to PNG file and optional previews
    the render in a window before saving.

    If the optional output path is omitted, preview is enabled.

    """

    if list_styles:
        for style in StyleBook.available_styles():
            print(style)
        return

    try:
        stylebook = StyleBook.by_name(style_name)
    except FileNotFoundError:
        print(click.get_current_context().get_help())
        print(f"\nUnknown style: '{style_name}'\n")
        return

    if input_file == sys.stdin:
        input_file = io.BytesIO(sys.stdin.buffer.read())

    if not output_file:
        preview = True

    stylebook.default["font_name"] = font_name
    stylebook.default["font_size"] = font_size

    render = PythonRender(
        input_file,
        start_line,
        line_count,
        stylebook,
        preview,
        transparent,
        not no_line_numbers,
    )

    render.run(output_file)
