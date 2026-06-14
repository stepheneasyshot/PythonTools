"""AI/LLM tools: local model chat, DeepSeek API, Gemini video generation."""

__all__ = [
    "load_model",
    "chat_loop",
    "deepseek_chat",
    "generate_video",
]


def __getattr__(name):
    if name in ("load_model", "chat_loop"):
        from .local_llm_chat import load_model, chat_loop
        return locals()[name]
    if name == "deepseek_chat":
        from .deepseek_chat import deepseek_chat
        return deepseek_chat
    if name == "generate_video":
        from .gemini_video_gen import generate_video
        return generate_video
    raise AttributeError(f"module 'ai_tools' has no attribute {name!r}")