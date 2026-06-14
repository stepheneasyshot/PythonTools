"""Image processing tools: format conversion, negative-to-positive, screenshot."""

__all__ = [
    "convert_jpg_to_png",
    "convert_png_to_ico",
    "convert_mp4_to_gif",
    "process_image",
    "run_app",
    "capture_screen",
]


def __getattr__(name):
    if name == "convert_jpg_to_png":
        from .convert_jpg_to_png import convert_jpg_to_png
        return convert_jpg_to_png
    if name == "convert_png_to_ico":
        from .convert_png_to_ico import convert_png_to_ico
        return convert_png_to_ico
    if name == "convert_mp4_to_gif":
        from .convert_mp4_to_gif import convert_mp4_to_gif
        return convert_mp4_to_gif
    if name == "process_image":
        from .negative_to_positive import process_image
        return process_image
    if name == "run_app":
        from .negative_to_positive import run_app
        return run_app
    if name == "capture_screen":
        from .screenshot import capture_screen
        return capture_screen
    raise AttributeError(f"module 'image_tools' has no attribute {name!r}")