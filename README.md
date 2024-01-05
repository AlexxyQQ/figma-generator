# Color Shades and SVG Generator

## Overview

This repository contains a Python script for generating a series of color shades based on a base color and creating SVG representations of these shades. It's designed to help designers and developers visualize and utilize consistent color schemes across their projects.

## Features

- Color Shade Generation: Given a base hex color, the script generates a range of shades.
- SVG Output: Each color and its shades are represented in an SVG format for easy visualization.
- Theme Customization: Includes light and dark theme color mappings.
- Color Mapping: A JSON file containing mappings of color names to their respective hex values.

## Files in this Repository

- `color_shades.svg`: SVG file showing all generated color shades.
- `color_map.json`: JSON file containing the hex values of all generated color shades.
- `semantic.svg`: SVG file that includes color semantics for light and dark themes.
- `README.md`: This file, explaining the project and its components.

## How to Use

### Generating Color Shades

1. **Modify Base Colors**: Edit the colors dictionary in the script to include your base colors.
2. **Run the Script**: Execute the Python script. It will generate color shades based on the specified base colors and create corresponding SVG files.

## Viewing SVGs

You can drag and drop the svg into the figma to view it as a vector image.

## Utilizing JSON Color Map

- Integrate color_map.json in your project to maintain color consistency.
- Use the key-value pairs in your CSS, HTML, or other design tools.
