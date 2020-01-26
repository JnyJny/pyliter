""" python syntax highlighting tool

"""


import io
import pathlib
import sys
import typer
import yaml

from . import VERSION
from .render import PythonRender
from .style_book import StyleBook

pyliter_cli = typer.Typer()


def print_version(ctx, param, value):
    if not value:
        return
    typer.secho("version ", fg="red", nl=False)
    typer.secho(VERSION, fg="green")
    raise typer.Exit()


@pyliter_cli.command()
def main(
    input_file: pathlib.Path = typer.Argument("-", allow_dash=True),
    output_file: pathlib.Path = typer.Argument(None),
    start_line: int = typer.Option(0, "--start-line", "-l", show_default=True),
    line_count: int = typer.Option(10, "--line-count", "-c", show_default=True),
    no_line_numbers: bool = typer.Option(False, "--no-line-numbers", "-N"),
    preview: bool = typer.Option(
        False, "--preview", "-p", help="Preview rendered code in a window."
    ),
    transparent: bool = typer.Option(
        False, "--transparent", "-t", help="Enable transparent background."
    ),
    style_name: str = typer.Option(
        "default", "--style", "-S", help="Colors to style text."
    ),
    font_name: str = typer.Option("courier", "--font-name", "-f", show_default=True),
    font_size: int = typer.Option(24, "--font-size", "-s", show_default=True),
    list_styles: bool = typer.Option(False, "--list-styles", "-L", help=""),
    version: bool = typer.Option(
        False, "--version", "-v", is_eager=True, callback=print_version
    ),
):
    """Python syntax highlighting

    Renders syntax-highlighted text to PNG file or preview the render in
    a window.

    If the optional output path is omitted, preview is enabled
    automatically.
    """

    if list_styles:
        for style in StyleBook.available_styles():
            print(style)
        return

    try:
        stylebook = StyleBook.from_any(style_name)
    except ValueError as error:
        print_help(str(error))
        return

    if input_file.name == "-":
        input_file = io.BytesIO(sys.stdin.buffer.read())
    else:
        input_file = input_file.open("rb")

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


def print_help(msg: str) -> None:
    """Print the help message for the current click context
    and the supplied message.

    :param str msg:
    """
    print(click.get_current_context().get_help())
    print(f"\n{msg}\n")


pyliter_style_cli = typer.Typer()


@pyliter_style_cli.command()
def pyliter_style():
    """Manage pyliter styles.
    """
    pass
