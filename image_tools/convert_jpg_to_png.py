"""Convert JPG images to PNG format.

Supports single file or batch conversion of all JPG files in a directory.
"""

import os
from pathlib import Path
from PIL import Image


def convert_jpg_to_png(source_path, target_folder=None):
    """Convert one or more JPG images to PNG format.

    Args:
        source_path: Path to a single JPG file or a directory containing JPG files.
        target_folder: Optional output directory. If omitted, saves alongside the source.

    Returns:
        List of paths to the generated PNG files.
    """
    if target_folder and not os.path.exists(target_folder):
        os.makedirs(target_folder)

    if os.path.isfile(source_path):
        files = [source_path]
    else:
        source_path = str(source_path)
        files = [
            os.path.join(source_path, f)
            for f in os.listdir(source_path)
            if f.lower().endswith(".jpg")
        ]

    output_paths = []
    for file_path in files:
        try:
            with Image.open(file_path) as img:
                file_name = os.path.splitext(os.path.basename(file_path))[0]
                save_dir = target_folder if target_folder else os.path.dirname(file_path)
                out_path = os.path.join(save_dir, f"{file_name}.png")
                img.save(out_path, "PNG")
                print(f"Converted: {file_path} -> {out_path}")
                output_paths.append(out_path)
        except Exception as e:
            print(f"Error converting {file_path}: {e}")

    return output_paths


if __name__ == "__main__":
    # Example: convert a single file
    # convert_jpg_to_png("example.jpg")

    # Example: batch convert all JPGs in a directory
    input_dir = Path("~/Downloads/app_icon.jpg").expanduser()
    output_dir = "./converted_pngs"
    convert_jpg_to_png(input_dir, output_dir)