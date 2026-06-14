# CLAUDE.md - PythonTools 项目指南

本文件为 Claude Code 提供项目上下文和协作规范。

## 项目概述

PythonTools 是日常实用 Python 脚本的合集，按功能分为 7 个包。每个工具独立运行，也可作为库导入使用。

- **Python 版本**: 3.10+（见 `.python-version`）
- **虚拟环境**: `venv/`
- **主要入口**: `main.py`（交互式菜单）

## 项目结构

```
PythonTools/
├── main.py                  # 统一启动入口（交互式菜单）
├── image_tools/             # 图片 / 视频处理（5 个模块）
├── ai_tools/                # AI / LLM 工具（3 个模块）
├── file_tools/              # 文件操作工具（4 个模块）
├── system_tools/            # 系统工具（2 个模块）
├── code_tools/              # 代码分析（1 个模块）
├── music_tools/             # 音频处理（1 个模块）
├── VoxCpm/                  # 文字转语音（Streamlit Web UI）
└── archive/                 # 已归档的临时/废弃文件
```

每个工具包的结构：
- `__init__.py` — 使用 PEP 562 `__getattr__` 懒加载导出
- 每个模块都是独立脚本，可单独 `python -m <package>.<module>` 运行

## 开发规范

### 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 文件名 | 全小写 snake_case | `convert_jpg_to_png.py` |
| 函数名 | 全小写 snake_case，动词开头 | `convert_jpg_to_png()` |
| 变量名 | 全小写 snake_case | `input_file`, `output_path` |
| 常量 | 全大写下划线分隔 | `CORE_KEY`, `LANGUAGE_EXTENSIONS` |
| 类名 | PascalCase | （当前项目无类） |
| 包名 | 全小写 snake_case | `image_tools`, `ai_tools` |

### Docstring 格式

统一使用 **Google-style** docstring，必须包含以下部分（视实际情况）：

```python
def example_function(param1, param2, param3=None):
    """一句话描述函数的功能。

    可选：详细说明（如果功能复杂，需要额外解释）。

    Args:
        param1: 参数的说明。
        param2: 参数的说明。
        param3: 可选参数，默认值为 None。

    Returns:
        返回值的说明。如果无返回值则省略此节。

    Raises:
        FileNotFoundError: 说明何时抛出此异常。
        ValueError: 说明何时抛出此异常。
    """
```

### 导入顺序

按以下顺序排列，各组之间留一空行：

1. 标准库（`os`, `sys`, `re`, `json` 等）
2. 第三方库（`PIL`, `numpy`, `cv2`, `torch` 等）
3. 本地模块（相对导入）

### `__main__` 区块

- 移除硬编码路径，改为示例注释或通用参数
- 保留 `if __name__ == "__main__":` 结构，方便直接运行

## 包初始化规范

所有包的 `__init__.py` 必须使用 PEP 562 懒加载模式：

```python
"""包的一句话描述。"""

__all__ = ["function_a", "function_b"]


def __getattr__(name):
    if name == "function_a":
        from .module_a import function_a
        return function_a
    if name == "function_b":
        from .module_b import function_b
        return function_b
    raise AttributeError(f"module 'package_name' has no attribute {name!r}")
```

这样做的原因：很多工具依赖重型第三方库（如 `torch`、`transformers`），如果立即导入，缺失依赖时整个包都不可用。

## 添加新工具的步骤

1. **选择包**: 按功能归入对应的包（image_tools / ai_tools / file_tools / system_tools / code_tools / music_tools）
2. **创建文件**: 全小写 snake_case 命名
3. **编写模块**: 遵循命名规范 + Google-style docstring
4. **更新 `__init__.py`**: 添加懒加载条目
5. **更新 `main.py`**: 在 `TOOLS` 字典中添加菜单项，注意递增编号
6. **更新 `requirements.txt`**: 如果引入新依赖
7. **更新 README.md 和 CLAUDE.md**: 在工具列表中补充说明

## 测试

```bash
# 验证包可导入
python -c "import image_tools; print('OK')"

# 验证函数可访问
python -c "from image_tools import convert_jpg_to_png; print('OK')"

# 运行 main.py 菜单
python main.py

# 直接运行某个工具模块
python -m file_tools.base64_encoder
```

## 常见注意事项

- **不要**将工具路径硬编码在函数中，改为函数参数
- **不要**在 `__init__.py` 中直接导入模块（会触发懒加载失效）
- **新增依赖**时，在 `requirements.txt` 对应分类下添加注释说明用途
- **VoxCpm/** 是独立的 Streamlit 应用，启动方式为 `streamlit run VoxCpm/Voxcpm_test.py`
- **archive/** 存放已废弃或临时文件，不应包含仍在使用的工具
- **venv/** 和 **VoxCpm/pretrained_models/** 已在 `.gitignore` 中忽略
