"""
"""

import yaml

from pathlib import Path
import importlib.resources
from . import resources
from .color import Color


class StyleBook(dict):
    @classmethod
    def available_styles(cls) -> list:
        """Return a list of available style books by name.
        """
        styles = []
        for filename in importlib.resources.contents(resources):
            path = Path(filename)
            if path.match("*_style.yaml"):
                styles.append(path.stem.replace("_style", ""))
        return styles

    @classmethod
    def by_name(cls, style_name: str):
        """Return a StyleBook initialized with the contents of the
        resource file identified by 'style_name'.
        """
        with importlib.resources.path(resources, f"{style_name}_style.yaml") as path:
            return cls.from_filename(path)

    @classmethod
    def from_filename(cls, filename: str):
        """Return a StyleBook initializes with the contents of the given filename.
        """
        path = Path(filename)
        return cls(yaml.safe_load(path.read_text()))

    def __init__(self, styles: dict):
        """
        :param dict styles: dictionary of dictionaries
        """

        self.update(styles)

        for category, attributes in self.items():
            for color_key in ["color", "background_color", "underline"]:
                try:
                    color_spec = attributes[color_key]
                    color = Color.from_any(color_spec)
                    attributes[color_key] = color.rgba
                except KeyError:
                    pass

    def get(self, key: str) -> dict:
        """Returns a dictionary for the given key.
        """
        return super().get(key, {})

    def __str__(self):
        """YAML formatted string.
        """
        return yaml.safe_dump(dict(self), sort_keys=False)

    def save(self, path):
        """Save the contents of this StyleBook to path in YAML format.
        """
        yaml.safe_dump(dict(self), open(path, "w"), sort_keys=False)

    @property
    def default(self):
        """Returns the DEFAULT style category dictionary.
        """
        return self.get("DEFAULT")

    @property
    def styles(self):
        """List of style category names.
        """
        return list(self.keys())
