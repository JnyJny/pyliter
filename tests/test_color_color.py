import pytest
import pyliter.color

m = pyliter.color.value.Value8.minimum
M = pyliter.color.value.Value8.maximum
h = round(M / 2)

palette = [
    # RGBA, hex, scaled, HSL, HSV, CMYK, NAME
    (
        (M, m, m, M),
        "#ff0000ff",
        (1.0, 0.0, 0.0, 1.0),
        (0, 1.0, 0.5),
        (0, 1.0, 1.0),
        (0, 1, 1, 0),
        "red",
    ),
    (
        (M, m, m, m),
        "#ff000000",
        (1.0, 0.0, 0.0, 0.0),
        (0, 1.0, 0.5),
        (0, 1.0, 1.0),
        (0, 1, 1, 0),
        "red",
    ),
    (
        (m, h, m, M),
        "#008000ff",
        (0.0, 0.5, 0.0, 1.0),
        (120, 1.0, 0.25),
        (120, 1.0, 0.5),
        (1, 0, 1, 0.5),
        "green",
    ),
    (
        (m, h, m, m),
        "#00800000",
        (0.0, 0.5, 0.0, 0.0),
        (120, 1.0, 0.25),
        (120, 1.0, 0.5),
        (1, 0, 1, 0.5),
        "green",
    ),
    (
        (m, M, m, M),
        "#00ff00ff",
        (0.0, 1.0, 0.0, 1.0),
        (120, 1.0, 0.5),
        (120, 1.0, 1.0),
        (1, 0, 1, 0),
        "lime",
    ),
    (
        (m, M, m, m),
        "#00ff0000",
        (0.0, 1.0, 0.0, 0.0),
        (120, 1.0, 0.5),
        (120, 1.0, 1.0),
        (1, 0, 1, 0),
        "lime",
    ),
    (
        (m, m, M, M),
        "#0000ffff",
        (0.0, 0.0, 1.0, 1.0),
        (240, 1.0, 0.5),
        (240, 1.0, 1.0),
        (1, 1, 0, 0),
        "blue",
    ),
    (
        (m, m, M, m),
        "#0000ff00",
        (0.0, 0.0, 1.0, 0.0),
        (240, 1.0, 0.5),
        (240, 1.0, 1.0),
        (1, 1, 0, 0),
        "blue",
    ),
    (
        (M, M, M, M),
        "#ffffffff",
        (1.0, 1.0, 1.0, 1.0),
        (0, 0.0, 1.0),
        (0, 0, 1.0),
        (0, 0, 0, 0),
        "white",
    ),
    (
        (M, M, M, m),
        "#ffffff00",
        (1.0, 1.0, 1.0, 0.0),
        (0, 0.0, 1.0),
        (0, 0.0, 1.0),
        (0, 0, 0, 0),
        "white",
    ),
    (
        (m, m, m, M),
        "#000000ff",
        (0.0, 0.0, 0.0, 1.0),
        (0, 0.0, 0.0),
        (0, 0, 0),
        (0, 0, 0, 1),
        "black",
    ),
    (
        (m, m, m, m),
        "#00000000",
        (0.0, 0.0, 0.0, 0.0),
        (0, 0.0, 0.0),
        (0, 0, 0),
        (0, 0, 0, 1),
        "black",
    ),
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


@pytest.mark.parametrize(
    "rgba_values, hex_string, float_values, hsl_values, hsv_values, cmyk_values, name",
    palette,
)
def test_create_color(
    rgba_values, hex_string, float_values, hsl_values, hsv_values, cmyk_values, name
):
    """Create Color with (red,green,blue,alpha) 4-tuples.
    """
    color = pyliter.color.Color(*rgba_values)
    assert color.rgba == rgba_values
    assert color.hex == hex_string
    assert color.name == name
    assert color.rgba_f == float_values
    assert color.hsl == hsl_values
    assert color.hsv == hsv_values
    assert color.cmyk == cmyk_values
    assert hash(color) == int(hex_string[1:], 16)


@pytest.mark.parametrize(
    "rgba_values, hex_string, float_values, hsl_values, hsv_values, cmyk_values, name",
    palette,
)
def test_create_color_from_name(
    rgba_values, hex_string, float_values, hsl_values, hsv_values, cmyk_values, name
):
    """Create Color colors by name. 
    """
    color = pyliter.color.Color.from_name(name, alpha=rgba_values[3])
    assert color.rgba == rgba_values
    assert color.hex == hex_string
    assert color.name == name
    assert color.rgba_f == float_values
    assert color.hsl == hsl_values
    assert color.hsv == hsv_values
    assert color.cmyk == cmyk_values
    assert hash(color) == int(hex_string[1:], 16)


@pytest.mark.parametrize(
    "rgba_values, hex_string, float_values, hsl_values, hsv_values, cmyk_values, name",
    palette,
)
def test_create_color_from_hex_string(
    rgba_values, hex_string, float_values, hsl_values, hsv_values, cmyk_values, name
):
    """Create Color colors with a string of eight hex digits with a octothorpe prefix.
    """
    color = pyliter.color.Color.from_hex_string(hex_string)
    assert color.rgba == rgba_values
    assert color.hex == hex_string
    assert color.name == name
    assert color.rgba_f == float_values
    assert color.hsl == hsl_values
    assert color.hsv == hsv_values
    assert color.cmyk == cmyk_values
    assert hash(color) == int(hex_string[1:], 16)


@pytest.mark.parametrize(
    "rgba_values, hex_string, float_values, hsl_values, hsv_values, cmyk_values, name",
    palette,
)
def test_create_color_from_value(
    rgba_values, hex_string, float_values, hsl_values, hsv_values, cmyk_values, name
):
    """Create Color color using a 32-bit integer value.
    """
    color = pyliter.color.Color.from_value(int(hex_string[1:], 16))
    assert color.rgba == rgba_values
    assert color.hex == hex_string
    assert color.name == name
    assert color.rgba_f == float_values
    assert color.hsl == hsl_values
    assert color.hsv == hsv_values
    assert color.cmyk == cmyk_values
    assert hash(color) == int(hex_string[1:], 16)


@pytest.mark.parametrize(
    "rgba_values, hex_string, float_values, hsl_values, hsv_values, cmyk_values, name",
    palette,
)
def test_create_color_from_scale(
    rgba_values, hex_string, float_values, hsl_values, hsv_values, cmyk_values, name
):
    """Create colors specifying red, green, blue and alpha channels with a floating
    point number between 0.0 and 1.0 inclusive. Ensure that the resulting color is
    consistent.
    """
    color = pyliter.color.Color.from_scale(*float_values)
    assert color.rgba == rgba_values
    assert color.hex == hex_string
    assert color.name == name
    assert color.rgba_f == float_values
    assert color.hsl == hsl_values
    assert color.hsv == hsv_values
    assert color.cmyk == cmyk_values
    assert hash(color) == int(hex_string[1:], 16)


@pytest.mark.parametrize(
    "rgba_values, hex_string, float_values, hsl_values, hsv_values, cmyk_values, name",
    palette,
)
def test_create_color_from_hsl(
    rgba_values, hex_string, float_values, hsl_values, hsv_values, cmyk_values, name
):
    """Create colors using HSL; hue, saturation, and lightness values and ensure that
    the result color is consistent.
    """
    color = pyliter.color.Color.from_hsl(*hsl_values, float_values[-1])
    assert color.rgba == rgba_values
    assert color.hex == hex_string
    assert color.name == name
    assert color.rgba_f == float_values
    assert color.hsl == hsl_values
    assert color.hsv == hsv_values
    assert color.cmyk == cmyk_values
    assert hash(color) == int(hex_string[1:], 16)


@pytest.mark.parametrize(
    "rgba_values, hex_string, float_values, hsl_values, hsv_values, cmyk_values, name",
    palette,
)
def test_create_color_from_hsv(
    rgba_values, hex_string, float_values, hsl_values, hsv_values, cmyk_values, name
):
    """Create colors using HSL; hue, saturation, and lightness values and ensure that
    the result color is consistent.
    """
    color = pyliter.color.Color.from_hsv(*hsv_values, float_values[-1])
    assert color.rgba == rgba_values
    assert color.hex == hex_string
    assert color.name == name
    assert color.rgba_f == float_values
    assert color.hsl == hsl_values
    assert color.hsv == hsv_values
    assert color.cmyk == cmyk_values
    assert hash(color) == int(hex_string[1:], 16)


@pytest.mark.parametrize(
    "rgba_values, hex_string, float_values, hsl_values, hsv_values, cmyk_values, name",
    palette,
)
def test_create_color_from_cmyk(
    rgba_values, hex_string, float_values, hsl_values, hsv_values, cmyk_values, name
):
    """Create colors using HSL; hue, saturation, and lightness values and ensure that
    the result color is consistent.
    """
    color = pyliter.color.Color.from_cmyk(*cmyk_values, float_values[-1])
    assert color.rgba == rgba_values
    assert color.hex == hex_string
    assert color.name == name
    assert color.rgba_f == float_values
    assert color.hsl == hsl_values
    assert color.hsv == hsv_values
    assert color.cmyk == cmyk_values
    assert hash(color) == int(hex_string[1:], 16)


@pytest.mark.parametrize(
    "hsl_values, expected",
    [
        ((720, 0.0, 0.0), (0, 0.0, 0.0)),
        ((-180, 0.0, 0.0), (0, 0.0, 0.0)),
        ((0, -1.0, 0.0), (0, 0.0, 0.0)),
        ((0, 0.0, 2.0), (0, 0.0, 1.0)),
        ((0, 2.0, 0.5), (0, 1.0, 0.5)),
        ((0, -2.0, 0.5), (0, 0.0, 0.5)),
    ],
)
def test_create_color_from_hsl_with_out_of_range_values(hsl_values, expected):
    """Check to make sure HSL value ranges are enforced.
    """
    color = pyliter.color.Color.from_hsl(*hsl_values)
    assert color.hsl == expected


@pytest.mark.parametrize("hex_string, expected", mutated_hex_strings)
def test_create_color_with_mutating_short_hex_strings(hex_string, expected):
    """Checks that creating a color with a short 4-bit RGB/RGBA strings results
    in an 8-bit scaled version of the color.
    """
    color = pyliter.color.Color.from_hex_string(hex_string)
    assert color.hex == expected


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
    """Check that hex strings with or without prefixes ('#' and '0x') createes
    the expected color.
    """
    color = pyliter.color.Color.from_hex_string(hex_string)
    assert color.hex == expected


@pytest.mark.parametrize("value, expected", [(256, M), (-1, m)])
def test_color_argument_outside_of_range(value, expected):
    """Create a color with values greater than 255 and less than 0
    and check that they get clamped to the maximum or minimum
    accordlingly.
    """
    color = pyliter.color.Color(value, value, value, value)
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
        color = pyliter.color.Color.from_hex_string(hex_string)


def test_color_not_found():
    """Make sure unknown colors raise ColorNameNotFound exception.
    """
    with pytest.raises(pyliter.color.ColorNameNotFound):
        color = pyliter.color.Color.from_name("mojojojo fruit salad")


def test_color_to_dict():
    """Make sure Color.as_dict returns a dictionary with
    the expected keys and values.
    """
    color = pyliter.color.Color(11, 22, 33, 44)
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


@pytest.mark.parametrize("name, rgb_values", list(pyliter.color.COLORS_BY_NAME.items()))
def test_all_colors_in_the_catalog_by_name(name, rgb_values):
    """Create all the colors in the catalog by name. 
    """
    c = pyliter.color.Color.from_name(name)
    assert c.rgb == rgb_values
    assert c.name in pyliter.color.COLORS_BY_NAME


@pytest.mark.parametrize("name, rgb_values", list(pyliter.color.COLORS_BY_NAME.items()))
def test_all_colors_in_the_catalog_by_upper_case_name(name, rgb_values):
    """Create all the colors in the catalog by uppercase name. 
    """
    c = pyliter.color.Color.from_name(name.upper())
    assert c.rgb == rgb_values
    assert c.name in pyliter.color.COLORS_BY_NAME


@pytest.mark.parametrize("name, rgb_values", list(pyliter.color.COLORS_BY_NAME.items()))
def test_all_colors_in_the_catalog_by_lower_case_name(name, rgb_values):
    """Create all the colors in the catalog by uppercase name. 
    """
    c = pyliter.color.Color.from_name(name.lower())
    assert c.rgb == rgb_values
    assert c.name in pyliter.color.COLORS_BY_NAME


@pytest.mark.parametrize("name, rgb_values", list(pyliter.color.COLORS_BY_NAME.items()))
def test_all_colors_in_the_catalog_with_goofed_up_name(name, rgb_values):
    """Create all the colors in the catalog by uppercase name. 
    """
    goofed_a = "".join(
        sum([[a, b] for a, b in zip(list(name.title()), [" "] * len(name))], [])
    )

    goofed_b = goofed_a.replace(" ", "\t")
    goofed_c = goofed_a.replace(" ", "\n")
    goofed_d = goofed_a.replace(" ", "\r")

    for goofed in [goofed_a, goofed_b, goofed_c, goofed_d]:
        c = pyliter.color.Color.from_name(goofed)
        assert c.rgb == rgb_values
        assert c.name in pyliter.color.COLORS_BY_NAME


@pytest.mark.parametrize("name, rgb_values", list(pyliter.color.COLORS_BY_NAME.items()))
def test_all_colors_in_the_catalog_by_value(name, rgb_values):
    """Create all the colors in the catalog by RGB values.
    """
    c = pyliter.color.Color(*rgb_values)
    assert c.name in pyliter.color.COLORS_BY_NAME
    assert c.rgb == rgb_values


@pytest.mark.parametrize("args", [[], [0], [0, 0]])
def test_creating_with_missing_arguments(args):
    """Check that Color.__init__ raises TypeError when it
    recieves less than 3 arguments.
    """
    with pytest.raises(TypeError):
        c = pyliter.color.Color(*args)


def test_color_repr():

    c = pyliter.color.Color(0, 0, 0)
    assert isinstance(repr(c), str)


def test_color_equality():
    black = pyliter.color.Color(0, 0, 0)
    white = pyliter.color.Color(255, 255, 255)

    assert black.name == "black"
    assert white.name == "white"

    assert black != white
    assert black is not white
    assert black == pyliter.color.Color(0, 0, 0)
    assert white == pyliter.color.Color(255, 255, 255)


@pytest.mark.parametrize("target", [None, 0, "foo", {}, [], set()])
def test_color_comparisons(target):

    foo = pyliter.color.Color(0, 0, 0)
    bar = pyliter.color.Color(255, 255, 255)

    with pytest.raises(AttributeError):
        assert foo == target

    with pytest.raises(AttributeError):
        assert foo < target

    with pytest.raises(AttributeError):
        assert foo <= target

    with pytest.raises(AttributeError):
        assert foo > target

    with pytest.raises(AttributeError):
        assert foo >= target

    assert foo != bar
    assert foo == foo
    assert foo < bar
    assert bar > foo
    assert foo <= bar
    assert bar >= foo
