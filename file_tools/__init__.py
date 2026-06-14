"""File utility tools: encoding, renaming, format conversion, cleanup."""

__all__ = [
    "encode_file_variables",
    "decode_base64",
    "rename_files",
    "markdown_to_pdf",
    "clean_macos_temp_files",
]


def __getattr__(name):
    if name in ("encode_file_variables", "decode_base64"):
        from .base64_encoder import encode_file_variables, decode_base64
        return locals()[name]
    if name == "rename_files":
        from .batch_rename import rename_files
        return rename_files
    if name == "markdown_to_pdf":
        from .convert_md_to_pdf import markdown_to_pdf
        return markdown_to_pdf
    if name == "clean_macos_temp_files":
        from .macos_cleaner import clean_macos_temp_files
        return clean_macos_temp_files
    raise AttributeError(f"module 'file_tools' has no attribute {name!r}")