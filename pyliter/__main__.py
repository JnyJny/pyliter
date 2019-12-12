""" python syntax highlighting tool
"""

import click
import sys
import yaml

from . import VERSION

from .scrutinizer import Scrutinizer

from importlib.resources import read_text
from . import resources
import io

_DEFAULT_STYLE = "default_style.yaml"


@click.command()
@click.argument("input-file", type=click.File(mode="rb"), default=sys.stdin)
@click.argument("output-file", type=click.File(mode="w"), default=sys.stdout)
@click.option("-s", "--style-file", type=click.Path(exists=True), default=None)
@click.option("-S", "--dump-style", is_flag=True, default=False)
@click.version_option(VERSION)
def pyliter_cli(input_file, output_file, style_file, dump_style):
    """Python syntax highlighting

    Performs Python syntax highlighting on code found in INPUT_FILE
    and writes ANSI escape code annotated source to OUTPUT_FILE. The
    display attributes of various code elements can be styled by
    supplying a YAML file. Use the --dump-style option to view the
    default syntax highlighting style in YAML format.

    """

    if dump_style:
        print(read_text(resources, _DEFAULT_STYLE))
        return

    try:
        style = yaml.safe_load(open(style_file))
    except (AttributeError, TypeError):
        style = yaml.safe_load(read_text(resources, _DEFAULT_STYLE))

    if input_file == sys.stdin:
        input_file = io.BytesIO(sys.stdin.buffer.read())

    scrutinizer = Scrutinizer(input_file, style)

    output_file.write(str(scrutinizer))
