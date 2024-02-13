def get_user_input(prompt, default):
    """Helper function to get user input or provide default."""
    user_input = input(prompt + f" [{default}]: ").strip()
    return user_input if user_input else default


def main():
    # # Collect user preferences
    # font_family = get_user_input("Enter font family", "Roboto")
    # bold_weight = get_user_input("Bold font weight", "700")
    # regular_weight = get_user_input("Regular font weight", "400")
    # light_weight = get_user_input("Light font weight", "300")

    # # Body text preferences
    # body_small_size = get_user_input("Body small font size (px)", "12")
    # body_small_line_height = get_user_input("Body small line height", "1.5")

    # body_medium_size = get_user_input("Body medium font size (px)", "14")
    # body_medium_line_height = get_user_input("Body medium line height", "1.5")

    # body_large_size = get_user_input("Body large font size (px)", "16")
    # body_large_line_height = get_user_input("Body large line height", "1.5")

    # # Caption text preferences
    # caption_size = get_user_input("Caption font size (px)", "10")
    # caption_line_height = get_user_input("Caption line height", "1.2")

    # All at once
    # Collect user preferences
    font_family = "Roboto"
    bold_weight = "700"
    regular_weight = "400"
    light_weight = "300"

    # Body text preferences
    body_small_size = "12"
    body_small_line_height = "1.5"

    body_medium_size = "14"
    body_medium_line_height = "1.5"

    body_large_size = "16"
    body_large_line_height = "1.5"

    # Caption text preferences
    caption_size = "10"
    caption_line_height = "1.2"

    # Heading preferences (h1 to h6)
    headings = {}
    for i in range(1, 7):
        size = str(36 - (i - 1) * 4)
        line_height = "1.2" if i == 1 else "1.4"
        weight = 700
        headings[f"h{i}"] = (size, line_height, weight)

    # Generate CSS
    css_content = f"""/* Base settings */
body {{
  font-family: "{font_family}", sans-serif; /* Example font */
  margin: 0;
}}

/* Font weight categories */
.bold {{
  font-weight: {bold_weight}; /* Typically 700 */
}}

.regular {{
  font-weight: {regular_weight}; /* Typically 400 */
}}

.light {{
  font-weight: {light_weight};
}}

/* Body text */
.body-small {{
  font-size: {body_small_size}px;
  line-height: {body_small_line_height};
  margin: 0;
}}

.body-medium {{
  font-size: {body_medium_size}px;
  line-height: {body_medium_line_height};
  margin: 0;
}}

.body-large {{
  font-size: {body_large_size}px;
  line-height: {body_large_line_height};
  margin: 0;
}}

/* Caption Text */
.caption {{
  font-size: {caption_size}px;
  line-height: {caption_line_height};
  margin: 0;
}}
"""

    # Append headings to CSS
    for h, (size, line_height, weight) in headings.items():
        css_content += f"""
{h} {{
  font-size: {size}px;
  line-height: {line_height};
  font-weight: {weight};
  margin: 0;
}}
"""

    # Save to CSS file
    with open("custom_typography.css", "w") as file:
        file.write(css_content)

    print(
        "Custom typography CSS has been generated and saved as 'custom_typography.css'."
    )


if __name__ == "__main__":
    main()
