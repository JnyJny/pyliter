"""
"""

from enum import IntEnum


class ValueRange(IntEnum):
    min: int
    max: int

    @classmethod
    def clamp(cls, value: int) -> int:
        return int(min(cls.max, max(value, cls.min)))

    @classmethod
    def scale(cls, value: float) -> int:
        return cls.clamp(round(cls.max * value))


class ValueRange8(ValueRange):
    min: int = 0
    max: int = 0xF


class ValueRange16(ValueRange):
    min: int = 0
    max: int = 0xFF
