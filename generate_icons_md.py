# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import os
from collections import defaultdict

# Define the icon sizes and styles
icon_sizes = ["12", "16", "20", "24", "28", "32", "48"]
icon_styles = ["regular", "filled"]

def to_camel_case(snake_str):
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])

def write_icon_file(icons_md, weight_type):
    icons_md.write("<!-- This file is generated using generate_icons_md.py -->\n")
    icons_md.write(f"# {weight_type.title()} Icons\n")
    icons_md.write("\n")
    icons_md.write("|Name|Icon|iOS|Android|\n")
    icons_md.write("|---|---|---|---|\n")

    for asset_dir in sorted(os.listdir("assets")):
        if asset_dir == ".DS_Store":
            continue

        largest_svg_icon_path_by_weight = {}

        ios_references_by_weight = defaultdict(list)
        android_references_by_weight = defaultdict(list)
        weights = set()

        pdf_dir = os.path.join("assets", asset_dir, "PDF")
        for filename in sorted(os.listdir(pdf_dir)):
            components = filename.replace(".pdf", "").split("_")[2:]
            weight = components[-1]
            weights.add(weight)
            ios_references_by_weight[weight].append(f'`{to_camel_case("_".join(components))}`')

        svg_dir = os.path.join("assets", asset_dir, "SVG")
        for filename in sorted(os.listdir(svg_dir)):
            weight = filename.split("_")[-1].replace(".svg", "")
            weights.add(weight)
            android_references_by_weight[weight].append(f'`{filename.replace(".svg", "")}`')
            largest_svg_icon_path_by_weight[weight] = filename

        for weight in sorted(weights, reverse=True):
            if weight != weight_type:
                continue
            icons_md.write(
                f"|{asset_dir}"
                f'|<img src="{svg_dir}/{largest_svg_icon_path_by_weight[weight]}?raw=true" width="24" height="24">'
                f'|{"<br />".join(ios_references_by_weight[weight])}'
                f'|{"<br />".join(android_references_by_weight[weight])}|\n'
            )

def check_missing_icons():
    missing_icons_dict = {}
    for folder in os.listdir("assets"):
        svg_dir = os.path.join("assets", folder, "SVG")
        if os.path.exists(svg_dir):
            icon_name = folder.lower().replace(" ", "_")
            for style in icon_styles:
                missing_sizes = []
                for size in icon_sizes:
                    filename = f"ic_fluent_{icon_name}_{size}_{style}.svg"
                    if not os.path.exists(os.path.join(svg_dir, filename)):
                        missing_sizes.append(size)
                if missing_sizes:
                    missing_icons_dict.setdefault((folder, style), []).extend(missing_sizes)
    
    # Convert the dictionary into a list of tuples
    missing_icons = [(icon_name, style, ", ".join(sizes)) for (icon_name, style), sizes in missing_icons_dict.items()]
    return missing_icons

# Function to generate Markdown file listing missing icons
def write_missing_icons_file(md_file):
    missing_icons = check_missing_icons()
    # Sort the missing icons alphabetically by icon name
    missing_icons.sort(key=lambda x: x[0])

    md_file.write("<!-- This file is generated by a script to list missing icons -->\n")
    md_file.write("# Missing Sizes and Styles\n\n")
    md_file.write("| Icon Name | Style | Size |\n")
    md_file.write("|-----------|-------|------|\n")
    for item in missing_icons:
        if len(item) == 3:
            md_file.write(f"| {item[0]} | {item[1].title()} | {item[2]} |\n")

with open("icons_filled.md", "w") as icons_filled_md:
    write_icon_file(icons_filled_md, "filled")

with open("icons_regular.md", "w") as icons_regular_md:
    write_icon_file(icons_regular_md, "regular")

with open("missing_icons.md", "w") as missing_icons_md:
    write_missing_icons_file(missing_icons_md)
