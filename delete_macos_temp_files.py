import os
import time
import logging
from datetime import datetime

"""

删除目录中以 ._ 开头的，和 ".DS_Store"文件

"""

def delete_macos_temp_files(directory):
    """
    迭代递归删除目录中以 ._ 开头的文件

    :param directory: 目录路径
    """
    # 检查目录是否存在
    if not os.path.exists(directory):
        print(f'directory {directory} not exists')
        return

    # 遍历目录下所有文件
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if item.startswith('._'):
            try:
                os.remove(item_path)
                print(f'deleted file: {item_path}')
            except Exception as e:
                print(f'delete file {item_path} failed: {str(e)}')
        elif item == '.DS_Store':
            try:
                os.remove(item_path)
                print(f'deleted file: {item_path}')
            except Exception as e:
                print(f'delete file {item_path} failed: {str(e)}')
        elif os.path.isdir(item_path):
            delete_macos_temp_files(item_path)

if __name__ == '__main__':
    # 要删除的目录
    directory_to_clean = 'E:\\ExpoTranslate\\ICAR03T\\LAO\\Car461_LAO_202510241509_codestringmodify'
    # 调用函数删除文件
    delete_macos_temp_files(directory_to_clean)
