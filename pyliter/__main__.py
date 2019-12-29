""" python syntax highlighting tool

"""

import click
import sys
import yaml

from importlib.resources import read_text

from . import VERSION
from .render import OnscreenRender
from .color import Color

from . import resources
import io

# Fun comment here
#


@click.command()
@click.argument("input-file", type=click.File(mode="rb"), default=sys.stdin)
@click.argument("output-file", type=click.Path(allow_dash=True), default=sys.stdout)
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

    Performs Python syntax highlighting on code found in INPUT_FILE
    and writes color annotated text in PNG format to OUTPUT_FILE.

    Display attributes of various code elements can be styled by
    supplying a YAML file
    """

    style = yaml.safe_load(read_text(resources, "default_style.yaml"))

    for category, attributes in style.items():
        for color_key in ["color", "background_color", "underline"]:
            try:
                color_spec = attributes[color_key]
                color = Color.from_any(color_spec)
                if color_key == "background_color" and transparent:
                    color.alpha.value = 0
                attributes[color_key] = color.rgba
            except KeyError:
                pass

    if input_file == sys.stdin:
        input_file = io.BytesIO(sys.stdin.buffer.read())

    render = OnscreenRender(input_file, start_line, line_count, style, output_file)

    render.run(preview)
