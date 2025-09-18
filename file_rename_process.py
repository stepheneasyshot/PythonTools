import io
import logging
import os
import re

"""

文件批量快速重命名

"""

def rename_files(directory, pattern, replacement):
    """
    重命名目录下所有匹配指定模式的文件。

    :param directory: 包含文件的目录路径
    :param pattern: 匹配文件名的正则表达式模式
    :param replacement: 替换匹配部分的字符串
    """
    for filename in os.listdir(directory):
        if re.search(pattern, filename):
            new_filename = re.sub(pattern, replacement, filename)
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
            print(f"Renamed: {filename} -> {new_filename}")

if __name__ == "__main__":
    # 示例用法
    directory = "/path/to/your/directory"  # 替换为你的目录路径
    pattern = r"old_name"  # 替换为你要匹配的文件名模式
    replacement = "new_name"  # 替换为你要替换的字符串

    rename_files(directory, pattern, replacement)
