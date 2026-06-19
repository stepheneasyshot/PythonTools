"""Convert PNG images to ICO icon format."""

from PIL import Image


def convert_png_to_ico(png_path, ico_path):
    """Convert a PNG image to ICO format.

    Args:
        png_path: Path to the source PNG file.
        ico_path: Path for the output ICO file.

    Raises:
        FileNotFoundError: If the PNG file does not exist.
        ValueError: If the image format is unsupported.
    """
    try:
        image = Image.open(png_path)
        image.save(ico_path, format="ICO", sizes=[(image.width, image.height)])
        print(f"Converted: {png_path} -> {ico_path}")
    except FileNotFoundError:
        print(f"Error: file not found - {png_path}")
        raise
    except Exception as e:
        print(f"Error converting {png_path} to ICO: {e}")
        raise


if __name__ == "__main__":
    import os
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    src = filedialog.askopenfilename(
        title="选择一个 PNG 图片",
        filetypes=[("PNG 图片", "*.png"), ("所有文件", "*.*")],
    )

    if not src:
        print("未选择任何文件。")
    else:
        out = os.path.splitext(src)[0] + ".ico"
        convert_png_to_ico(src, out)