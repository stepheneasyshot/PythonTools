"""Base64-encode string variable values in source code files.

Designed for Kotlin files: finds `val variable = "value"` patterns and
encodes the string values with Base64 while preserving the file structure.
"""

import base64
import re


def encode_file_variables(file_path, pattern=None, output_path=None):
    """Find string variable assignments in a file and Base64-encode their values.

    The default pattern matches Kotlin-style `val name = "value"` assignments.

    Args:
        file_path: Path to the source file to process.
        pattern: Optional regex pattern. Must have groups for (prefix, varname, value, suffix).
                 Default matches Kotlin `val var = "value"`.
        output_path: Path for the output file. If None, appends '_encoded' before the extension.

    Returns:
        The encoded file content as a string, or None on failure.

    Raises:
        FileNotFoundError: If the input file does not exist.
    """
    if pattern is None:
        pattern = r'(val\s+(\w+)\s*=\s*")([^"]*)(")'

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        def _replace_with_base64(match):
            prefix = match.group(1)
            var_name = match.group(2)
            original_value = match.group(3)
            suffix = match.group(4)

            encoded = base64.b64encode(original_value.encode("utf-8")).decode("utf-8")
            print(f"Encoded variable: {var_name}")
            print(f"  Original: {original_value}")
            print(f"  Base64:   {encoded}")
            return f"{prefix}{encoded}{suffix}"

        new_content = re.sub(pattern, _replace_with_base64, content)

        if output_path is None:
            output_path = file_path.rsplit(".", 1)[0] + "_encoded." + file_path.rsplit(".", 1)[1]

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"Done! Output: {output_path}")
        return new_content

    except FileNotFoundError:
        print(f"Error: file not found - {file_path}")
        raise


def decode_base64(encoded_string):
    """Decode a Base64-encoded string.

    Args:
        encoded_string: The Base64 string to decode.

    Returns:
        Decoded UTF-8 string, or an error message if decoding fails.
    """
    try:
        decoded = base64.b64decode(encoded_string)
        return decoded.decode("utf-8")
    except Exception as e:
        return f"Decode failed: {e}"


if __name__ == "__main__":
    # Example: encode variables in a Kotlin file
    encode_file_variables("example.kt")