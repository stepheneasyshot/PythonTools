import cv2
import numpy as np
import os


def adjust_levels(channel, low_perc=1, high_perc=99):
    """
    通过百分比裁剪实现黑白场拉伸，解决发灰问题
    """
    low_val, high_val = np.percentile(channel, [low_perc, high_perc])
    # 线性映射 low_val -> 0, high_val -> 1
    channel = (channel - low_val) / (high_val - low_val)
    return np.clip(channel, 0, 1)


def process_negative_pro(image_path, output_path):
    # 1. 加载图像 (保持 16bit 精度处理)
    img = cv2.imread(image_path)
    if img is None:
        print("无法加载图像。")
        return

    img = img.astype(np.float32) / 255.0

    # 2. 去除橙色色罩 (改进：采样边缘或最亮区域)
    # 胶片边缘通常是纯色罩颜色，如果没有边缘，取各通道 98% 分位数作为参考
    mask_color = np.array([np.percentile(img[:, :, i], 98) for i in range(3)])
    img_normalized = np.clip(img / mask_color, 0, 1)

    # 3. 反转
    img_inverted = 1.0 - img_normalized

    # 4. 核心优化：各通道独立黑白场拉伸 (解决偏色和发灰)
    # low_perc 越小，暗部细节越多；high_perc 越大，亮部越不容易过曝
    for i in range(3):
        img_inverted[:, :, i] = adjust_levels(img_inverted[:, :, i], low_perc=2, high_perc=98)

    # 5. 增强饱和度 (HSV 空间调整)
    img_hsv = cv2.cvtColor((img_inverted * 255).astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
    # 提升饱和度通道 (S)，通常增加 1.2-1.5 倍
    img_hsv[:, :, 1] *= 1.4
    img_hsv[:, :, 1] = np.clip(img_hsv[:, :, 1], 0, 255)
    img_inverted = cv2.cvtColor(img_hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32) / 255.0

    # 6. 对比度增强 (CLAHE 限制对比度自适应直方图均衡化)
    # 这比单纯的 Gamma 效果更接近专业扫描仪
    img_lab = cv2.cvtColor((img_inverted * 255).astype(np.uint8), cv2.COLOR_BGR2Lab)
    l, a, b = cv2.split(img_lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    img_final = cv2.merge((l, a, b))
    img_final = cv2.cvtColor(img_final, cv2.COLOR_Lab2BGR)

    # 7. 保存结果
    cv2.imwrite(output_path, img_final)
    print(f"优化处理完成: {output_path}")


if __name__ == "__main__":
    # 迭代某一个文件夹下，所有图片都转换
    work_space = os.path.expanduser("~/Downloads/")
    for file_name in os.listdir(work_space):
        if file_name.endswith(".jpg") or file_name.endswith(".png"):
            input_p = os.path.join(work_space, file_name)
            output_p = os.path.join(work_space, file_name.replace(".jpg", "_output.jpg").replace(".png", "_output.png"))
            process_negative_pro(input_p, output_p)
