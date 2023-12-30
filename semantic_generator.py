import json

# Function to load JSON data from a file
def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Load the color map, light theme, and dark theme from JSON files
color_map = load_json('color_map/color_map.json')
light_theme = load_json('meterial_semantic/light_theme_semantic.json')
dark_theme = load_json('meterial_semantic/dark_theme_semantic.json')

def create_svg_element(color_code, name, color_map, color_shade_name):
    fill_color = color_map.get(color_code, '#FFFFFF')
    # Create SVG content without the 'name' label text
    svg_content = f'<svg id="{name}" width="300" height="50" xmlns="http://www.w3.org/2000/svg">' \
                  f'<rect id="{name}" width="60" height="60" fill="{fill_color}" />' \
                  f'<rect id="primitive-{color_shade_name}" width="65" height="65" fill="{fill_color}" />' \
                  f'<text x="60" y="30" fill="black">{name}: {fill_color}</text>' \
                  f'</svg>'
    return svg_content

# Function to group SVGs into named categories
def group_svgs_by_theme_and_category(light_svgs, dark_svgs):
    themes = {
        "light": {
            "primary": [],
            "secondary": [],
            "tertiary": [],
            "error": [],
            "surface": [],
            "other": []
        },
        "dark": {
            "primary": [],
            "secondary": [],
            "tertiary": [],
            "error": [],
            "surface": [],
            "other": []
        }
    }

    # Helper function to determine the category
    def get_category(name):
        for category in themes["light"]:
            if category in name:
                return category
        return "other"

    # Group light theme SVGs
    for name, svg_content in light_svgs.items():
        category = get_category(name)
        themes["light"][category].append((name, svg_content))

    # Group dark theme SVGs
    for name, svg_content in dark_svgs.items():
        category = get_category(name)
        themes["dark"][category].append((name, svg_content))

    return themes

def create_svg_dynamic_for_figma(color_map, theme):
    theme_svgs = {}
    for key, value in theme.items():
        color_shade_name = f'{value}'[:value.rfind('-')] + '/' + f'{value}'[value.rfind('-')+1:]
        theme_svgs[key] = create_svg_element(value, key, color_map, color_shade_name)
    return theme_svgs

# Generate SVGs for light and dark themes
light_theme_svgs = create_svg_dynamic_for_figma(color_map, light_theme)
dark_theme_svgs = create_svg_dynamic_for_figma(color_map, dark_theme)

# Group all SVGs by theme and then by category
categorized_svgs = group_svgs_by_theme_and_category(light_theme_svgs, dark_theme_svgs)

# Function to group all SVGs into a single container with separate groups for each theme and category
def group_svgs_into_semantics_container(categorized_svgs):
    svg_container = '<svg id="semantics" xmlns="http://www.w3.org/2000/svg">'
    y_offset = 0

    for theme, categories in categorized_svgs.items():
        svg_container += f'<g id="{theme}">'
        for category, svgs in categories.items():
            svg_container += f'<g id="{theme}/{category}">'
            for name, svg_content in svgs:
                # Extract the inner content of the SVG element
                inner_content = svg_content.split('>', 1)[1].rsplit('</svg>', 1)[0]
                inner_content = inner_content.replace(f'id="{name}"', f'id="{theme}/{category}/{name}"')

                # Append a group element with the extracted content
                svg_container += f'<g id="{name}" transform="translate(0,{y_offset})">{inner_content}</g>'
                y_offset += 50
            svg_container += '</g>'
        svg_container += '</g>'

    svg_container += '</svg>'
    return svg_container

# Group all categorized SVGs into the semantics container
semantics_svg = group_svgs_into_semantics_container(categorized_svgs)


# Give the output in a file
with open('semantic.svg', 'w') as f:
    f.write(semantics_svg)

