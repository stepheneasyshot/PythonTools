"""Code analysis tools: line counting, project statistics."""

__all__ = [
    "count_lines",
    "analyze_project",
]


def __getattr__(name):
    if name in ("count_lines", "analyze_project"):
        from .line_counter import count_lines, analyze_project
        return locals()[name]
    raise AttributeError(f"module 'code_tools' has no attribute {name!r}")