"""System utility tools: file monitoring, system settings."""

__all__ = [
    "start_monitoring",
    "delete_scr_files",
    "open_date_time_settings",
]


def __getattr__(name):
    if name in ("start_monitoring", "delete_scr_files"):
        from .scr_cleaner import start_monitoring, delete_scr_files
        return locals()[name]
    if name == "open_date_time_settings":
        from .open_time_settings import open_date_time_settings
        return open_date_time_settings
    raise AttributeError(f"module 'system_tools' has no attribute {name!r}")