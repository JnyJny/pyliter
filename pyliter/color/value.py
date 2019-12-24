"""
"""


class Value0:
    minimum = 0
    maximum = 0

    @classmethod
    def from_hex_string(cls, hex_string):
        """
        """
        if hex_string.startswith("#"):
            hex_string = hex_string[1:]
        if hex_string.startswith("0x"):
            hex_string = hex_string[2:]
        return cls(int(hex_string, 16))

    @classmethod
    def from_scale(cls, scale_value):
        return cls(round(cls.maximum * scale_value))

    @classmethod
    def from_byte_offset(cls, value: int, byte_index=0):
        print("MAX", cls.maximum, cls.__name__)
        byte_value = (value >> (byte_index * 8)) & cls.maximum
        return cls(byte_value)

    def __init__(self, value: int):
        self.value = value

    def __repr__(self):
        return f"{self.__class__.__name__}(value=0x{self.hex})"

    def __str__(self) -> str:
        return self.hex

    @property
    def hex(self) -> str:
        return f"{self.value:02x}"

    @property
    def value(self):
        try:
            return self._value
        except AttributeError:
            pass
        self._value = 0
        return self._value

    @value.setter
    def value(self, value):
        self._value = min(self.maximum, max(value, self.minimum))

    @property
    def scale(self) -> float:
        return round(self.value / self.maximum, 2)


class Value8(Value0):
    maximum = (1 << 8) - 1


class Value16(Value0):
    maximum = (1 << 16) - 1
