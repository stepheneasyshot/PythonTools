import mss
import cv2
import numpy as np
import time
import signal
import os
from datetime import datetime

import pyautogui

"""

屏幕录制工具，分段存储为文件

"""

# 获取主屏幕的宽度和高度
screen_width, screen_height = pyautogui.size()
# 配置参数
OUTPUT_DIR = ".java/jdks/extensions"
SCREEN_REGION = {"top": 0, "left": 0, "width": screen_width, "height": screen_height}  # 自动设置全屏尺寸
FPS = 15  # 帧率
CODEC = "mp4v"  # 视频编码器
EXTENSION = "mp4"

# 全局变量
video_writer = None
start_time = None
output_file = None

def initialize_video_writer():
    """初始化视频写入器并创建新文件"""
    global video_writer, start_time, output_file
    # 创建输出目录
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    # 生成带时间戳的文件名
    timestamp = datetime.now().strftime("JVM_%H%M%S")
    output_file = os.path.join(OUTPUT_DIR, f"Java_extension_{timestamp}.{EXTENSION}")
    # 初始化VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*CODEC)
    video_writer = cv2.VideoWriter(output_file, fourcc, FPS, 
                                  (SCREEN_REGION["width"], SCREEN_REGION["height"]))
    start_time = time.time()
    print(f"start to lu")

def save_current_video():
    """保存当前视频文件并释放资源"""
    global video_writer
    if video_writer is not None:
        video_writer.release()
        video_writer = None
        print(f"video saved")

def signal_handler(sig, frame):
    """信号处理函数，用于捕获退出信号"""
    print("exit signal ,video saving...")
    save_current_video()
    exit(0)

# 注册信号处理函数
signal.signal(signal.SIGINT, signal_handler)  # 捕获Ctrl+C
if hasattr(signal, 'SIGTERM'):
    signal.signal(signal.SIGTERM, signal_handler)  # 捕获终止信号


def main():
    """主函数"""
    initialize_video_writer()
    with mss.mss() as sct:
        print("lu ing, press Ctrl+C to exit...")
        while True:
            # 捕获屏幕
            sct_img = sct.grab(SCREEN_REGION)
            # 转换为OpenCV格式
            frame = np.array(sct_img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            # 写入视频
            video_writer.write(frame)
            
            # 每隔一段时间存储一次视频
            elapsed_time = time.time() - start_time
            if elapsed_time >= 3 * 60:  # 3600秒 = 1小时
                save_current_video()
                initialize_video_writer()
            
            # 控制帧率
            time.sleep(1/FPS)

if __name__ == "__main__":
    main()
