from modelscope import snapshot_download
snapshot_download("OpenBMB/VoxCPM2", local_dir='./pretrained_models/VoxCPM2') # specify the local directory to save the model
print("==================模型已经下载完毕！==================")

from voxcpm import VoxCPM
import soundfile as sf
import os

# 1. 在循环外部加载模型（仅加载一次）
print("正在加载模型，请稍候...")
model = VoxCPM.from_pretrained("./pretrained_models/VoxCPM2", load_denoiser=False)
sample_rate = model.tts_model.sample_rate

print("\n--- 模型加载完毕 ---")
print("输入 'quit' 或 'exit' 可以退出程序。")

# 计数器，用于区分输出的文件名
count = 1

# 2. 进入交互循环
while True:
    # 获取控制台输入
    user_input = input(f"\n[{count}] 请输入想要转换的文字: ").strip()

    # 退出条件检查
    if user_input.lower() in ['quit', 'exit', 'q']:
        print("程序已退出。")
        break

    if not user_input:
        continue

    try:
        print("正在生成音频...")
        # 3. 执行推理
        # 注意：这里保留了你原本的 Prompt 格式，如果想让 Prompt 也动态化，可以进一步拆分字符串
        wav = model.generate(
            text=f"(A young man with a magnetic voice){user_input}",
            cfg_value=2.0,
            inference_timesteps=10,
        )

        # 4. 保存文件
        file_name = f"output_{count}.wav"
        sf.write(file_name, wav, sample_rate)

        print(f"生成成功！文件已保存为: {file_name}")
        count += 1

    except Exception as e:
        print(f"发生错误: {e}")