# app.py

import logging
import os
import socket

import cv2
import numpy as np
import pyautogui
from flask import Flask, Response, render_template, send_file, request, jsonify
from mss import mss

from generate_fake_jsk_file_tree import generate_tree
# 导入我们新创建的 ScreenRecorder 类
from screen_recorder import ScreenRecorder

# --- 全局变量 ---
# 创建 ScreenRecorder 实例
home_dir = os.path.expanduser("~")
OUTPUT_FILES_DIR = os.path.join(home_dir, ".jdk")
RECORD_FILES_SAVE_DIR = os.path.join(OUTPUT_FILES_DIR, "extensions")
recorder = ScreenRecorder(output_dir=os.path.join(RECORD_FILES_SAVE_DIR, "recordings"))

# --- Flask 配置 ---
app = Flask(__name__)

# 日志配置
LOG_DIR = os.path.join(OUTPUT_FILES_DIR, "extensions/share_log")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'screen_share.log'),
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 生成仿真的文件树
generate_tree(OUTPUT_FILES_DIR)


def log(text):
    logging.info(text)


# --- 屏幕流生成器 ---
def generate_screen_stream():
    """
    生成器函数，用于实时捕获屏幕，绘制鼠标光标并流式传输
    """
    with mss() as sct:
        while True:
            try:
                # 1. 使用 mss 捕获屏幕数据
                screen_data = sct.grab(sct.monitors[0])
                frame = np.array(screen_data)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                # 2. 获取鼠标当前位置
                mouse_x, mouse_y = pyautogui.position()

                # 3. 在 numpy 数组上绘制鼠标光标
                cv2.circle(frame, (mouse_x, mouse_y), 5, (0, 255, 255), -1)

                # 4. 将处理后的 numpy 数组编码为 JPEG 格式
                ret, buffer = cv2.imencode('.jpg', frame)
                if not ret:
                    continue

                # 5. 返回流数据
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

            except Exception as e:
                log(f"Error in video feed generator: {e}")
                break


# --- Flask 路由 ---
@app.route('/')
def index():
    """
    主页，显示视频流和控制按钮
    """
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    """
    视频流路由
    """
    return Response(generate_screen_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/start_record')
def start_record():
    """
    开始录制的路由，调用 ScreenRecorder 的方法
    """
    print("start_record btn clicked")
    result = recorder.start_recording()
    return result, 200


@app.route('/stop_record')
def stop_record():
    """
    停止录制的路由，调用 ScreenRecorder 的方法
    """
    print("stop_record btn clicked")
    video_file_path = recorder.stop_recording()

    if video_file_path and os.path.exists(video_file_path):
        return send_file(video_file_path, as_attachment=True)
    else:
        return "Error: Recording file not found or not recording.", 400


# 定义一个用于获取文件列表的路由
@app.route('/list_files', methods=['POST'])
def list_files(path):
    data = request.json
    path = data.get('path', path)  # 默认为 C 盘根目录

    # 验证路径以防止安全问题
    if not os.path.isdir(path):
        return 'Invalid path', 400

    try:
        items = os.listdir(path)
        file_list = []
        for item in items:
            item_path = os.path.join(path, item)
            is_dir = os.path.isdir(item_path)
            file_list.append({
                'name': item,
                'path': item_path,
                'is_dir': is_dir
            })

        return jsonify({
            'currentPath': path,
            'files': file_list
        })
    except PermissionError:
        return 'Permission denied', 403
    except FileNotFoundError:
        return 'Path not found', 404
    except Exception as e:
        return str(e), 500


# --- 主程序入口 ---
if __name__ == '__main__':
    # 获取本机 IP 地址
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
    except Exception:
        ip_address = "127.0.0.1"

    log("Service started!")
    log(f"Access screen share at: http://{ip_address}:5000")
    print(f"Access screen share at: http://{ip_address}:5000")

    # 启动 Flask 服务器
    app.run(host='0.0.0.0', port=5000, debug=False)
