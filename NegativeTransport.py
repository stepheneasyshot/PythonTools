import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# 设置页面配置
st.set_page_config(page_title="胶片负片转正片工具", layout="wide")


def adjust_levels(channel, low_perc=1, high_perc=99):
    """通过百分比裁剪实现黑白场拉伸"""
    low_val, high_val = np.percentile(channel, [low_perc, high_perc])
    channel = (channel - low_val) / (high_val - low_val)
    return np.clip(channel, 0, 1)


def process_image(img_array, low_p, high_p, sat_mult):
    """核心处理逻辑"""
    # 1. 归一化 (转换为 float32)
    img = img_array.astype(np.float32) / 255.0

    # 2. 去除橙色色罩
    mask_color = np.array([np.percentile(img[:, :, i], 98) for i in range(3)])
    img_normalized = np.clip(img / mask_color, 0, 1)

    # 3. 反转
    img_inverted = 1.0 - img_normalized

    # 4. 各通道独立黑白场拉伸
    for i in range(3):
        img_inverted[:, :, i] = adjust_levels(img_inverted[:, :, i], low_perc=low_p, high_perc=high_p)

    # 5. 增强饱和度 (HSV 空间调整)
    img_uint8 = (img_inverted * 255).astype(np.uint8)
    img_hsv = cv2.cvtColor(img_uint8, cv2.COLOR_RGB2HSV).astype(np.float32)
    img_hsv[:, :, 1] *= sat_mult
    img_hsv[:, :, 1] = np.clip(img_hsv[:, :, 1], 0, 255)
    img_inverted = cv2.cvtColor(img_hsv.astype(np.uint8), cv2.COLOR_HSV2RGB).astype(np.float32) / 255.0

    # 6. 对比度增强 (CLAHE)
    img_lab = cv2.cvtColor((img_inverted * 255).astype(np.uint8), cv2.COLOR_RGB2Lab)
    l, a, b = cv2.split(img_lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    img_final = cv2.merge((l, a, b))
    img_final = cv2.cvtColor(img_final, cv2.COLOR_Lab2RGB)

    return img_final


# --- UI 界面 ---
st.title("🎞️ 胶片负片转换助手")
st.markdown("上传你的底片扫描件（JPG/PNG），实时调整参数并下载正片。")

# 侧边栏参数控制
with st.sidebar:
    st.header("调色参数")
    low_p = st.slider("暗部裁剪 (Low Percentile)", 0.0, 5.0, 2.0, 0.1)
    high_p = st.slider("亮部裁剪 (High Percentile)", 95.0, 100.0, 98.0, 0.1)
    sat_mult = st.slider("饱和度倍数", 0.5, 3.0, 1.4, 0.1)
    st.info("提示：若画面发灰，请尝试增大暗部裁剪或减小亮部裁剪。")

uploaded_file = st.file_uploader("选择负片图像...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 将上传的文件转为 OpenCV 格式
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    # 直接读取为 RGB
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("原始负片")
        st.image(image, use_container_width=True)

    with col2:
        st.subheader("转换结果")
        with st.spinner('转换中...'):
            result = process_image(image, low_p, high_p, sat_mult)
            st.image(result, use_container_width=True)

            # 准备下载
            result_pil = Image.fromarray(result)
            buf = io.BytesIO()
            result_pil.save(buf, format="JPEG", quality=95)
            byte_im = buf.getvalue()

            st.download_button(
                label="下载正片图像",
                data=byte_im,
                file_name="converted_positive.jpg",
                mime="image/jpeg"
            )