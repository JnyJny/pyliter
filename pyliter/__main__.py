""" python syntax highlighting tool

"""

import io
import sys

import typer
import yaml

from pathlib import Path

from .render import PythonRender
from .style_book import StyleBook


cli = typer.Typer()


@cli.callback()
def pyliter_main(ctx: typer.Context):
    """Python syntax highlighting"""


@cli.command(name="list")
def pyliter_list_styles():
    """List builtin text styles."""
    for style in StyleBook.available_styles():
        typer.secho(style)


@cli.command(name="render")
def pyliter_render(
    input_file: typer.FileBinaryRead,
    output_file: Path = typer.Option(None, "--output", "-o"),
    start_line: int = typer.Option(0, "--start-line", "-s"),
    line_count: int = typer.Option(10, "--line-count", "-L"),
    no_line_numbers: bool = typer.Option(
        False, "--no-line-numbers", "-N", is_flag=True
    ),
    preview: bool = typer.Option(False, "--preview", "-p", is_flag=True),
    transparent: bool = typer.Option(False, "--transparent", "-t", is_flag=True),
    style_name: str = "default",
    font_name: str = "courier",
    font_size: int = 24,
):
    """Renders syntax-highlighted text to PNG file or displayed in a window.

    If the optional output path is omitted, preview is enabled
    automatically.
    """

    try:
        stylebook = StyleBook.from_any(style_name)
    except ValueError as error:
        print_help(str(error))
        return

    if input_file.name == "-":
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
