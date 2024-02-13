import sys


def get_user_input(description, default):
    """Get user input or provide default."""
    try:
        return input(f"{description} [{default}]: ") or default
    except EOFError:
        return default


def main():
    # font_family = get_user_input("Enter font family", "Roboto")
    # bold_weight = get_user_input("Bold font weight", "700")
    # regular_weight = get_user_input("Regular font weight", "400")
    # light_weight = get_user_input("Light font weight", "300")
    # body_small_size = get_user_input("Body small font size (px)", "12")
    # body_small_line_height = get_user_input("Body small line height", "1.5")
    # body_medium_size = get_user_input("Body medium font size (px)", "14")
    # body_medium_line_height = get_user_input("Body medium line height", "1.5")
    # body_large_size = get_user_input("Body large font size (px)", "16")
    # body_large_line_height = get_user_input("Body large line height", "1.5")
    # caption_size = get_user_input("Caption font size (px)", "10")
    # caption_line_height = get_user_input("Caption line height", "1.2")
    #  Predefined user preferences
    font_family = "Roboto"
    bold_weight = "700"
    regular_weight = "400"
    light_weight = "300"
    body_small_size = "12"
    body_small_line_height = "1.5"
    body_medium_size = "14"
    body_medium_line_height = "1.5"
    body_large_size = "16"
    body_large_line_height = "1.5"
    caption_size = "10"
    caption_line_height = "1.2"

    variations = build_variations(
        bold_weight,
        regular_weight,
        light_weight,
        body_small_size,
        body_small_line_height,
        body_medium_size,
        body_medium_line_height,
        body_large_size,
        body_large_line_height,
        caption_size,
        caption_line_height,
    )

    css_content = generate_css(font_family, variations)
    save_to_file("typography/custom_typography.css", css_content)
    print("Custom typography CSS has been generated and saved.")

    combined_svg_file = create_svg_variations(font_family, variations)
    print(
        f"Combined typography SVG has been generated and saved as '{combined_svg_file}'."
    )


def build_variations(
    bold_weight,
    regular_weight,
    light_weight,
    body_small_size,
    body_small_line_height,
    body_medium_size,
    body_medium_line_height,
    body_large_size,
    body_large_line_height,
    caption_size,
    caption_line_height,
):
    return {
        "Headings": {
            "H1": ("36", "1.2", bold_weight),
            "H2": ("32", "1.4", bold_weight),
            "H3": ("28", "1.4", bold_weight),
            "H4": ("24", "1.4", bold_weight),
            "H5": ("20", "1.4", bold_weight),
            "H6": ("16", "1.4", bold_weight),
        },
        "Bold": {
            "Body Small": (body_small_size, body_small_line_height, bold_weight),
            "Body Medium": (body_medium_size, body_medium_line_height, bold_weight),
            "Body Large": (body_large_size, body_large_line_height, bold_weight),
        },
        "Regular": {
            "Body Small": (body_small_size, body_small_line_height, regular_weight),
            "Body Medium": (body_medium_size, body_medium_line_height, regular_weight),
            "Body Large": (body_large_size, body_large_line_height, regular_weight),
        },
        "Light": {
            "Body Small": (body_small_size, body_small_line_height, light_weight),
            "Body Medium": (body_medium_size, body_medium_line_height, light_weight),
            "Body Large": (body_large_size, body_large_line_height, light_weight),
        },
        "Captions": {
            "Caption": (caption_size, caption_line_height, light_weight),
            # Add other caption styles as needed
        },
    }


def generate_css(font_family, variations):
    base_settings = f"""/* Base settings */
     body {{
       font-family: '{font_family}', sans-serif;
       margin: 0;
     }}
     """

    typography_css = ""
    for group_name, group_variations in variations.items():
        for variation_name, (size, line_height, weight) in group_variations.items():
            # Convert group and variation names into a CSS class name
            class_name = f"{variation_name.lower().replace(' ', '-')}"
            typography_css += f"""
                            .{class_name} {{
                              font-size: {size}px;
                              line-height: {line_height};
                              font-weight: {weight};
                              font-family: '{font_family}';
                              margin: 0;

                            }}
                            """

    return base_settings + typography_css


def create_svg_variations(font_family, variations):
    vertical_position = 40  # Initial vertical position
    group_spacing = 100  # Space between main groups
    element_spacing = 120  # Space between elements in a group

    # Dynamically calculate total height
    total_height = sum(
        [
            group_spacing + len(subgroup) * 20
            for group in variations.values()
            for subgroup in group.values()
        ]
    )

    svg_header = f'<svg id="typography" width="650" height="{total_height}" xmlns="http://www.w3.org/2000/svg">\n'
    svg_content = ""

    for group_name, group_variations in variations.items():
        # Normalize group name for ID (e.g., "Body Bold" -> "bold")
        group_id = group_name.lower().replace(" ", "_")

        # Main group label
        svg_content += f'<g id="{group_id}">\n'
        svg_content += f'  <text x="10" y="{vertical_position}" fill="#02080A" font-size="28" font-family="Arial" font-weight="bold">{group_name}</text>\n'
        vertical_position += 40  # Adjust for group label

        for variation_name, variation_props in group_variations.items():
            # Normalize variation name for ID (e.g., "Body Small" -> "body/small")
            variation_id = variation_name.lower().replace(" ", "/")

            # Individual variation group
            svg_content += f'  <g id="{group_id}/{variation_id}">\n'
            size, line_height, weight = variation_props

            # Variation name
            svg_content += f'    <text x="20" y="{vertical_position}" fill="#02080A" font-size="{size}" font-family="{font_family}">{variation_name}</text>\n'
            # Example usage with detailed ID
            svg_content += f'    <text x="20" y="{vertical_position + 50}" fill="#50616A" font-size="{size}" font-family="{font_family}" id="{group_id}/{variation_id}">The quick brown fox jumps over the lazy dog.</text>\n'
            # Typography properties
            svg_content += f'    <text x="20" y="{vertical_position + 70}" fill="#50616A" font-size="12" font-family="Arial">{size}px / W{weight}</text>\n'
            svg_content += "  </g>\n"
            vertical_position += element_spacing  # Adjust for the next variation

        svg_content += "</g>\n"  # Close main group
        vertical_position += (
            group_spacing  # Additional space before the next main group
        )

    svg_footer = "</svg>"
    combined_svg = svg_header + svg_content + svg_footer

    # Save the combined SVG content to a file
    file_path = "typography/typography_variations.svg"
    with open(file_path, "w") as file:
        file.write(combined_svg)

    return file_path


def save_to_file(file_path, content):
    with open(file_path, "w") as file:
        file.write(content)


if __name__ == "__main__":
    main()
