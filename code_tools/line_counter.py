"""Count lines of code in a project directory, grouped by language.

Supports Kotlin, Java, XML, Python, C/C++, and Groovy file types.
Ignores blank lines and single-line comments.
"""

import os
import sys
from collections import defaultdict


LANGUAGE_EXTENSIONS = {
    "Kotlin": (".kt", ".kts"),
    "Java": (".java",),
    "XML": (".xml",),
    "Python": (".py",),
    "C/C++": (".c", ".cpp", ".h", ".hpp"),
    "Groovy": (".groovy",),
}

COMMENT_PREFIXES = ("#", "//")


def count_lines(file_path):
    """Count non-blank, non-comment lines in a single file.

    Args:
        file_path: Path to the file to analyze.

    Returns:
        Number of valid code lines.
    """
    count = 0
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                stripped = line.strip()
                if stripped and not stripped.startswith(COMMENT_PREFIXES):
                    count += 1
    except Exception as e:
        print(f"Cannot read {file_path}: {e}")
    return count


def analyze_project(project_path):
    """Analyze a project directory and print code line statistics by language.

    Args:
        project_path: Path to the project root directory.

    Returns:
        Dictionary mapping language -> (file_count, line_count).
    """
    if not os.path.isdir(project_path):
        print(f"Error: '{project_path}' is not a valid directory.")
        return {}

    line_counts = defaultdict(int)
    file_counts = defaultdict(int)

    print(f"Scanning: {project_path}\n")

    for root, _, files in os.walk(project_path):
        for file in files:
            for lang, extensions in LANGUAGE_EXTENSIONS.items():
                if file.endswith(extensions):
                    file_path = os.path.join(root, file)
                    lines = count_lines(file_path)
                    line_counts[lang] += lines
                    file_counts[lang] += 1
                    break

    # Print results table
    print("--- Code Line Count ---")
    table = [["Language", "Files", "Lines"]]
    total_lines = 0
    total_files = 0

    for lang in sorted(line_counts.keys()):
        table.append([lang, str(file_counts[lang]), str(line_counts[lang])])
        total_lines += line_counts[lang]
        total_files += file_counts[lang]

    col_widths = [max(len(row[i]) for row in table) for i in range(3)]

    header = " | ".join(f"{h:<{w}}" for h, w in zip(table[0], col_widths))
    print(header)
    print("-+-".join("-" * w for w in col_widths))

    for row in table[1:]:
        print(" | ".join(f"{cell:<{w}}" for cell, w in zip(row, col_widths)))

    print("-" * len(header))
    print(" | ".join(f"{cell:<{w}}" for cell, w in zip(["Total", str(total_files), str(total_lines)], col_widths)))
    print()

    return {lang: (file_counts[lang], line_counts[lang]) for lang in line_counts}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python line_counter.py <project_path>")
        sys.exit(1)
    analyze_project(sys.argv[1])