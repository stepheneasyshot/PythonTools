# screen_recorder.py

import os
import threading
import time
import cv2
import numpy as np
from mss import mss

class ScreenRecorder:
    """
    一个用于录制屏幕视频的工具类。

    使用 mss 库捕获屏幕，并使用 OpenCV (cv2) 将其写入视频文件。
    """

    def __init__(self, output_dir="recordings", fps=15.0):
        """
        初始化屏幕录制器。

        Args:
            output_dir (str): 录制文件保存的目录。
            fps (float): 录制的帧率。
        """
        self.output_dir = output_dir
        self.fps = fps
        self._is_recording = False
        self._out = None
        self._video_file_path = None
        self._record_thread = None
        self._lock = threading.Lock()

        # 确保输出目录存在
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _record_screen_thread_func(self):
        """
        独立的线程函数，在后台执行屏幕录制。
        """
        try:
            with mss() as sct:
                monitor = sct.monitors[0]
                width, height = monitor["width"], monitor["height"]

                video_file_name = f"recording_{int(time.time())}.mp4"
                self._video_file_path = os.path.join(self.output_dir, video_file_name)
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')

                with self._lock:
                    self._out = cv2.VideoWriter(self._video_file_path, fourcc, self.fps, (width, height))
                    self._is_recording = True

                frame_interval = 1.0 / self.fps

                while self._is_recording:
                    loop_start_time = time.time()

                    screen_data = sct.grab(monitor)
                    frame = np.array(screen_data)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                    self._out.write(frame)

                    # 计算处理当前帧所花费的时间
                    elapsed_time = time.time() - loop_start_time

                    # 动态计算需要睡眠的时间，以保持帧率稳定
                    sleep_time = frame_interval - elapsed_time
                    if sleep_time > 0:
                        time.sleep(sleep_time)

        except Exception as e:
            print(f"Error during recording: {e}")
            with self._lock:
                self._is_recording = False
        finally:
            self._stop_writer()
            print("Recording thread stopped.")

    def _stop_writer(self):
        """
        停止 VideoWriter 对象并释放资源。
        """
        with self._lock:
            if self._out:
                self._out.release()
                self._out = None

    def start_recording(self):
        """
        开始屏幕录制。

        如果已经在录制，则不执行任何操作。
        """
        with self._lock:
            if self._is_recording:
                return "Already recording."

            self._record_thread = threading.Thread(target=self._record_screen_thread_func)
            self._record_thread.start()
            return "Recording started!"

    def stop_recording(self):
        """
        停止屏幕录制并返回录制文件的路径。

        如果未在录制，则返回 None。
        """
        with self._lock:
            if not self._is_recording:
                return None

            # 设置停止标志
            self._is_recording = False

        # 等待录制线程结束
        if self._record_thread and self._record_thread.is_alive():
            self._record_thread.join()

        return self._video_file_path

    def get_file_path(self):
        """
        获取当前录制文件的路径。
        """
        return self._video_file_path

    def is_recording(self):
        """
        检查当前是否正在录制。
        """
        return self._is_recording
