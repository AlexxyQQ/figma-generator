import json


# Function to load JSON data from a file
def load_json(filename):
    with open(filename, "r") as file:
        return json.load(file)


# Load the color map, light theme, and dark theme from JSON files
color_map = load_json("primitive_colors/primitive_colors_map.json")
light_theme = load_json("meterial_semantic/meterial_tamplete/light_theme_semantic.json")
dark_theme = load_json("meterial_semantic/meterial_tamplete/dark_theme_semantic.json")


def convert_to_sentence_case(name):
    # Split the name by underscores, capitalize each part, then join back with spaces
    return " ".join(word.capitalize() for word in name.split("_"))


# Assuming the JSON files are loaded into color_map, light_theme, and dark_theme variables
def create_svg_element(color_code, name, color_map):
    # Determine fill color based on the color map; default to white if not found
    fill_color = color_map.get(color_code, "#FFFFFF")
    # Initially, assign an ID to the <rect> that matches the 'name'
    svg_content = f"""
    <svg id="{name}" width="500" height="50" xmlns="http://www.w3.org/2000/svg">
        <rect id="{name}" width="50" height="50" fill="{fill_color}" x="0" y="0" rx="4" ry="4"/>
        <text x="60" y="25" fill="black" font-size="14" font-family="Arial" dominant-baseline="middle">{convert_to_sentence_case(name)} ({color_code})</text>
        <text x="60" y="40" fill="black" font-size="10" font-family="Arial" dominant-baseline="middle">{fill_color}</text>
    </svg>
    """
    return svg_content


def create_svg_dynamic_for_figma(color_map, theme):
    theme_svgs = {}
    for key, value in theme.items():
        # For each theme item, generate its SVG representation
        theme_svgs[key] = create_svg_element(value, key, color_map)
    return theme_svgs


# Generate SVGs for light and dark themes
light_theme_svgs = create_svg_dynamic_for_figma(color_map, light_theme)
dark_theme_svgs = create_svg_dynamic_for_figma(color_map, dark_theme)


def group_svgs_by_theme_and_category(light_svgs, dark_svgs):
    # Define the recognized categories
    recognized_categories = [
        "primary",
        "secondary",
        "tertiary",
        "error",
        "surface",
        "background",
    ]
    # Initialize theme structure with categories, including an "Others" category
    themes = {
        "light": {category: [] for category in recognized_categories + ["others"]},
        "dark": {category: [] for category in recognized_categories + ["others"]},
    }

    # Helper function to determine the category of a given name
    def get_category(name):
        for category in recognized_categories:
            if category.lower() in name.lower():  # Case-insensitive match
                return category
        return "others"  # Default category if no match found

    # Helper function to categorize and group SVG elements under their theme and category
    def categorize_and_group(theme_svgs, theme):
        for name, svg_content in theme_svgs.items():
            category = get_category(name)  # Determine the category for each name
            themes[theme][category].append((name, svg_content))

    # Categorize and group SVGs for both light and dark themes
    categorize_and_group(light_svgs, "light")
    categorize_and_group(dark_svgs, "dark")

    return themes


# Function to create and group SVG elements into a semantic container
def group_svgs_into_semantics_container(categorized_svgs):
    svg_container = (
        '<svg id="semantics_container" xmlns="http://www.w3.org/2000/svg" width="2000">'
    )
    y_offset = 0

    for theme, categories in categorized_svgs.items():
        svg_container += f'<g id="{theme}" transform="translate(0,{y_offset})">'
        x_offset = 0

        for category, svgs in categories.items():
            svg_container += (
                f'<g id="{theme}/{category}" transform="translate({x_offset},0)">'
            )
            local_y_offset = 0
            for name, svg_content in svgs:
                # Generate a new ID based on theme, category, and name
                new_id = f"{theme}/{category}/{name}"
                # Update the ID in the SVG content, specifically targeting the <rect> element's ID
                modified_svg_content = svg_content.replace(
                    f'id="{name}"', f'id="{new_id}"'
                )
                svg_container += f'<g id="{new_id}" transform="translate(0, {local_y_offset})">{modified_svg_content}</g>'
                local_y_offset += 60
            svg_container += "</g>"
            x_offset += 500
        svg_container += "</g>"
        if theme == "light":
            y_offset += local_y_offset + 600
        else:
            y_offset += local_y_offset

    svg_container += "</svg>"
    return svg_container


# Generate SVGs for light and dark themes
light_theme_svgs = create_svg_dynamic_for_figma(color_map, light_theme)
dark_theme_svgs = create_svg_dynamic_for_figma(color_map, dark_theme)

# Categorize SVGs by theme and category
categorized_svgs = group_svgs_by_theme_and_category(light_theme_svgs, dark_theme_svgs)

# Group categorized SVGs into a semantics container
semantics_svg = group_svgs_into_semantics_container(categorized_svgs)

# Save the final SVG to a file
with open("meterial_semantic/semantic.svg", "w") as f:
    f.write(semantics_svg)


# Assuming the color_map, light_theme, and dark_theme data is already loaded as shown in the provided code.


def save_theme_colors_as_json(theme, theme_name):
    # Extract and save the theme colors in a JSON format where the key is the semantic name and the value is the hex color.
    theme_colors = {}
    for key, value in theme.items():
        # Use the color code to get the actual hex value from the color map
        color_hex = color_map.get(value, "#FFFFFF")
        theme_colors[key] = color_hex

    # Save to a JSON file
    filename = f"meterial_semantic/{theme_name}_theme_colors.json"
    with open(filename, "w") as file:
        json.dump(theme_colors, file, indent=4)

    return filename


# Save light and dark theme colors as separate JSON files
light_theme_colors_file = save_theme_colors_as_json(light_theme, "light")
dark_theme_colors_file = save_theme_colors_as_json(dark_theme, "dark")

light_theme_colors_file, dark_theme_colors_file

# Output the path of the generated file
print("Generated SVG saved to semantic.svg")
