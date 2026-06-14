"""Convert film negative scans to positive images.

A Streamlit-based web app that processes scanned film negatives by removing
the orange mask, inverting colors, and enhancing contrast/saturation.
"""

import io

import cv2
import numpy as np
from PIL import Image
import streamlit as st


def adjust_levels(channel, low_perc=1, high_perc=99):
    """Stretch black and white levels by percentile-based clipping.

    Args:
        channel: Single-channel image array (float).
        low_perc: Low percentile for black point. Defaults to 1.
        high_perc: High percentile for white point. Defaults to 99.

    Returns:
        Array with values clipped and scaled to [0, 1].
    """
    low_val, high_val = np.percentile(channel, [low_perc, high_perc])
    channel = (channel - low_val) / (high_val - low_val)
    return np.clip(channel, 0, 1)


def process_image(img_array, low_p, high_p, sat_mult):
    """Convert a film negative scan to a positive image.

    Steps: normalize, remove orange mask, invert, level adjust,
    saturation boost, CLAHE contrast enhancement.

    Args:
        img_array: RGB image array (uint8).
        low_p: Low percentile for dark clipping.
        high_p: High percentile for bright clipping.
        sat_mult: Saturation multiplier (>1 increases saturation).

    Returns:
        Processed RGB image array (uint8).
    """
    img = img_array.astype(np.float32) / 255.0

    mask_color = np.array([np.percentile(img[:, :, i], 98) for i in range(3)])
    img_normalized = np.clip(img / mask_color, 0, 1)

    img_inverted = 1.0 - img_normalized

    for i in range(3):
        img_inverted[:, :, i] = adjust_levels(img_inverted[:, :, i], low_perc=low_p, high_perc=high_p)

    img_uint8 = (img_inverted * 255).astype(np.uint8)
    img_hsv = cv2.cvtColor(img_uint8, cv2.COLOR_RGB2HSV).astype(np.float32)
    img_hsv[:, :, 1] *= sat_mult
    img_hsv[:, :, 1] = np.clip(img_hsv[:, :, 1], 0, 255)
    img_inverted = cv2.cvtColor(img_hsv.astype(np.uint8), cv2.COLOR_HSV2RGB).astype(np.float32) / 255.0

    img_lab = cv2.cvtColor((img_inverted * 255).astype(np.uint8), cv2.COLOR_RGB2Lab)
    l, a, b = cv2.split(img_lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    img_final = cv2.merge((l, a, b))
    img_final = cv2.cvtColor(img_final, cv2.COLOR_Lab2RGB)

    return img_final


def run_app():
    """Launch the Streamlit web app for negative-to-positive conversion."""
    st.set_page_config(page_title="Film Negative Converter", layout="wide")

    st.title("Film Negative Converter")
    st.markdown("Upload film negative scans (JPG/PNG), adjust parameters, and download positives.")

    with st.sidebar:
        st.header("Adjustment Parameters")
        low_p = st.slider("Dark Clipping (Low %)", 0.0, 5.0, 2.0, 0.1)
        high_p = st.slider("Bright Clipping (High %)", 95.0, 100.0, 98.0, 0.1)
        sat_mult = st.slider("Saturation Multiplier", 0.5, 3.0, 1.4, 0.1)
        st.info("If the image looks flat, increase dark clipping or decrease bright clipping.")

    uploaded_file = st.file_uploader("Choose a negative image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original Negative")
            st.image(image, use_container_width=True)

        with col2:
            st.subheader("Converted Positive")
            with st.spinner("Processing..."):
                result = process_image(image, low_p, high_p, sat_mult)
                st.image(result, use_container_width=True)

                result_pil = Image.fromarray(result)
                buf = io.BytesIO()
                result_pil.save(buf, format="JPEG", quality=95)
                byte_im = buf.getvalue()

                st.download_button(
                    label="Download Positive Image",
                    data=byte_im,
                    file_name="converted_positive.jpg",
                    mime="image/jpeg",
                )


if __name__ == "__main__":
    run_app()