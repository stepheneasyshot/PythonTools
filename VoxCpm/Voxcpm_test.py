# streamlit run
from pathlib import Path

import soundfile as sf
import streamlit as st

SCRIPT_DIR = Path(__file__).resolve().parent
MODEL_DIR = SCRIPT_DIR / "pretrained_models" / "VoxCPM2"
OUTPUT_DIR = SCRIPT_DIR

st.set_page_config(page_title="VoxCPM 配音助手", page_icon="🎙️", layout="wide")


@st.cache_resource(show_spinner="正在下载并加载模型，首次启动可能需要几分钟...")
def load_model():
    from modelscope import snapshot_download
    from voxcpm import VoxCPM

    if not (MODEL_DIR / "config.json").exists():
        snapshot_download("OpenBMB/VoxCPM2", local_dir=str(MODEL_DIR))

    return VoxCPM.from_pretrained(str(MODEL_DIR), load_denoiser=False)


def build_target_text(voice_character: str, content: str) -> str:
    voice = voice_character.strip()
    text = content.strip()
    if voice:
        return f"({voice}){text}"
    return text


if "output_count" not in st.session_state:
    st.session_state.output_count = 1

st.title("🎙️ VoxCPM 配音助手")
st.markdown("调整角色声音特征与台词内容，一键生成配音音频。")

VOICE_PRESETS = {
    "自定义": "",
    "成熟女性 · 慵懒害羞": "Sultry and shy mature female voice",
    "年轻女性 · 温柔": "Warm and gentle young female voice",
    "成熟男性 · 低沉": "Deep and calm mature male voice",
    "年轻男性 · 活泼": "Energetic and cheerful young male voice",
    "女性 · 轻声耳语": "Soft and whispering female voice",
}

if "last_preset" not in st.session_state:
    st.session_state.last_preset = "成熟女性 · 慵懒害羞"

with st.sidebar:
    st.header("声音设置")
    preset_name = st.selectbox("快速预设", list(VOICE_PRESETS.keys()))
    if preset_name != "自定义" and preset_name != st.session_state.last_preset:
        st.session_state.voice_character = VOICE_PRESETS[preset_name]
        st.session_state.last_preset = preset_name
    elif preset_name == "自定义" and st.session_state.last_preset != "自定义":
        st.session_state.last_preset = "自定义"

    if "voice_character" not in st.session_state:
        st.session_state.voice_character = VOICE_PRESETS["成熟女性 · 慵懒害羞"]

    voice_character = st.text_area(
        "角色声音特征",
        height=100,
        help="描述角色的音色、语气、年龄感等，例如：温柔成熟的女性声音、低沉稳重的男声。",
        key="voice_character",
    )

    st.divider()
    st.header("生成参数")
    cfg_value = st.slider("引导强度 (cfg_value)", 1.0, 4.0, 2.0, 0.1)
    inference_timesteps = st.slider("推理步数 (inference_timesteps)", 4, 20, 10, 1)

    with st.expander("高级选项"):
        use_reference = st.checkbox("使用参考音频克隆音色", value=False)
        normalize_text = st.checkbox("文本归一化", value=False)
        uploaded_ref = st.file_uploader("参考音频 (.wav)", type=["wav"], disabled=not use_reference)

st.subheader("台词内容")
content = st.text_area(
    "请输入想要转换的文字",
    height=150,
    placeholder="例如：小弟弟怎么一个人在这里，想不想和姐姐一起回家",
)

reference_wav_path = None
if use_reference and uploaded_ref is not None:
    ref_path = OUTPUT_DIR / "_reference.wav"
    ref_path.write_bytes(uploaded_ref.getvalue())
    reference_wav_path = str(ref_path)

col1, col2 = st.columns([1, 3])
with col1:
    generate_clicked = st.button("生成配音", type="primary", use_container_width=True)

if generate_clicked:
    if not content.strip():
        st.warning("请先输入台词内容。")
    else:
        target_text = build_target_text(voice_character, content)
        st.info(f"完整输入：`{target_text}`")

        try:
            model = load_model()
            sample_rate = model.tts_model.sample_rate

            with st.spinner("正在生成音频，请稍候..."):
                kwargs = {
                    "text": target_text,
                    "cfg_value": cfg_value,
                    "inference_timesteps": inference_timesteps,
                    "normalize": normalize_text,
                }
                if reference_wav_path:
                    kwargs["reference_wav_path"] = reference_wav_path

                wav = model.generate(**kwargs)

            file_name = f"output_{st.session_state.output_count}.wav"
            output_path = OUTPUT_DIR / file_name
            sf.write(str(output_path), wav, sample_rate)
            st.session_state.output_count += 1

            st.success(f"生成成功！文件已保存为 `{file_name}`")
            st.audio(str(output_path), format="audio/wav")

            with open(output_path, "rb") as f:
                st.download_button(
                    label="下载音频",
                    data=f.read(),
                    file_name=file_name,
                    mime="audio/wav",
                    use_container_width=True,
                )
        except Exception as e:
            st.error(f"生成失败：{e}")
