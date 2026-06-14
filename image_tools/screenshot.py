"""Capture the full screen and save as a PNG image."""

import time
from PIL import ImageGrab


def capture_screen(output_path="screenshot.png", delay=0):
    """Capture the entire screen and save to a file.

    Args:
        output_path: Path for the saved screenshot. Defaults to "screenshot.png".
        delay: Seconds to wait before capturing. Defaults to 0.

    Returns:
        Path to the saved screenshot file.
    """
    if delay > 0:
        print(f"Waiting {delay} seconds...")
        time.sleep(delay)

    print("Capturing screen...")
    screenshot = ImageGrab.grab()
    screenshot.save(output_path)
    print(f"Screenshot saved to {output_path}")
    return output_path


if __name__ == "__main__":
    capture_screen("full_screen_capture.png", delay=10)