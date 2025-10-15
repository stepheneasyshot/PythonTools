# -*- coding: utf-8 -*-

import os
import sys
from collections import defaultdict

# --- 配置区 ---
# 在这里定义你想要统计的文件类型及其对应的语言名称
# 格式：'语言名称': ('.后缀1', '.后缀2', ...)
# 我已经为你预设了Android、Python和C++常用的文件类型
FILE_EXTENSIONS_TO_COUNT = {
    'Kotlin': ('.kt', '.kts'),
    'Java': ('.java',),
    'XML': ('.xml',),
    'Python': ('.py',),
    'C/C++': ('.c', '.cpp', '.h', '.hpp'),
    'Groovy': ('.groovy',),
}

# 定义单行注释的起始符，脚本会忽略以这些符号开头的行
# 注意：这里暂时没有处理多行注释(/* ... */)和行内注释，旨在保持脚本简洁
SINGLE_LINE_COMMENT_PREFIXES = ('#', '//')


# --- 核心功能 ---

def count_line(file_path):
    """
    统计单个文件的有效代码行数。
    会忽略空行和以特定前缀开头的注释行。
    """
    count = 0
    try:
        # 使用 utf-8 编码打开文件，这是最常见的代码文件编码
        # errors='ignore' 可以避免因个别文件编码问题导致程序中断
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                # 去除行首和行尾的空白字符
                stripped_line = line.strip()
                # 如果处理后不为空，并且不是以单行注释开头，则计数+1
                if stripped_line and not stripped_line.startswith(SINGLE_LINE_COMMENT_PREFIXES):
                    count += 1
    except Exception as e:
        print(f"无法读取文件 {file_path}: {e}")
    return count


def main(project_path):
    """
    主函数，遍历项目路径并统计代码行数。
    """
    # 检查路径是否存在且为目录
    if not os.path.isdir(project_path):
        print(f"错误：提供的路径 '{project_path}' 不是一个有效的目录。")
        return

    # 使用 defaultdict 可以方便地累加计数，无需检查键是否存在
    line_counts = defaultdict(int)
    file_counts = defaultdict(int)

    print(f"开始扫描项目目录：{project_path}\n")

    # os.walk 会递归遍历目录下的所有子目录和文件
    for root, _, files in os.walk(project_path):
        for file in files:
            # 遍历我们定义的文件类型
            for lang, extensions in FILE_EXTENSIONS_TO_COUNT.items():
                if file.endswith(extensions):
                    # 如果文件后缀匹配，则进行统计
                    file_path = os.path.join(root, file)
                    lines = count_line(file_path)
                    line_counts[lang] += lines
                    file_counts[lang] += 1
                    # 找到匹配的语言后就跳出内层循环，避免重复计数
                    break

    # --- 打印结果 ---
    print("--- 代码行数统计结果 ---")

    # 准备表格数据
    # 表头
    table_data = [["语言类型", "文件数量", "有效代码行数"]]
    total_lines = 0
    total_files = 0

    # 排序使输出更美观
    sorted_langs = sorted(line_counts.keys())

    for lang in sorted_langs:
        lines = line_counts[lang]
        files = file_counts[lang]
        table_data.append([lang, str(files), str(lines)])
        total_lines += lines
        total_files += files

    # 计算每列的最大宽度以便对齐
    col_widths = [max(len(cell) for cell in col) for col in zip(*table_data)]

    # 打印表头和分隔线
    header = " | ".join(f"{h:<{w}}" for h, w in zip(table_data[0], col_widths))
    print(header)
    print("-+-".join("-" * w for w in col_widths))

    # 打印数据行
    for row in table_data[1:]:
        print(" | ".join(f"{cell:<{w}}" for cell, w in zip(row, col_widths)))

    # 打印总计
    print("-" * len(header))
    total_row = ["总计", str(total_files), str(total_lines)]
    print(" | ".join(f"{cell:<{w}}" for cell, w in zip(total_row, col_widths)))
    print("\n统计完成！")


if __name__ == "__main__":
    # 从命令行获取第一个参数作为项目路径
    # sys.argv[0] 是脚本本身的名称
    if len(sys.argv) < 2:
        # 如果用户没有提供路径，打印使用说明
        print("使用方法: python count_loc.py <你的项目路径>")
        # 你也可以将当前目录作为默认路径
        # print("未提供路径，将使用当前目录作为项目路径。")
        # project_directory = "."
        sys.exit(1)  # 退出程序

    project_directory = sys.argv[1]
    main(project_directory)