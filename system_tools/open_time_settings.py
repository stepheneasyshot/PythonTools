"""Open the Windows Date & Time settings page."""

import subprocess


def open_date_time_settings():
    """Open the Windows 'Date & Time' settings page via the ms-settings URI.

    Raises:
        RuntimeError: If the settings page cannot be opened.
    """
    print("Opening Windows Date & Time settings...")
    try:
        subprocess.run(["start", "ms-settings:dateandtime"], check=True, shell=True)
        print("Settings page opened successfully.")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to open settings: {e}") from e


if __name__ == "__main__":
    open_date_time_settings()