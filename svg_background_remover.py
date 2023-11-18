
import xml.etree.ElementTree as ET
import argparse


def parse_svg(file_path):
    """
    Parse an SVG file and return the parsed XML tree.

    :param file_path: Path to the SVG file to be parsed
    :return: Parsed XML tree of the SVG file
    """
    try:
        tree = ET.parse(file_path)
        print(f"SVG file {file_path} parsed successfully.")
        return tree
    except ET.ParseError as e:
        print(f"Error parsing SVG file: {e}")
        return None
    

def color_distance(hex_color1, hex_color2):
        rgb1 = tuple(int(hex_color1[i:i+2], 16) for i in (0, 2, 4))
        rgb2 = tuple(int(hex_color2[i:i+2], 16) for i in (0, 2, 4))
        return sum((c1 - c2) ** 2 for c1, c2 in zip(rgb1, rgb2)) ** 0.5


def remove_background(svg_tree, size_threshold=10000, tags=['path'], fill_color='#FFFFFF', color_tolerance=10):
    root = svg_tree.getroot()
    backgrounds = []
    processed_fill_color = fill_color.lstrip('#')

    for tag in tags:
        for element in root.findall(f'.//{{http://www.w3.org/2000/svg}}{tag}'):
            if ('width' in element.attrib and 'height' in element.attrib) or 'fill' in element.attrib:
                try:
                    if 'width' in element.attrib and 'height' in element.attrib:
                        width = float(element.attrib['width'])
                        height = float(element.attrib['height'])
                        size_check = width * height > size_threshold
                    else:
                        size_check = True

                    element_fill = element.attrib.get('fill', '').lstrip('#')
                    fill_check = color_distance(element_fill, processed_fill_color) <= color_tolerance

                    if size_check and fill_check:
                        backgrounds.append(element)
                except ValueError:
                    continue

    

    # Print the number of background elements found
    print(f"Found {len(backgrounds)} background elements to remove.")

    # Remove identified background elements
    for bg in backgrounds:
        root.remove(bg)


def save_svg(svg_tree, output_path):
    """
    Save the modified SVG XML tree back to an SVG file.

    :param svg_tree: Modified XML tree of the SVG file
    :param output_path: Path where the modified SVG file will be saved
    """
    svg_tree.write(output_path, encoding='utf-8', xml_declaration=True)

    print(f"SVG file saved as {output_path}.")


def main():
    # Prompt for the SVG file path
    svg_file = input("Enter the path to the SVG file: ")

    # Optional parameters with default values
    size_threshold = input("Enter size threshold for background detection (default 10000): ")
    size_threshold = int(size_threshold) if size_threshold else 10000

    fill_color = input("Enter fill color for background detection (default #FFFFFF): ")
    fill_color = fill_color if fill_color else '#FFFFFF'

    # Prompt for the output file path
    output = input("Enter the output file path (leave blank for default name): ")
    output_path = output if output else svg_file.replace('.svg', '_no_background.svg')

    # Process SVG file
    tree = parse_svg(svg_file)
    if tree is not None:
        remove_background(tree, size_threshold=size_threshold, tags=['path'], fill_color=fill_color)
        save_svg(tree, output_path)

if __name__ == "__main__":
    main()




