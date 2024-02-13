import json


# Color conversion utility functions
def rgb_to_hsl(rgb):
    """
    Converts RGB color format to HSL format.

    Args:
        rgb (tuple): RGB color tuple.

    Returns:
        tuple: HSL color tuple.
    """
    # Convert RGB values to a range of [0, 1]
    r, g, b = [x / 255.0 for x in rgb]
    # Determine the min and max RGB values
    max_color = max(r, g, b)
    min_color = min(r, g, b)
    # Calculate lightness
    l = (max_color + min_color) / 2

    # Calculate hue and saturation
    if max_color == min_color:
        h = s = 0  # achromatic
    else:
        d = max_color - min_color
        s = d / (2 - max_color - min_color) if l > 0.5 else d / (max_color + min_color)
        # Calculate hue based on which color is max
        if max_color == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif max_color == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4
        h /= 6

    return h, s, l


def hsl_to_rgb(hsl):
    """
    Converts HSL color format to RGB format.

    Args:
        hsl (tuple): HSL color tuple.

    Returns:
        tuple: RGB color tuple.
    """
    h, s, l = hsl

    def hue_to_rgb(p, q, t):
        """
        Helper function for converting hue to RGB.
        """
        if t < 0:
            t += 1
        if t > 1:
            t -= 1
        if t < 1 / 6:
            return p + (q - p) * 6 * t
        if t < 1 / 2:
            return q
        if t < 2 / 3:
            return p + (q - p) * (2 / 3 - t) * 6
        return p

    # Calculate RGB values from HSL
    if s == 0:
        r = g = b = l  # achromatic
    else:
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = hue_to_rgb(p, q, h + 1 / 3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1 / 3)

    return int(r * 255), int(g * 255), int(b * 255)


def rgb_to_hex(rgb):
    """
    Converts RGB color format to Hex format.

    Args:
        rgb (tuple): RGB color tuple.

    Returns:
        str: Hex color string.
    """
    return "#{:02x}{:02x}{:02x}".format(*rgb)


import json


def generate_individual_shade_svg(base_color, color_name, shade_values):
    base_color_rgb = tuple(int(base_color[i : i + 2], 16) for i in (0, 2, 4))
    base_color_hsl = rgb_to_hsl(base_color_rgb)

    shades_dict = {}
    svg_elements = []
    elements_per_row = 10
    row_width = (
        120 * elements_per_row
    )  # Adjusted for clarity but not directly used due to fixed element size and spacing
    x_offset = 0
    y_offset = 20  # Start with an offset to accommodate the color group name

    # Add the color group name at the top
    group_name_svg = f'<text x="0" y="15" fill="black" font-size="14" font-family="Arial" text-anchor="start">{color_name.capitalize()}</text>'
    svg_elements.append(group_name_svg)

    for index, shade in enumerate(shade_values):
        if index % elements_per_row == 0 and index != 0:
            x_offset = 0  # Reset x offset for a new row
            y_offset += 100  # Move down for the next row of elements

        new_hsl = (base_color_hsl[0], base_color_hsl[1], shade / 100)
        new_rgb = hsl_to_rgb(new_hsl)
        new_hex = rgb_to_hex(new_rgb)

        # SVG element for the shade
        svg_code = f"""
        <rect id="{color_name}/{shade*10}" width="100" height="50" fill="{new_hex}" x="{x_offset}" y="{y_offset}" rx="8" ry="8"/>
        <text x="{x_offset + 50}" y="{y_offset + 65}" fill="black" font-size="8" font-family="Arial" text-anchor="middle">Shade: {shade*10}</text>
        <text x="{x_offset + 50}" y="{y_offset + 80}" fill="black" font-size="8" font-family="Arial" text-anchor="middle">Hex: {new_hex}</text>
        """

        shade_key = f"{color_name}-{shade*10}"
        shades_dict[shade_key] = new_hex
        svg_elements.append(f'<g id="{shade_key}">{svg_code}</g>')

        x_offset += 120  # Move right for the next element in the row

    return (
        shades_dict,
        svg_elements,
        y_offset
        + 100,  # Return y_offset for the next color group, including space for the name
    )


# The rest of the processing code remains the same


# Color conversion utility functions remain the same

# Define base colors and shade values
colors = {
    "grey": "6B7280",
    "grey-variant": "6d8691",
    "error": "f75555",
    "primary": "ffc800",
    "secondary": "B523FA",
    "tertiary": "EC6890",
}
shade_values = [
    0,
    2,
    4,
    6,
    8,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    22,
    24,
    26,
    28,
    30,
    35,
    40,
    45,
    50,
    55,
    60,
    65,
    70,
    75,
    80,
    81,
    82,
    83,
    84,
    85,
    86,
    87,
    88,
    89,
    90,
    91,
    92,
    93,
    94,
    95,
    96,
    97,
    98,
    99,
    100,
]

all_shades_dict = {}
final_svg_elements = []
group_y_offset = 0  # Initialize y offset for positioning color groups vertically

# Generate SVG elements for each shade of each color
for color_name, base_color_hex in colors.items():
    shades_dict, svg_elements, updated_y_offset = generate_individual_shade_svg(
        base_color_hex, color_name, shade_values
    )
    all_shades_dict.update(shades_dict)

    # Group SVG elements for the current color with updated vertical positioning
    color_group = "\n".join(svg_elements)
    final_svg_elements.append(
        f'<g id="{color_name}-group" transform="translate(0, {group_y_offset})">{color_group}</g>'
    )

    group_y_offset += updated_y_offset + 50  # Update group_y_offset for the next group

# Combine all grouped SVG elements into the final SVG container
final_svg_code = (
    f'<svg id="color-shades" xmlns="http://www.w3.org/2000/svg" width="{1180}" height="{group_y_offset}" style="overflow: visible;">\n'
    + "\n".join(final_svg_elements)
    + "\n</svg>"
)

# Save the SVG code and shades dictionary
with open("primitive_colors/primitive_colors.svg", "w") as f:
    f.write(final_svg_code)

with open("primitive_colors/primitive_colors_map.json", "w") as f:
    json.dump(all_shades_dict, f, indent=4)

print("Generated SVG saved to color_shades.svg")
print("Generated color shades dictionary saved to color_map.json")
