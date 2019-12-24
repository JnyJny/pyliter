"""
"""

import collections
import yaml

from importlib.resources import read_text
from .. import resources


COLORS = collections.ChainMap()
COLORS.maps.pop()

for catalog_file in resources.color_catalog_files:
    COLORS.maps.append(yaml.safe_load(read_text(resources, catalog_file)))

REVERSE_LOOKUP = {tuple(v): k for k, v in COLORS.items()}
