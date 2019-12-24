import pytest

from pyliter.color.value import Value8


@pytest.mark.parametrize("value", list(range(Value8.minimum, Value8.maximum)))
def test_create_rgba_value_8(value):
    v = Value8(value)
    assert v.value == value
    assert v.hex == f"{value:02x}"
    assert v.scale == round(value / Value8.maximum, 2)


@pytest.mark.parametrize("value", list(range(Value8.minimum, Value8.maximum)))
def test_create_value_from_hex_strings(value):
    hexstr = hex(value)
    a = Value8.from_hex_string(hexstr)
    b = Value8.from_hex_string(hexstr.replace("0x", "#"))
    c = Value8.from_hex_string(hexstr[2:])
    d = Value8.from_hex_string(hexstr.upper())
    e = Value8.from_hex_string(hexstr.upper().replace("0x", "#"))
    f = Value8.from_hex_string(hexstr.upper()[2:])

    assert a.value == value
    assert b.value == value
    assert c.value == value
    assert d.value == value
    assert e.value == value
    assert f.value == value


@pytest.mark.parametrize(
    "scale, expected",
    [
        (0, Value8.minimum),
        (1, Value8.maximum),
        (0.25, round(Value8.maximum / 4)),
        (0.5, round(Value8.maximum / 2)),
    ],
)
def test_create_value_from_scale(scale, expected):
    v = Value8.from_scale(scale)
    assert v.value == expected
    assert v.scale == scale


def test_create_value_from_byte_offset_into_word():

    word = int("aabbccdd", 16)
    v0 = Value8.from_byte_offset(word, 0)
    v1 = Value8.from_byte_offset(word, 1)
    v2 = Value8.from_byte_offset(word, 2)
    v3 = Value8.from_byte_offset(word, 3)
    assert v0.value == int("dd", 16) and v0.hex == "dd"
    assert v1.value == int("cc", 16) and v1.hex == "cc"
    assert v2.value == int("bb", 16) and v2.hex == "bb"
    assert v3.value == int("aa", 16) and v3.hex == "aa"


@pytest.mark.parametrize("offset", list(range(1, Value8.maximum)))
def test_create_value_out_of_range(offset):
    hi = Value8(Value8.maximum + offset)
    lo = Value8(Value8.minimum - offset)
    assert hi.value == Value8.maximum
    assert lo.value == Value8.minimum


@pytest.mark.parametrize("scale, expected", [(-1, 0), (-2.5, 0), (1.1, Value8.maximum)])
def test_create_from_scale_out_of_range(scale, expected):
    v = Value8.from_scale(scale)
    assert v.value == expected
