import subprocess
import os
from time import sleep

"""

打开 Windows 设置中的“日期和时间”页面的工具
"""
def open_date_time_settings():
    """
    自动打开 Windows 设置中的“日期和时间”页面。
    """
    print("正在尝试打开 Windows 日期和时间设置页面...")

    try:
        # 使用 start 命令和特定的 URI 来打开设置页面
        subprocess.run(["start", "ms-settings:dateandtime"], check=True, shell=True)
        print("已成功打开设置页面。")
    except Exception as e:
        print(f"打开设置页面时发生错误：{e}")


# 调用函数
if __name__ == "__main__":
    sleep(5)
    open_date_time_settings()