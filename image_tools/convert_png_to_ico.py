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
    # Example usage
    convert_png_to_ico("logo.png", "logo.ico")