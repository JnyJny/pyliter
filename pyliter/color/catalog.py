"""
"""

import collections
import yaml

from importlib.resources import read_text
from .. import resources


def make_color_key(name):
    """Normalizes a color name to a lowercase string with
    no embedded white space; tabs, newlines, newline/returns
    and spaces are removed.
    """

    tt = str.maketrans({"\n": "", "\t": "", "\r": "", " ": ""})

    return name.translate(tt).strip().casefold()


COLORS_BY_NAME = collections.ChainMap()
COLORS_BY_NAME.maps.pop()

for catalog_file in resources.color_catalog_files:
    catalog = {}
    for k, v in yaml.safe_load(read_text(resources, catalog_file)).items():
        catalog.setdefault(make_color_key(k), tuple(v))
    COLORS_BY_NAME.maps.append(catalog)


NAMES_BY_COLOR = {v: k for k, v in COLORS_BY_NAME.items()}
# this clobbers some alternate spellings/names
# aqua =/= cyan
# grey =/= gray in substrings of names

ALL_NAMES_BY_COLOR = {}
for k, v in COLORS_BY_NAME.items():
    ALL_NAMES_BY_COLOR.setdefault(v, []).append(k)
