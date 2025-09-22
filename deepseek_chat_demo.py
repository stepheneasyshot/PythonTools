from openai import OpenAI

# for backward compatibility, you can still use `https://api.deepseek.com/v1` as `base_url`.
client = OpenAI(api_key="sk-xxxx", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "帮我使用Java写一个倒计时工具类"},
    ],
    max_tokens=1024,
    temperature=0.7,
    stream=True
)

for chunk in response:
    print(chunk.choices[0].delta.content, end=" ")
