from time import sleep

from PIL import ImageGrab

# 捕获整个屏幕
print("等待10秒")
sleep(10)
print("开始截图")
screenshot = ImageGrab.grab()
screenshot.save("full_screen_capture.png")
print("已捕获整个屏幕并保存为 full_screen_capture.png")
