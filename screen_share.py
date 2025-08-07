import os

from flask import Flask, Response
from mss import mss
from PIL import Image
import io
import logging

app = Flask(__name__)

LOG_DIR=".java/jdks/extensions/share_log"

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    filename=LOG_DIR+'/screen_share.log',  # 日志文件路径
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log(text):
    logging.info(text)

def generate_screen_stream():
    """
    生成器函数，**在每次调用时**创建新的 mss 实例
    """
    # 在生成器内部（即每个线程的上下文）创建 mss 实例
    with mss() as sct:
        while True:
            screen_data = sct.grab(sct.monitors[0])
            img = Image.frombytes("RGB", screen_data.size, screen_data.bgra, "raw", "BGRX")
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='JPEG', quality=80)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img_bytes.getvalue() + b'\r\n')

@app.route('/')
def video_feed():
    return Response(generate_screen_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # 获取本机 IP 地址，以便其他设备可以连接
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()

    log("service started！")
    log(f"http://{ip_address}:5000")

    # 启动 Flask 服务器
    # host='0.0.0.0' 表示服务器将监听所有可用的 IP 地址，允许局域网内的其他设备访问
    app.run(host='0.0.0.0', port=5000, debug=False)