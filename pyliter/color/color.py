from .catalog import COLORS_BY_NAME, NAMES_BY_COLOR, make_color_key
from .exceptions import ColorNameNotFound
from .value import Value8


class Color:
    """A 32-bit RGBA based color with four 8-bit channels:

    - red
    - green
    - blue
    - alpha (transparency)

    Colors may be specified by their component values, chosen by name,
    hexadecimal string or integer representation, by HSL or HSV tuples.
    """

    @classmethod
    def from_any(cls, colorspec, tuple_type: str = None):

        try:
            return cls.from_value(colorspec)
        except ValueError:
            pass

        try:
            return cls.from_name(colorspec)
        except ColorNameNotFound:
            pass

        try:
            return cls.from_hex_string(colorspec)
        except ValueError:
            pass

        try:
            return cls(*colorspec)
        except Exception:
            raise TypeError(f"unable to decode colorspec {type(colorspec)}") from None

    @classmethod
    def from_name(cls, name: str, alpha: int = Value8.maximum):
        """Attempts to locate RGB values for the color name given.

        :param str name:
        :param int alpha: range [0,255], defaults to 255
        
        Raises:
        - ColorNameNotFound

        :param str name:
        :param int alpha:
        """
        try:
            r, g, b = COLORS_BY_NAME[make_color_key(name)]
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
        """Returns a RGBA color constructed from a string composed of

        hexidecimal digits. Traditional hex string prefixes '#' or '0x'
        are ignored.

        Supported hex string formats:

        3 digit: RGB
        4 digit: RGBA
        6 digit: RRGGBB
        8 digit: RRGGBBAA

        R - red, G - green, B - blue, A - alpha

        If the alpha channel is not present (3 or 6 digits), it defaults
        to 0xff.

        Three and four digit hex values are scaled from 4-bit to 8-bit
        color.

        :param str hex_string:
        """

        try:
            if hex_string.startswith("#"):
                hex_string = hex_string[1:]
        except AttributeError:
            raise ValueError(f"str expected, not {type(hex_string)}")

        if hex_string.startswith("0x"):
            hex_string = hex_string[2:]

        hex_string_len = len(hex_string)

        if hex_string_len not in [3, 4, 6, 8]:
            raise ValueError(f"cannot decode '{hex_string}'")

        if hex_string_len in [3, 4]:

            def scale_8_to_16(value):
                return round(255 * (int(value, 16) / 15))

            return cls(*tuple(scale_8_to_16(v) for v in hex_string))

        byte_values = [hex_string[x : x + 2] for x in range(0, hex_string_len, 2)]

        return cls(*[int(v, 16) for v in byte_values])

    @classmethod
    def from_scale(cls, red: float, green: float, blue: float, alpha: float = 1.0):
        """
        :param float red: [0, 1]
        :param float green: [0, 1]
        :param float blue: [0, 1]
        :param float alpha: [0, 1]
        """
        color = cls(0, 0, 0, 0)
        color.red = Value8.from_scale(red)
        color.green = Value8.from_scale(green)
        color.blue = Value8.from_scale(blue)
        color.alpha = Value8.from_scale(alpha)
        return color

    @classmethod
    def from_hsl(
        cls, hue: float, saturation: float, lightness: float, alpha: float = 1.0
    ):
        """
        :param float hue: [0, 359] degrees
        :param float saturation: [0, 1]
        :param float lightness: [0, 1]
        :param float alpha: [0, 1]
        """
        hue %= 360
        saturation, lightness, alpha = map(
            lambda v: min(1.0, max(v, 0.0)), [saturation, lightness, alpha]
        )

        c = (1 - (abs((2 * lightness) - 1))) * saturation
        x = c * (1 - abs(((hue / 60) % 2) - 1))
        m = lightness - (c / 2)

        try:
            return cls._from_hcxma(hue, c, x, m, alpha, "hsl")
        except ValueError as error:
            raise error from None

    @classmethod
    def from_hsv(cls, hue: float, saturation: float, value: float, alpha: float = 1.0):
        """
        :param float hue: [0, 359] degrees
        :param float saturation: [0, 1]
        :param float value: [0, 1]
        :param float alpha: [0, 1]
        """
        hue %= 360
        saturation, value, alpha = map(
            lambda v: min(1.0, max(v, 0.0)), [saturation, value, alpha]
        )

        c = value * saturation
        x = c * (1 - abs(((hue / 60) % 2) - 1))
        m = value - c

        try:
            return cls._from_hcxma(hue, c, x, m, alpha, "hsv")
        except ValueError as error:
            raise error from None

    @classmethod
    def _from_hcxma(
        cls, hue: float, c: float, x: float, m: float, alpha: float, src: str
    ):
        """Common conversion from HSL/HSV to RGB.

        :param float hue: degrees constrained between 0 and 359
        :param float c: 
        :param float x:
        :param float m:
        :param float alpha: [0,1]
        :param str src: string identifying source conversion format ['hsv'|'hsl']
        """

        rgb = {
            0: (c + m, x + m, 0 + m),
            60: (x + m, c + m, 0 + m),
            120: (0 + m, c + m, x + m),
            180: (0 + m, x + m, c + m),
            240: (x + m, 0 + m, c + m),
            300: (c + m, 0 + m, x + m),
        }

        color = cls(0, 0, 0, 0)
        color.alpha = Value8.from_scale(alpha)

        for key, values in rgb.items():
            if key <= hue <= key + 60:
                color.red, color.green, color.blue = map(Value8.from_scale, values)
                break
        else:
            raise ValueError(f"problem converting {src} to rgb")

        return color

    @classmethod
    def from_cmyk(
        cls,
        cyan: float,
        magenta: float,
        yellow: float,
        black: float,
        alpha: float = 1.0,
    ):
        """
        :param float cyan: [0, 1]
        :param float magenta: [0, 1]
        :param float yellow: [0, 1]
        :param float black: [0, 1]
        :param float alpha: [0, 1]
        """

        r = (1.0 - cyan) * (1.0 - black)
        g = (1.0 - magenta) * (1.0 - black)
        b = (1.0 - yellow) * (1.0 - black)

        return cls.from_scale(r, g, b, alpha)

    def __init__(self, red: int, green: int, blue: int, alpha: int = Value8.maximum):
        """
        :param int red: [0, 255]
        :param int green: [0, 255]
        :param int blue: [0, 255]
        :param int alpha: [0, 255]
        """
        self.red = Value8(red)
        self.green = Value8(green)
        self.blue = Value8(blue)
        self.alpha = Value8(alpha)

    def __repr__(self):

        return "{}(red={}, green={}, blue={}, alpha={})".format(
            self.__class__.__name__,
            self.red.value,
            self.green.value,
            self.blue.value,
            self.alpha.value,
        )

    def __eq__(self, other):
        return self.rgba == other.rgba

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __hash__(self):
        return self.value

    @property
    def name(self) -> str:
        """Color name if RGB tuple present in the catalog otherwise 'unnamed'."""
        return NAMES_BY_COLOR.get(self.rgb, "unnamed")

    @property
    def value(self) -> int:
        """A 32-bit integer color representation.
        """
        return int(self.hex[1:], 16)

    @property
    def hex(self) -> str:
        """An eight digit hex string prefixed with an octothorpe: #RRGGBBAA
        """
        return "#" + self.red.hex + self.green.hex + self.blue.hex + self.alpha.hex

    @property
    def rgb(self) -> tuple:
        """Three-tuple of integer values: (red, green, blue).
        """
        return (self.red.value, self.green.value, self.blue.value)

    @property
    def rgba(self) -> tuple:
        """Four-tuple of integer values: (red, green, blue, alpha).
        """
        return self.rgb + (self.alpha.value,)

    @property
    def rgb_f(self) -> tuple:
        """Three-tuple of float values: (red, green, blue).
        """
        return (self.red.scale, self.green.scale, self.blue.scale)

    @property
    def rgba_f(self) -> tuple:
        """Four-tuple of float values: (red, green, blue, alpha).
        """
        return self.rgb_f + (self.alpha.scale,)

    @property
    def hsl(self) -> tuple:
        """Three-tuple of float values: (hue, saturation, lightness)

        Hue is a float in [0, 359]
        Saturation is a float in [0,1]
        Lightness is a float in [0,1]
        """
        c_max = max(self.rgb_f)
        c_min = min(self.rgb_f)
        c_delta = c_max - c_min

        try:
            if c_max == self.red.scale:
                hue = ((self.green.scale - self.blue.scale) / c_delta) % 6
            if c_max == self.green.scale:
                hue = ((self.blue.scale - self.red.scale) / c_delta) + 2
            if c_max == self.blue.scale:
                hue = ((self.red.scale - self.green.scale) / c_delta) + 4
        except ZeroDivisionError:
            hue = 0

        hue *= 60
        lightness = (c_max + c_min) / 2

        saturation = 0.0 if c_delta == 0 else (c_delta / (1 - abs(2 * lightness - 1)))

        return (hue, saturation, lightness)

    @property
    def hsv(self) -> tuple:
        """Three-tuple of float values: (hue, saturation, value)

        Hue is a float in [0, 359]
        Saturation is a float in [0,1]
        Lightness is a float in [0,1]
        """
        return self.hsl[:2] + (max(self.rgb_f),)

    @property
    def cmyk(self) -> tuple:
        """Four-tuple of float values: (cyan, magenta, yellow, black)
        
        Cyan is a float in [0, 1]
        Magenta is a float in [0, 1]
        Yellow is a float in [0, 1]
        Black is a float in [0, 1]
        """

        k = 1 - max(self.rgb_f)
        try:
            c = (1 - self.red.scale - k) / (1 - k)
            m = (1 - self.green.scale - k) / (1 - k)
            y = (1 - self.blue.scale - k) / (1 - k)
        except ZeroDivisionError:
            c, m, y = 0.0, 0.0, 0.0
        return (c, m, y, k)

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
