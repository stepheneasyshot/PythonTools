#!/usr/bin/env python3
"""PythonTools - 实用工具集 GUI 启动器

使用 tkinter 构建的图形界面入口，按分类展示所有工具。
"""

import io
import os
import sys
import threading
import traceback
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog


# ---------------------------------------------------------------------------
# 工具注册表
# ---------------------------------------------------------------------------

TOOLS = [
    # -- 图片处理 --
    {
        "category": "图片处理",
        "name": "JPG 转 PNG",
        "desc": "批量将 JPG/JPEG 图片转换为 PNG 格式",
        "module": "image_tools.convert_jpg_to_png",
        "func": "convert_jpg_to_png",
        "args": [
            {"label": "选择源文件夹", "type": "dir", "param": "source_path"},
            {"label": "选择目标文件夹（可选，留空则默认）", "type": "dir", "param": "target_folder", "required": False},
        ],
    },
    {
        "category": "图片处理",
        "name": "PNG 转 ICO",
        "desc": "将 PNG 图片转换为 ICO 图标文件",
        "module": "image_tools.convert_png_to_ico",
        "func": "convert_png_to_ico",
        "args": [
            {"label": "选择 PNG 文件", "type": "file", "param": "png_path"},
            {"label": "保存 ICO 文件为", "type": "save", "param": "ico_path", "filetypes": [("ICO files", "*.ico")]},
        ],
    },
    {
        "category": "图片处理",
        "name": "MP4 转 GIF",
        "desc": "将 MP4 视频转换为 GIF 动图",
        "module": "image_tools.convert_mp4_to_gif",
        "func": "convert_mp4_to_gif",
        "args": [
            {"label": "选择 MP4 文件", "type": "file", "param": "input_file", "filetypes": [("MP4 files", "*.mp4")]},
            {"label": "保存 GIF 文件为", "type": "save", "param": "output_file", "filetypes": [("GIF files", "*.gif")]},
        ],
    },
    {
        "category": "图片处理",
        "name": "胶片负片转正片",
        "desc": "启动 Streamlit Web 界面，将胶片负片扫描件转换为正片",
        "module": "image_tools.negative_to_positive",
        "func": "run_app",
        "args": [],
        "terminal_only": True,
        "terminal_hint": "此工具启动 Streamlit Web 服务，请在终端中运行：\nstreamlit run image_tools/negative_to_positive.py",
    },
    {
        "category": "图片处理",
        "name": "屏幕截图",
        "desc": "截取当前屏幕并保存为 PNG 文件",
        "module": "image_tools.screenshot",
        "func": "capture_screen",
        "args": [
            {"label": "保存路径（可选，默认 screenshot.png）", "type": "save", "param": "output_path", "required": False, "filetypes": [("PNG files", "*.png")]},
        ],
    },
    {
        "category": "图片处理",
        "name": "PNG 压缩",
        "desc": "批量压缩 PNG 图片（类似 TinyPNG 效果）",
        "module": "image_tools.png_compressor",
        "func": "compress_png",
        "args": [
            {"label": "选择源文件夹", "type": "dir", "param": "source_path"},
            {"label": "选择目标文件夹（可选，留空则默认）", "type": "dir", "param": "target_path", "required": False},
        ],
    },
    # -- AI 工具 --
    {
        "category": "AI 工具",
        "name": "本地 LLM 聊天",
        "desc": "在终端中启动本地大语言模型对话（需预加载模型）",
        "module": "ai_tools.local_llm_chat",
        "func": "chat_loop",
        "args": [],
        "terminal_only": True,
        "terminal_hint": "此工具需要在代码中加载模型后调用，请在 Python 脚本中使用：\nfrom ai_tools.local_llm_chat import chat_loop\nchat_loop(tokenizer, model, device)",
    },
    {
        "category": "AI 工具",
        "name": "DeepSeek 聊天",
        "desc": "通过 DeepSeek API 进行 AI 对话",
        "module": "ai_tools.deepseek_chat",
        "func": "deepseek_chat",
        "args": [],
        "terminal_only": True,
        "terminal_hint": "此工具需要 API Key，请在终端中运行：\npython -m ai_tools.deepseek_chat",
    },
    {
        "category": "AI 工具",
        "name": "Gemini 视频生成",
        "desc": "通过 Gemini API 生成视频",
        "module": "ai_tools.gemini_video_gen",
        "func": "generate_video",
        "args": [],
        "terminal_only": True,
        "terminal_hint": "此工具需要 API Key 且运行时间较长，请在终端中运行：\npython -m ai_tools.gemini_video_gen",
    },
    # -- 文件工具 --
    {
        "category": "文件工具",
        "name": "Base64 编码",
        "desc": "将文件中的变量编码为 Base64 格式",
        "module": "file_tools.base64_encoder",
        "func": "encode_file_variables",
        "args": [
            {"label": "选择要编码的文件", "type": "file", "param": "file_path"},
        ],
    },
    {
        "category": "文件工具",
        "name": "批量重命名",
        "desc": "使用正则表达式批量重命名文件夹中的文件",
        "module": "file_tools.batch_rename",
        "func": "rename_files",
        "args": [
            {"label": "选择目标文件夹", "type": "dir", "param": "directory"},
            {"label": "正则表达式匹配模式", "type": "string", "param": "pattern"},
            {"label": "替换字符串", "type": "string", "param": "replacement"},
        ],
    },
    {
        "category": "文件工具",
        "name": "Markdown 转 PDF",
        "desc": "使用 Pandoc 将 Markdown 文件转换为 PDF",
        "module": "file_tools.convert_md_to_pdf",
        "func": "markdown_to_pdf",
        "args": [
            {"label": "选择 Markdown 文件", "type": "file", "param": "input_md_file", "filetypes": [("Markdown files", "*.md")]},
            {"label": "保存 PDF 文件为", "type": "save", "param": "output_pdf_file", "filetypes": [("PDF files", "*.pdf")]},
        ],
    },
    {
        "category": "文件工具",
        "name": "清理 macOS 临时文件",
        "desc": "清理 macOS 系统中的临时文件（.DS_Store 等）",
        "module": "file_tools.macos_cleaner",
        "func": "clean_macos_temp_files",
        "args": [
            {"label": "选择要清理的文件夹", "type": "dir", "param": "directory"},
        ],
    },
    # -- 系统工具 --
    {
        "category": "系统工具",
        "name": "SCR 文件清理器",
        "desc": "后台守护进程，持续监控并清理 .scr 文件",
        "module": "system_tools.scr_cleaner",
        "func": "start_monitoring",
        "args": [
            {"label": "选择监控目录", "type": "dir", "param": "target_dir"},
        ],
        "terminal_only": True,
        "terminal_hint": "此工具以后台守护进程方式运行，请在终端中使用 Ctrl+C 停止。",
    },
    {
        "category": "系统工具",
        "name": "打开 Windows 时间设置",
        "desc": "打开 Windows 系统的日期和时间设置面板",
        "module": "system_tools.open_time_settings",
        "func": "open_date_time_settings",
        "args": [],
    },
    # -- 代码工具 --
    {
        "category": "代码工具",
        "name": "项目代码行数统计",
        "desc": "统计项目中各类型文件的代码行数",
        "module": "code_tools.line_counter",
        "func": "analyze_project",
        "args": [
            {"label": "选择项目文件夹", "type": "dir", "param": "project_path"},
        ],
    },
    # -- 音乐工具 --
    {
        "category": "音乐工具",
        "name": "NCM 文件解密",
        "desc": "批量解密网易云音乐 .ncm 加密文件",
        "module": "music_tools.ncm_decrypt",
        "func": "decrypt_ncm",
        "args": [
            {"label": "选择包含 .ncm 文件的文件夹", "type": "dir", "param": "directory_path"},
        ],
    },
]


# ---------------------------------------------------------------------------
# 颜色常量
# ---------------------------------------------------------------------------

CATEGORY_COLORS = {
    "图片处理": ("#e3f2fd", "#1565c0"),   # 浅蓝底 + 深蓝字
    "AI 工具":  ("#f3e5f5", "#7b1fa2"),   # 浅紫底 + 深紫字
    "文件工具": ("#e8f5e9", "#2e7d32"),   # 浅绿底 + 深绿字
    "系统工具": ("#fff3e0", "#e65100"),   # 浅橙底 + 深橙字
    "代码工具": ("#fce4ec", "#c62828"),   # 浅粉底 + 深红字
    "音乐工具": ("#e0f7fa", "#006064"),   # 浅青底 + 深青字
}
DEFAULT_CAT_COLOR = ("#f5f5f5", "#333333")


# ---------------------------------------------------------------------------
# GUI 应用
# ---------------------------------------------------------------------------

class PythonToolsApp:
    """PythonTools 图形界面主应用。"""

    def __init__(self, root):
        self.root = root
        self.root.title("PythonTools - 实用工具集")
        self.root.geometry("800x780")
        self.root.minsize(640, 560)
        self.root.configure(bg="#fafafa")

        self._build_ui()

    # ---- UI 构建 ----

    def _build_ui(self):
        # 顶部标题栏
        header = tk.Frame(self.root, bg="#fafafa")
        header.pack(fill=tk.X, padx=16, pady=(14, 6))

        tk.Label(
            header,
            text="PythonTools  实用工具集",
            font=("Helvetica", 22, "bold"),
            fg="#333",
            bg="#fafafa",
        ).pack(side=tk.LEFT)

        tk.Label(
            header,
            text="选择一个工具开始使用",
            font=("Helvetica", 12),
            fg="#999",
            bg="#fafafa",
        ).pack(side=tk.LEFT, padx=(16, 0), pady=(5, 0))

        # 分隔线
        sep = tk.Frame(self.root, height=1, bg="#e0e0e0")
        sep.pack(fill=tk.X, padx=16)

        # 工具卡片区域
        self.tools_frame = tk.Frame(self.root, bg="#fafafa")
        self.tools_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=8)

        # 按分类组织
        categories = {}
        for tool in TOOLS:
            categories.setdefault(tool["category"], []).append(tool)

        for cat_name, cat_tools in categories.items():
            self._add_category_section(cat_name, cat_tools)

        # 底部输出区域
        output_label = tk.Label(self.root, text="运行输出", font=("Helvetica", 10, "bold"), fg="#666", bg="#fafafa", anchor="w")
        output_label.pack(fill=tk.X, padx=18, pady=(4, 0))

        output_bg = tk.Frame(self.root, bg="#eceff1", highlightbackground="#ddd", highlightthickness=1)
        output_bg.pack(fill=tk.BOTH, padx=16, pady=(2, 4), ipady=1)

        self.output_text = tk.Text(
            output_bg,
            height=6,
            wrap=tk.WORD,
            font=("Menlo", 11),
            state=tk.DISABLED,
            relief=tk.FLAT,
            borderwidth=0,
            bg="#f5f5f5",
            fg="#333",
            padx=10,
            pady=8,
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

        # 底部状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = tk.Frame(self.root, bg="#fafafa")
        status_bar.pack(fill=tk.X, padx=16, pady=(0, 10))
        tk.Label(
            status_bar, textvariable=self.status_var,
            font=("Helvetica", 10), fg="#aaa", bg="#fafafa",
        ).pack(side=tk.LEFT)

    def _add_category_section(self, cat_name, tools):
        """添加一个分类区域，包含标题和两列工具按钮。"""
        bg_color, fg_color = CATEGORY_COLORS.get(cat_name, DEFAULT_CAT_COLOR)

        # 分类标题
        cat_header = tk.Frame(self.tools_frame, bg=bg_color)
        cat_header.pack(fill=tk.X, pady=(10, 2))

        tk.Label(
            cat_header,
            text=f"  {cat_name}",
            font=("Helvetica", 13, "bold"),
            fg=fg_color,
            bg=bg_color,
            anchor="w",
        ).pack(fill=tk.X, padx=10, pady=(7, 7))

        # 工具按钮网格（2 列）
        grid = tk.Frame(self.tools_frame, bg="#fafafa")
        grid.pack(fill=tk.X, padx=6)

        for i, tool in enumerate(tools):
            row = i // 2
            col = i % 2
            grid.rowconfigure(row, weight=1)
            grid.columnconfigure(col, weight=1, uniform="col")

            card = tk.Frame(
                grid,
                bg="white",
                highlightbackground="#e0e0e0",
                highlightthickness=1,
                padx=12,
                pady=10,
            )
            card.grid(row=row, column=col, padx=5, pady=4, sticky="nsew")

            btn = tk.Button(
                card,
                text=f"  {tool['name']}  ",
                font=("Helvetica", 13),
                bg="#ffffff",
                fg="#333",
                activebackground="#e3f2fd",
                activeforeground="#1565c0",
                relief=tk.FLAT,
                cursor="hand2",
                padx=4,
                pady=12,
                command=lambda t=tool: self._on_tool_click(t),
            )
            btn.pack(fill=tk.X)

            desc = tk.Label(
                card,
                text=tool["desc"],
                font=("Helvetica", 10),
                fg="#888",
                bg="white",
                wraplength=300,
                justify=tk.CENTER,
            )
            desc.pack(fill=tk.X, pady=(3, 0))

    # ---- 工具执行 ----

    def _on_tool_click(self, tool):
        """用户点击工具按钮时调用。"""
        if tool.get("terminal_only"):
            messagebox.showinfo(
                f"{tool['name']} — 终端工具",
                tool.get("terminal_hint", "此工具需要在终端中运行。"),
            )
            return

        # 收集参数
        kwargs = self._collect_args(tool)
        if kwargs is None:
            return  # 用户取消

        # 在后台线程中运行
        self._set_status(f"正在运行: {tool['name']}...")
        self._clear_output()

        thread = threading.Thread(
            target=self._run_tool,
            args=(tool, kwargs),
            daemon=True,
        )
        thread.start()

    def _collect_args(self, tool):
        """根据工具定义的参数列表，弹出对话框收集参数。"""
        kwargs = {}
        root = self.root

        for arg in tool.get("args", []):
            label = arg["label"]
            atype = arg["type"]
            param = arg["param"]
            required = arg.get("required", True)

            if atype == "file":
                filetypes = arg.get("filetypes", [("All files", "*.*")])
                path = filedialog.askopenfilename(parent=root, title=label, filetypes=filetypes)
                if not path and required:
                    return None
                if path:
                    kwargs[param] = path

            elif atype == "save":
                filetypes = arg.get("filetypes", [("All files", "*.*")])
                path = filedialog.asksaveasfilename(parent=root, title=label, filetypes=filetypes)
                if not path and required:
                    return None
                if path:
                    kwargs[param] = path

            elif atype == "dir":
                path = filedialog.askdirectory(parent=root, title=label)
                if not path and required:
                    return None
                if path:
                    kwargs[param] = path

            elif atype == "string":
                value = simpledialog.askstring(label, f"{label}:", parent=root)
                if not value and required:
                    return None
                if value:
                    kwargs[param] = value

        return kwargs

    def _run_tool(self, tool, kwargs):
        """在后台线程中导入并执行工具函数。"""
        stdout = io.StringIO()
        stderr = io.StringIO()

        try:
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = stdout
            sys.stderr = stderr

            try:
                module = __import__(tool["module"], fromlist=[tool["func"]])
                func = getattr(module, tool["func"])
                if kwargs:
                    func(**kwargs)
                else:
                    func()
            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr

            output = stdout.getvalue()
            errors = stderr.getvalue()

            self.root.after(0, lambda: self._show_result(tool["name"], output, errors, None))

        except Exception as e:
            output = stdout.getvalue()
            errors = stderr.getvalue()
            tb = traceback.format_exc()
            full_error = f"{errors}\n{tb}" if errors else tb
            self.root.after(0, lambda: self._show_result(tool["name"], output, full_error, str(e)))

    def _show_result(self, name, output, errors, exc_msg):
        """在主线程中显示工具运行结果。"""
        self._clear_output()

        lines = [f"--- {name} ---"]

        if output.strip():
            lines.append(output.rstrip())

        if errors.strip():
            lines.append(f"[stderr]\n{errors.rstrip()}")

        if exc_msg:
            lines.append(f"\n[错误] {exc_msg}")

        if not output.strip() and not errors.strip() and not exc_msg:
            lines.append("运行完成，无输出。")

        self._append_output("\n".join(lines))

        if exc_msg:
            self._set_status(f"运行失败: {name}")
        else:
            self._set_status(f"运行完成: {name}")

    # ---- 输出区域操作 ----

    def _clear_output(self):
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.configure(state=tk.DISABLED)

    def _append_output(self, text):
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)
        self.output_text.configure(state=tk.DISABLED)

    def _set_status(self, msg):
        self.status_var.set(msg)


# ---------------------------------------------------------------------------
# 入口
# ---------------------------------------------------------------------------

def main():
    """启动 GUI 主窗口。"""
    root = tk.Tk()
    app = PythonToolsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
