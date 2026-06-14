"""Music/audio processing tools: NCM decryption, audio format conversion."""

__all__ = [
    "dump_ncm_file",
    "get_all_files",
    "decrypt_ncm",
]


def __getattr__(name):
    if name in ("dump_ncm_file", "get_all_files", "decrypt_ncm"):
        from .ncm_decrypt import dump_ncm_file, get_all_files, decrypt_ncm
        return locals()[name]
    raise AttributeError(f"module 'music_tools' has no attribute {name!r}")