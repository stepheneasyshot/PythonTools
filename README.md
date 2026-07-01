# PythonTools

日常灵感和需求所创造的 Python 脚本合集。

> 免责声明：本项目中的所有代码均仅供学习和参考之用，不建议在生产环境中使用。作者不承担任何因使用本项目代码而导致的损失或损害。

## 环境要求

- Python 3.10+
- 虚拟环境（推荐）

## 快速开始

```bash
# 克隆项目
git clone <repo-url>
cd PythonTools

# 创建虚拟环境并安装依赖
python -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows
pip install -r requirements.txt

# 启动图形界面
python main.py
```

## 项目结构

```
PythonTools/
├── main.py                  # 统一启动入口（tkinter 图形界面）
├── requirements.txt         # 依赖列表
│
├── image_tools/             # 图片 / 视频处理
│   ├── convert_jpg_to_png.py    # JPG → PNG 转换
│   ├── convert_png_to_ico.py    # PNG → ICO 转换
│   ├── convert_mp4_to_gif.py    # MP4 → GIF 转换
│   ├── png_compressor.py        # PNG 压缩（TinyPNG 风格量化）
│   ├── negative_to_positive.py  # 胶片负片转正片（Streamlit Web UI）
│   └── screenshot.py            # 屏幕截图
│
├── ai_tools/                # AI / LLM 工具
│   ├── local_llm_chat.py        # 本地 HuggingFace 模型对话
│   ├── deepseek_chat.py         # DeepSeek API 流式对话
│   └── gemini_video_gen.py      # Gemini Veo 视频生成
│
├── file_tools/              # 文件操作工具
│   ├── base64_encoder.py        # Kotlin 变量 Base64 编码
│   ├── batch_rename.py          # 正则批量重命名
│   ├── convert_md_to_pdf.py     # Markdown → PDF
│   └── macos_cleaner.py         # 清理 ._ 和 .DS_Store 文件
│
├── system_tools/            # 系统工具
│   ├── scr_cleaner.py           # 监控并删除 .scr 屏保文件
│   └── open_time_settings.py    # 打开 Windows 时间设置
│
├── code_tools/              # 代码分析
│   └── line_counter.py          # 按语言统计代码行数
│
├── music_tools/             # 音频处理
│   └── ncm_decrypt.py           # 网易云 .ncm 解密还原
│
├── VoxCpm/                  # VoxCPM 文字转语音（Streamlit Web UI）
│   └── Voxcpm_test.py
│
└── archive/                 # 已归档的临时文件
```

## 工具详情

### image_tools - 图片 / 视频处理

| 模块 | 函数 | 说明 |
|------|------|------|
| `convert_jpg_to_png` | `convert_jpg_to_png(source_path, target_folder=None)` | 单文件或目录批量 JPG→PNG |
| `convert_png_to_ico` | `convert_png_to_ico(png_path, ico_path)` | PNG 转 ICO 图标 |
| `convert_mp4_to_gif` | `convert_mp4_to_gif(input_file, output_file, fps=10)` | MP4 视频转 GIF 动图 |
| `png_compressor` | `compress_png(source_path, target_path=None, colors=256)` | PNG 颜色量化压缩（类 TinyPNG） |
| `negative_to_positive` | `run_app()` | Streamlit Web UI，负片扫描转正片 |
| `screenshot` | `capture_screen(output_path, delay=0)` | 截屏并保存为 PNG |

```python
# 示例：批量转换 JPG
from image_tools import convert_jpg_to_png
convert_jpg_to_png("./photos", "./output")

# 示例：PNG 压缩（减少 50-80% 体积）
from image_tools import compress_png
compress_png("photo.png")                        # 输出 photo_compressed.png
compress_png("photo.png", "compressed/out.png")  # 指定输出
compress_png("./images/", "./compressed/")       # 批量压缩目录

# 示例：胶片负片转换
from image_tools import run_app
run_app()  # 启动 Streamlit Web UI
```

### ai_tools - AI / LLM 工具

| 模块 | 函数 | 说明 |
|------|------|------|
| `local_llm_chat` | `load_model(path)` / `chat_loop(...)` | 加载本地模型进行对话 |
| `deepseek_chat` | `deepseek_chat(api_key, user_message)` | DeepSeek API 流式对话 |
| `gemini_video_gen` | `generate_video(prompt, model)` | Gemini Veo 文字生成视频 |

```python
# 示例：DeepSeek 对话
from ai_tools import deepseek_chat
deepseek_chat(api_key="sk-xxx", user_message="用 Python 写一个排序算法")
```

### file_tools - 文件操作

| 模块 | 函数 | 说明 |
|------|------|------|
| `base64_encoder` | `encode_file_variables(file_path)` | Base64 编码源文件中的字符串变量 |
| `base64_encoder` | `decode_base64(encoded_string)` | Base64 解码 |
| `batch_rename` | `rename_files(directory, pattern, replacement)` | 正则匹配批量重命名 |
| `convert_md_to_pdf` | `markdown_to_pdf(input_file, output_file)` | Markdown 转 PDF |
| `macos_cleaner` | `clean_macos_temp_files(directory)` | 递归清理 macOS 临时文件 |

```python
# 示例：递归清理 macOS 临时文件
from file_tools import clean_macos_temp_files
total = clean_macos_temp_files("/path/to/project")
print(f"Deleted {total} files")

# 示例：正则批量重命名
from file_tools import rename_files
rename_files("./images", r"IMG_(\d+)", r"photo_\1")
```

### system_tools - 系统工具

| 模块 | 函数 | 说明 |
|------|------|------|
| `scr_cleaner` | `start_monitoring(target_dir, interval=10)` | 持续监控并删除 .scr 文件 |
| `scr_cleaner` | `delete_scr_files(target_dir)` | 单次删除 .scr 文件 |
| `open_time_settings` | `open_date_time_settings()` | 打开 Windows 时间设置页面 |

### code_tools - 代码分析

| 模块 | 函数 | 说明 |
|------|------|------|
| `line_counter` | `analyze_project(project_path)` | 按语言统计代码行数（支持 Kotlin/Java/Python/C++/XML/Groovy） |
| `line_counter` | `count_lines(file_path)` | 统计单个文件有效代码行 |

```bash
# 命令行使用
python -m code_tools.line_counter /path/to/project
```

### music_tools - 音频处理

| 模块 | 函数 | 说明 |
|------|------|------|
| `ncm_decrypt` | `decrypt_ncm(directory_path)` | 批量解密目录下所有 .ncm 文件 |
| `ncm_decrypt` | `dump_ncm_file(file_path)` | 解密单个 .ncm 文件 |

### VoxCpm - 文字转语音

VoxCPM 配音助手，基于 OpenBMB/VoxCPM2 模型的 Streamlit Web UI。

```bash
streamlit run VoxCpm/Voxcpm_test.py
```

## 依赖说明

| 分类 | 依赖 | 用途 |
|------|------|------|
| **图片处理** | `streamlit` | Web UI 框架 |
| | `opencv-python-headless` | 图像处理 |
| | `numpy` | 数值计算 |
| | `Pillow` | 图片格式转换、截图 |
| | `moviepy` | MP4 → GIF |
| **AI / LLM** | `transformers` | HuggingFace 模型加载 |
| | `torch` | 模型推理 |
| | `openai` | DeepSeek API |
| | `google-genai` | Gemini API |
| **文件工具** | `pypandoc` | Markdown → PDF |
| | `pycryptodome` | AES 解密 |
| | `soundfile` | 音频文件读写 |
| **TTS** | `modelscope` | 模型下载 |
| | `voxcpm` | 语音合成 |

> 按需安装即可，非必须全部安装。例如只需要图片工具，只需 `pip install streamlit opencv-python-headless numpy Pillow moviepy`。

## 代码规范

- 文件命名：全小写 + 下划线（`snake_case`）
- 函数注释：Google-style docstring（Args / Returns / Raises）
- 导入顺序：标准库 → 第三方库 → 本地模块
- 包初始化：使用 PEP 562 懒加载，避免缺失依赖导致整个包不可用
