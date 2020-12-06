"""style container
"""


import importlib.resources
import yaml

from pathlib import Path
from webcolors import name_to_rgb, hex_to_rgb

from . import resources


class StyleBook(dict):
    """"""

    @classmethod
    def available_styles(cls) -> list:
        """Return a list of available style books by name."""
        styles = []
        for filename in importlib.resources.contents(resources):
            path = Path(filename)
            if path.match("*_style.yaml"):
                styles.append(path.stem.replace("_style", ""))
        styles.sort()
        return styles

    @classmethod
    def from_any(cls, stylespec: str):
        """Returns a configured StyleBook. First it attempts to load
        a StyleBook from stylespec interpreted as a filesystem path.
        If no file is found, the method next tries to load a StyleBook
        using stylespec is a style name (see `available_styles`).

        If both of those fail, ValueError is raised.

        :param str stylespec: path or style name
        """

        try:
            return cls.from_filename(stylespec)
        except FileNotFoundError:
            pass

        try:
            return cls.by_name(stylespec)
        except FileNotFoundError:
            pass

        raise ValueError(f"unable to find a style matching '{stylespec}'")

    @classmethod
    def by_name(cls, style_name: str):
        """Return a StyleBook initialized with the contents of the
        resource file identified by 'style_name'.

        :param str style_name:
        """
        with importlib.resources.path(resources, f"{style_name}_style.yaml") as path:
            return cls.from_filename(path)

    @classmethod
    def from_filename(cls, filename: str):
        """Return a StyleBook initializes with the contents of the given filename.

        :param str filename:
        """
        path = Path(filename)
        return cls(yaml.safe_load(path.read_text()))

    @classmethod
    def template(cls) -> dict:
        pass

    def __init__(self, styles: dict, name: str = None):
        """
        :param dict styles: dictionary of dictionaries
        """
        self.name = name
        self.update(styles)
        self.validate()

    def validate(self) -> bool:
        """"""
        if "DEFAULT" not in self:
            raise ValueError("Missing DEFAULT style.")

        for category, attributes in self.items():
            for color_key in ["color", "background_color", "underline"]:
                try:
                    color_spec = attributes[color_key]

                    try:
                        color = hex_to_rgb(color_spec)
                    except ValueError:
                        color = name_to_rgb(color_spec)

                    attributes[color_key] = (color.red, color.blue, color.green, 255)
                except KeyError:
                    pass

                except ValueError as error:
                    raise error from None

        return True

    def get(self, key: str) -> dict:
        """Returns a dictionary for the given key."""
        return super().get(key, {})

    def __str__(self):
        """YAML formatted string."""
        return yaml.safe_dump(dict(self), sort_keys=False)

    def save(self, path):
        """Save the contents of this StyleBook to path in YAML format."""
        yaml.safe_dump(dict(self), open(path, "w"), sort_keys=False)

    @property
    def default(self):
        """Returns the DEFAULT style category dictionary."""
        return self.get("DEFAULT")

    @property
    def categories(self):
        """List of style category names."""
        return list(self.keys())
