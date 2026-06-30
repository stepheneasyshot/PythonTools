#!/usr/bin/env python3
"""PythonTools - Utility Tools Launcher

A collection of practical Python utility scripts organized by category.
Select a tool to run from the menu.
"""

import sys


TOOLS = {
    "1": {
        "name": "Image: Convert JPG to PNG",
        "module": "image_tools.convert_jpg_to_png",
        "func": "convert_jpg_to_png",
        "interactive": False,
    },
    "2": {
        "name": "Image: Convert PNG to ICO",
        "module": "image_tools.convert_png_to_ico",
        "func": "convert_png_to_ico",
        "interactive": False,
    },
    "3": {
        "name": "Image: Convert MP4 to GIF",
        "module": "image_tools.convert_mp4_to_gif",
        "func": "convert_mp4_to_gif",
        "interactive": False,
    },
    "4": {
        "name": "Image: Film Negative to Positive (Web UI)",
        "module": "image_tools.negative_to_positive",
        "func": "run_app",
        "interactive": True,
    },
    "5": {
        "name": "Image: Take Screenshot",
        "module": "image_tools.screenshot",
        "func": "capture_screen",
        "interactive": False,
    },
    "6": {
        "name": "Image: Compress PNG (TinyPNG-style)",
        "module": "image_tools.png_compressor",
        "func": "compress_png",
        "interactive": False,
    },
    "7": {
        "name": "AI: Local LLM Chat",
        "module": "ai_tools.local_llm_chat",
        "func": "chat_loop",
        "interactive": True,
    },
    "8": {
        "name": "AI: DeepSeek Chat",
        "module": "ai_tools.deepseek_chat",
        "func": "deepseek_chat",
        "interactive": False,
    },
    "9": {
        "name": "AI: Gemini Video Generation",
        "module": "ai_tools.gemini_video_gen",
        "func": "generate_video",
        "interactive": False,
    },
    "10": {
        "name": "File: Base64 Encode Variables",
        "module": "file_tools.base64_encoder",
        "func": "encode_file_variables",
        "interactive": False,
    },
    "11": {
        "name": "File: Batch Rename Files",
        "module": "file_tools.batch_rename",
        "func": "rename_files",
        "interactive": False,
    },
    "12": {
        "name": "File: Markdown to PDF",
        "module": "file_tools.convert_md_to_pdf",
        "func": "markdown_to_pdf",
        "interactive": False,
    },
    "13": {
        "name": "File: Clean macOS Temp Files",
        "module": "file_tools.macos_cleaner",
        "func": "clean_macos_temp_files",
        "interactive": False,
    },
    "14": {
        "name": "System: SCR File Cleaner (Daemon)",
        "module": "system_tools.scr_cleaner",
        "func": "start_monitoring",
        "interactive": True,
    },
    "15": {
        "name": "System: Open Windows Time Settings",
        "module": "system_tools.open_time_settings",
        "func": "open_date_time_settings",
        "interactive": False,
    },
    "16": {
        "name": "Code: Project Line Counter",
        "module": "code_tools.line_counter",
        "func": "analyze_project",
        "interactive": False,
    },
    "17": {
        "name": "Music: Decrypt NCM Files",
        "module": "music_tools.ncm_decrypt",
        "func": "decrypt_ncm",
        "interactive": False,
    },
}


def print_menu():
    """Print the tool selection menu."""
    print("=" * 60)
    print("  PythonTools - Utility Tools")
    print("=" * 60)
    for key, tool in TOOLS.items():
        print(f"  [{key}] {tool['name']}")
    print("  [q] Quit")
    print("-" * 60)


def run_tool(key):
    """Import and run the selected tool's main function.

    Args:
        key: The menu key for the tool to run.
    """
    tool = TOOLS.get(key)
    if not tool:
        print("Invalid selection.")
        return

    try:
        module = __import__(tool["module"], fromlist=[tool["func"]])
        func = getattr(module, tool["func"])
        print(f"\n--- Running: {tool['name']} ---\n")

        if tool["interactive"]:
            func()
        else:
            print("This tool has no interactive mode.")
            print("Import and use it in your own script:")
            print(f"  from {tool['module']} import {tool['func']}")
    except ImportError as e:
        print(f"Error: Could not load module - {e}")
        print("Some tools require additional dependencies (see requirements.txt).")
    except Exception as e:
        print(f"Error running tool: {e}")


def main():
    """Main entry point: show menu and dispatch tool selection."""
    while True:
        print_menu()
        choice = input("\nSelect a tool [1-17, q]: ").strip().lower()

        if choice == "q":
            print("Goodbye!")
            break

        run_tool(choice)
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()