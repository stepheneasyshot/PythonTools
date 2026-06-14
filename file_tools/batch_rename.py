"""Batch rename files in a directory using regex pattern matching."""

import os
import re


def rename_files(directory, pattern, replacement):
    """Rename all files matching a regex pattern in the given directory.

    Args:
        directory: Path to the directory containing files to rename.
        pattern: Regular expression pattern to match in filenames.
        replacement: Replacement string for the matched pattern.

    Returns:
        List of (original_name, new_name) tuples for renamed files.
    """
    renamed = []
    for filename in os.listdir(directory):
        if re.search(pattern, filename):
            new_filename = re.sub(pattern, replacement, filename)
            os.rename(
                os.path.join(directory, filename),
                os.path.join(directory, new_filename),
            )
            print(f"Renamed: {filename} -> {new_filename}")
            renamed.append((filename, new_filename))
    return renamed


if __name__ == "__main__":
    # Example usage
    rename_files(
        directory="/path/to/your/directory",
        pattern=r"old_name",
        replacement="new_name",
    )