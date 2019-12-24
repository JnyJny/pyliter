import pytest

import pyliter.color

MIN = pyliter.color.value.Value8.minimum
MAX = pyliter.color.value.Value8.maximum
HLF = round(MAX / 2)

palette = [
    ((MAX, MIN, MIN, MAX), "#ff0000ff", (1.0, 0.0, 0.0, 1.0), "red"),
    ((MAX, MIN, MIN, MIN), "#ff000000", (1.0, 0.0, 0.0, 0.0), "red"),
    ((MIN, HLF, MIN, MAX), "#008000ff", (0.0, 0.5, 0.0, 1.0), "green"),
    ((MIN, HLF, MIN, MIN), "#00800000", (0.0, 0.5, 0.0, 0.0), "green"),
    ((MIN, MAX, MIN, MAX), "#00ff00ff", (0.0, 1.0, 0.0, 1.0), "lime"),
    ((MIN, MAX, MIN, MIN), "#00ff0000", (0.0, 1.0, 0.0, 0.0), "lime"),
    ((MIN, MIN, MAX, MAX), "#0000ffff", (0.0, 0.0, 1.0, 1.0), "blue"),
    ((MIN, MIN, MAX, MIN), "#0000ff00", (0.0, 0.0, 1.0, 0.0), "blue"),
    ((MAX, MAX, MAX, MAX), "#ffffffff", (1.0, 1.0, 1.0, 1.0), "white"),
    ((MAX, MAX, MAX, MIN), "#ffffff00", (1.0, 1.0, 1.0, 0.0), "white"),
    ((MIN, MIN, MIN, MAX), "#000000ff", (0.0, 0.0, 0.0, 1.0), "black"),
    ((MIN, MIN, MIN, MIN), "#00000000", (0.0, 0.0, 0.0, 0.0), "black"),
]

mutated_hex_strings = [
    ("#000", "#000000ff"),
    ("#000f", "#000000ff"),
    ("#0000", "#00000000"),
    ("#f00", "#ff0000ff"),
    ("#f00f", "#ff0000ff"),
    ("#f000", "#ff000000"),
    ("#001", "#000011ff"),
    ("#002", "#000022ff"),
    ("#003", "#000033ff"),
    ("#004", "#000044ff"),
    ("#005", "#000055ff"),
    ("#006", "#000066ff"),
    ("#007", "#000077ff"),
    ("#008", "#000088ff"),
    ("#009", "#000099ff"),
    ("#00a", "#0000aaff"),
    ("#00b", "#0000bbff"),
    ("#00c", "#0000ccff"),
    ("#00d", "#0000ddff"),
    ("#00e", "#0000eeff"),
    ("#00f", "#0000ffff"),
    ("#010", "#001100ff"),
    ("#020", "#002200ff"),
    ("#030", "#003300ff"),
    ("#040", "#004400ff"),
    ("#050", "#005500ff"),
    ("#060", "#006600ff"),
    ("#070", "#007700ff"),
    ("#080", "#008800ff"),
    ("#090", "#009900ff"),
    ("#0a0", "#00aa00ff"),
    ("#0b0", "#00bb00ff"),
    ("#0c0", "#00cc00ff"),
    ("#0d0", "#00dd00ff"),
    ("#0e0", "#00ee00ff"),
    ("#f00", "#ff0000ff"),
    ("#100", "#110000ff"),
    ("#200", "#220000ff"),
    ("#300", "#330000ff"),
    ("#400", "#440000ff"),
    ("#500", "#550000ff"),
    ("#600", "#660000ff"),
    ("#700", "#770000ff"),
    ("#800", "#880000ff"),
    ("#900", "#990000ff"),
    ("#a00", "#aa0000ff"),
    ("#b00", "#bb0000ff"),
    ("#c00", "#cc0000ff"),
    ("#d00", "#dd0000ff"),
    ("#e00", "#ee0000ff"),
    ("#f00", "#ff0000ff"),
]


@pytest.mark.parametrize("rgba_values, hex_string, float_values, name", palette)
def test_create_color(rgba_values, hex_string, float_values, name):
    """Create RGBA colors with (red,green,blue,alpha) 4-tuples.
    """
    color = pyliter.color.RGBAColor32(*rgba_values)
    assert color.rgba == rgba_values
    assert color.hex == hex_string
    assert color.name == name
    assert color.rgba_f == float_values


@pytest.mark.parametrize("rgba_values, hex_string, float_values, name", palette)
def test_create_color_from_name(rgba_values, hex_string, float_values, name):
    """Create RGBAColor32 colors by name. 
    """
    color = pyliter.color.RGBAColor32.from_name(name, alpha=rgba_values[3])
    assert color.rgba == rgba_values
    assert color.hex == hex_string
    assert color.name == name
    assert color.rgba_f == float_values


@pytest.mark.parametrize("rgba_values, hex_string, float_values, name", palette)
def test_create_color_from_hex_string(rgba_values, hex_string, float_values, name):
    """Create RGBAColor32 colors with a string of eight hex digits with a octothorpe prefix.
    """
    color = pyliter.color.RGBAColor32.from_hex_string(hex_string)
    assert color.rgba == rgba_values
    assert color.hex == hex_string
    assert color.name == name
    assert color.rgba_f == float_values


@pytest.mark.parametrize("rgba_values, hex_string, float_values, name", palette)
def test_create_color_from_value(rgba_values, hex_string, float_values, name):
    """Create RGBAColor32 colors with a string of eight hex digits with a octothorpe prefix.
    """
    color = pyliter.color.RGBAColor32.from_value(int(hex_string[1:], 16))
    assert color.rgba == rgba_values
    assert color.hex == hex_string
    assert color.name == name
    assert color.rgba_f == float_values


@pytest.mark.parametrize("rgba_values, hex_string, float_values, name", palette)
def test_create_color_from_scale(rgba_values, hex_string, float_values, name):
    color = pyliter.color.RGBAColor32.from_scale(*float_values)
    assert color.rgba == rgba_values
    assert color.hex == hex_string
    assert color.name == name
    assert color.rgba_f == float_values


@pytest.mark.parametrize("hex_string, expected", mutated_hex_strings)
def test_create_color_with_mutating_short_hex_strings(hex_string, expected):
    color = pyliter.color.RGBAColor32.from_hex_string(hex_string)
    assert color.hex == expected


@pytest.mark.parametrize("unused, hex_string", mutated_hex_strings)
def test_create_color_with_mutating_long_hex_values(unused, hex_string):
    color = pyliter.color.RGBAColor32.from_value(int(hex_string[1:], 16))
    assert color.hex == hex_string


@pytest.mark.parametrize(
    "hex_string, expected",
    [
        ("#aabbccdd", "#aabbccdd"),
        ("#AABBCCDD", "#aabbccdd"),
        ("aabbccdd", "#aabbccdd"),
        ("AABBCCDD", "#aabbccdd"),
        ("0xaabbccdd", "#aabbccdd"),
        ("0xAABBCCDD", "#aabbccdd"),
    ],
)
def test_create_color_with_different_hex_string_prefixes_and_case(hex_string, expected):
    color = pyliter.color.RGBAColor32.from_hex_string(hex_string)
    assert color.hex == expected


@pytest.mark.parametrize("value, expected", [(256, MAX), (-1, MIN)])
def test_color_argument_outside_of_range(value, expected):
    color = pyliter.color.RGBAColor32(value, value, value, value)
    assert color.rgba == (expected, expected, expected, expected)


@pytest.mark.parametrize(
    "hex_string",
    [
        None,
        0xFFAABBCC,
        0.1,
        [],
        {},
        (),
        "foobar",
        "f",
        "f" * 2,
        "f" * 5,
        "f" * 7,
        "f" * 9,
    ],
)
def test_create_color_with_invalid_hex_strings(hex_string):
    """Make sure invalid hex strings raise ValueError.
    """
    with pytest.raises(ValueError):
        color = pyliter.color.RGBAColor32.from_hex_string(hex_string)


def test_color_not_found():
    """Make sure unknown colors raise ColorNameNotFound exception.
    """
    with pytest.raises(pyliter.color.ColorNameNotFound):
        color = pyliter.color.RGBAColor32.from_name("mojojojo fruit salad")


def test_color_to_dict():
    """Make sure RGBAColor32.as_dict returns a dictionary with
    the expected keys and values.
    """
    color = pyliter.color.RGBAColor32(11, 22, 33, 44)
    info = color.as_dict()

    assert isinstance(info, dict)
    assert sorted(list(info.keys())) == sorted(
        ["name", "red", "green", "blue", "alpha"]
    )

    assert info["name"] == "unnamed"
    assert info["red"] == 11
    assert info["green"] == 22
    assert info["blue"] == 33
    assert info["alpha"] == 44
