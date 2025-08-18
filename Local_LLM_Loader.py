from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# 指定本地文件夹路径
local_model_path = "E:\\Dev\\AI\\Qwen3-4B-Thinking-2507"

# 加载分词器和模型
try:
    # 加载分词器
    tokenizer = AutoTokenizer.from_pretrained(local_model_path)
    # 加载模型
    model = AutoModelForCausalLM.from_pretrained(local_model_path)

    print("模型和分词器已从本地成功加载！")

    # 确保模型在合适的设备上运行，如果有GPU则使用GPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"模型将在 {device} 上运行")
    model.to(device)

    print("开始对话！输入 'exit' 退出。")

    while True:
        user_input = input("你: ")
        if user_input.lower() == 'exit':
            break

        # 对输入进行编码，并返回 attention_mask
        inputs = tokenizer(user_input, return_tensors="pt").to(device)

        # 打印 inputs，你会看到除了 input_ids，还有一个 attention_mask
        print("编码后的输入：", inputs)
        # 2. 模型生成回答
        # `max_length`: 限制生成文本的最大长度
        # `do_sample`: 是否使用采样策略，True 会让回答更具创造性
        # `top_k`: 采样时考虑概率最高的k个词
        # `temperature`: 控制生成文本的随机性，值越高越随机
        output_ids = model.generate(
            **inputs,
            max_length=100,
            do_sample=True,
            top_k=20,
            temperature=0.6
        )

        # 3. 将生成的 token ids 解码为文本
        # `skip_special_tokens=True` 会跳过特殊标记，如 [CLS], [SEP]
        response = tokenizer.decode(output_ids[0], skip_special_tokens=True)

        print(f"模型: {response}")

except Exception as e:
    print(f"加载模型时出错：{e}")
    print("请检查你的文件夹路径和文件是否完整。")
