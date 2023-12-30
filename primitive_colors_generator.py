import json
def generate_shades_and_svg(base_color, color_name, shade_values):
    """
    Generates a dictionary of color shades and an SVG representation for a given base color.
    Each color shade is represented as a rectangle in the SVG, and the hex code is displayed as text.
    
    Args:
        base_color (str): The base color in hexadecimal format (e.g., 'FF5733').
        color_name (str): The descriptive name of the color (used as an identifier in the SVG).
        shade_values (list of int): The percentages of the base color shades to generate.

    Returns:
        dict: A dictionary of shades with their hex values.
        str: An SVG string representation of the color shades.
    """
    # Convert hex to RGB and then to HSL
    base_color_rgb = tuple(int(base_color[i:i+2], 16) for i in (0, 2, 4))
    base_color_hsl = rgb_to_hsl(base_color_rgb)

    # Initialize lists for rectangles and labels, and the shades dictionary
    rectangles = []
    labels = []
    shades_dict = {}

    # Define SVG properties
    svg_width = 108 * len(shade_values)
    svg_height = 120  # Fixed height for each color shade row

    # Generate shades and SVG elements for each shade
    for i, shade in enumerate(sorted(shade_values)):
        # Calculate the new shade color
        new_hsl = (base_color_hsl[0], base_color_hsl[1], shade / 100)
        new_rgb = hsl_to_rgb(new_hsl)
        new_hex = rgb_to_hex(new_rgb)
        
        # Update the shades dictionary with the calculated color
        shade_key = f'{color_name}-{shade * 10}'
        shades_dict[shade_key] = new_hex

        # Calculate the x position for the rectangle and label
        x_position = 108 * i

        # Append the rectangle SVG element to the rectangles list
        rectangles.append(f'<rect id="{shade_key}" width="100" height="100" fill="{new_hex}" x="{x_position}" y="0"/>')

        # Append the text SVG element to the labels list
        labels.append(f'<text x="{x_position + 10}" y="50" fill="white" font-size="10" font-family="Arial" alignment-baseline="middle">{new_hex}</text>')

    # Combine all rectangles and labels to form the final SVG string
    svg_code = (
        f'<svg id="{color_name}-shades" width="{svg_width}" height="{svg_height}" '
        f'viewBox="0 0 {svg_width} {svg_height}" xmlns="http://www.w3.org/2000/svg">\n'
        + '\n'.join(rectangles) + '\n' + '\n'.join(labels) +
        '\n</svg>'
    )

    return shades_dict, svg_code


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
        if t < 0: t += 1
        if t > 1: t -= 1
        if t < 1/6: return p + (q - p) * 6 * t
        if t < 1/2: return q
        if t < 2/3: return p + (q - p) * (2/3 - t) * 6
        return p

    # Calculate RGB values from HSL
    if s == 0:
        r = g = b = l  # achromatic
    else:
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = hue_to_rgb(p, q, h + 1/3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1/3)

    return int(r * 255), int(g * 255), int(b * 255)

def rgb_to_hex(rgb):
    """
    Converts RGB color format to Hex format.

    Args:
        rgb (tuple): RGB color tuple.

    Returns:
        str: Hex color string.
    """
    return '#{:02x}{:02x}{:02x}'.format(*rgb)


# Uncomment this for user input
# User inputs for multiple colors
# colors = {
#     "primary": input("Enter the primary color in hex (e.g., 'DA2C24'): "),
#     "secondary": input("Enter the secondary color in hex (e.g., '4B88A2'): "),
#     "tertiary": input("Enter the tertiary color in hex (e.g., 'A1D68B'): "),
#     "error": input("Enter the error color in hex (e.g., 'FF0000'): "),
#     "grey": input("Enter the grey color in hex (e.g., '808080'): "),
#     "grey_variant": input("Enter the grey variant color in hex (e.g., 'BEBEBE'): ")
# }

# Define base colors and shade values
colors = {
    "grey": "7f7a84",
    "grey-variant": "6d8691",
    "error": "da2c24",
    "primary": "ffc800",
    "secondary": "00ffc6",
    "tertiary": 'ff7700',
}
shade_values = [0,4,6,10,12,17,20,22,24,30,40,50,60,70,80,87,90,92,94,95,96,98,100]
# Initialize the SVG container
svg_height = 120 * len(colors)
final_svg_code = f'<svg id="primitive-colors" width="{108 * len(shade_values)}" height="{120 * len(colors)}" style="display: inline-flex; flex-direction: column; align-items: flex-start;" xmlns="http://www.w3.org/2000/svg">\n'

# Initialize a dictionary to store all shades
all_shades_dict = {}

# Generate shades and SVG for each color and append them to the SVG container
y_offset = 0
for color_name, base_color_hex in colors.items():
    shades_dict, svg_code = generate_shades_and_svg(base_color_hex, color_name, shade_values)
    all_shades_dict.update(shades_dict)
    # Append the SVG code for this color to the final SVG container
    final_svg_code += f'<g id="{color_name}" transform="translate(0, {y_offset})">{svg_code}</g>\n'
    y_offset += 120  # Increment the y_offset for the next color group

# Close the SVG container
final_svg_code += '</svg>'

# Save the SVG code to a file
with open('shade.svg', 'w') as f:
    f.write(final_svg_code)

# Save the shades dictionary as a JSON file
with open('color_map/color_map.json', 'w') as f:
    json.dump(all_shades_dict, f, indent=4)

# Output paths of the generated files
print('Generated SVG saved to color_shades.svg')
print('Generated color shades dictionary saved to color_shades.json')

