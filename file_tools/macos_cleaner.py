"""Recursively delete macOS temporary files (._* and .DS_Store)."""

import os


def clean_macos_temp_files(directory):
    """Recursively delete macOS temporary files (._* and .DS_Store) from a directory.

    Args:
        directory: Root directory to clean.

    Returns:
        Number of files deleted.
    """
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        return 0

    deleted_count = 0
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if item.startswith("._") or item == ".DS_Store":
            try:
                os.remove(item_path)
                print(f"Deleted: {item_path}")
                deleted_count += 1
            except Exception as e:
                print(f"Failed to delete {item_path}: {e}")
        elif os.path.isdir(item_path):
            deleted_count += clean_macos_temp_files(item_path)

    return deleted_count


if __name__ == "__main__":
    total = clean_macos_temp_files("/path/to/clean")
    print(f"Total files deleted: {total}")