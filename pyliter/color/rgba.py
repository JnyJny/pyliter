"""
"""

import yaml

from .catalog import COLORS, REVERSE_LOOKUP
from .exceptions import ColorNameNotFound
from .value import Value8


class RGBAColor32:
    """
    RGBA models 32-bit color values:
    - 8 bits for red
    - 8 bits for green
    - 8 bits for blue
    - 8 bits for alpha (transparency)

    Colors may be specified by their component values, chosen by
    name or by hexadecimal string or integer representation. 

    """

    @classmethod
    def from_name(cls, name: str, alpha: int = Value8.maximum):
        """Attempts to locate RGB values for the color named.

        :param str name:
        :param int alpha:
        
        Raises:
        - ColorNameNotFound

        :param str name:
        :param int alpha:
        """
        key = name.replace(" ", "").strip().lower()
        try:
            r, g, b = COLORS[key]
        except KeyError:
            raise ColorNameNotFound(name) from None
        return cls(r, g, b, alpha)

    @classmethod
    def from_value(cls, value: int):
        """
        :param int value:
        """
        return cls.from_hex_string(f"{value:08x}")

    @classmethod
    def from_hex_string(cls, hex_string: str):
        """Returns a RGBA color constructed with the supplied hex string.

        Hex string prefixes '#' or '0x' are ignored.

        Expected hex formats:

        3 digit: RGB
        4 digit: RGBA
        6 digit: RRGGBB
        8 digit: RRGGBBAA

        R - red
        G - green
        B - blue
        A - alpha

        :param str hex_string:
        """

        try:
            if hex_string.startswith("#"):
                hex_string = hex_string[1:]
        except AttributeError:
            raise ValueError(f"str or int expected, received {type(hex_string)}")

        if hex_string.startswith("0x"):
            hex_string = hex_string[2:]

        if len(hex_string) not in [3, 4, 6, 8]:
            raise ValueError(f"cannot decode '{hex_string}'")

        if len(hex_string) in [3, 4]:

            def scale_8_to_16(value):
                return round(255 * int(value, 16) / 15)

            return cls(*tuple(scale_8_to_16(v) for v in hex_string))

        byte_values = [hex_string[x : x + 2] for x in range(0, len(hex_string), 2)]

        return cls(*[int(v, 16) for v in byte_values])

    @classmethod
    def from_scale(cls, red: float, green: float, blue: float, alpha: float = 1.0):
        """
        :param float red:
        :param float green:
        :param float blue:
        :param float alpha:
        """
        color = cls(0, 0, 0, 0)
        color.red = Value8.from_scale(red)
        color.green = Value8.from_scale(green)
        color.blue = Value8.from_scale(blue)
        color.alpha = Value8.from_scale(alpha)
        return color

    def __init__(self, red: int, green: int, blue: int, alpha: int = Value8.maximum):
        self.red = Value8(red)
        self.green = Value8(green)
        self.blue = Value8(blue)
        self.alpha = Value8(alpha)

    @property
    def name(self) -> str:
        """Color name if in the catalog otherwise 'unnamed'."""
        return REVERSE_LOOKUP.get(self.rgb, "unnamed")

    @property
    def value(self) -> int:
        """
        """
        return int(self.hex[1:], 16)

    @property
    def hex(self) -> str:
        """An eight digit hex string prefixed with an octothorpe: #RRGGBBAA
        """
        return f"#{self.red.hex}{self.green.hex}{self.blue.hex}{self.alpha.hex}"

    @property
    def rgba(self) -> tuple:
        """Four-tuple of integer values: (red, green, blue, alpha).
        """
        return (self.red.value, self.green.value, self.blue.value, self.alpha.value)

    @property
    def rgb(self) -> tuple:
        """Three-tuple of integer values: (red, green, blue).
        """
        return tuple(self.rgba[:3])

    @property
    def rgba_f(self) -> tuple:
        """Four-tuple of float values: (red, green, blue, alpha).
        """
        return (self.red.scale, self.green.scale, self.blue.scale, self.alpha.scale)

    @property
    def rgb_f(self) -> tuple:
        """Three-tuple of float values: (red, green, blue).
        """
        return tuple(self.rgba_f[:3])

    def as_dict(self) -> dict:
        """Returns a dictionary representation of this class.
        """
        return {
            "name": self.name,
            "red": self.red.value,
            "green": self.green.value,
            "blue": self.blue.value,
            "alpha": self.alpha.value,
        }
