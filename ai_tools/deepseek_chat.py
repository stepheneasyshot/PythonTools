"""Send a streaming chat request to the DeepSeek API."""

from openai import OpenAI


def deepseek_chat(
    api_key,
    system_prompt="You are a helpful assistant",
    user_message="Hello!",
    model="deepseek-chat",
    max_tokens=1024,
    temperature=0.7,
    stream=True,
):
    """Send a chat request to the DeepSeek API and stream the response.

    Args:
        api_key: DeepSeek API key.
        system_prompt: System-level instruction. Defaults to a generic assistant prompt.
        user_message: The user's input message.
        model: Model name to use. Defaults to "deepseek-chat".
        max_tokens: Maximum tokens in the response. Defaults to 1024.
        temperature: Sampling temperature. Defaults to 0.7.
        stream: Whether to stream the response. Defaults to True.

    Returns:
        The full response content if not streaming, otherwise None.
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        max_tokens=max_tokens,
        temperature=temperature,
        stream=stream,
    )

    if stream:
        for chunk in response:
            print(chunk.choices[0].delta.content or "", end="")
        print()
    else:
        return response.choices[0].message.content


if __name__ == "__main__":
    # Set your API key here or use environment variable
    api_key = "sk-your-api-key"
    deepseek_chat(
        api_key=api_key,
        user_message="Write a countdown timer in Java",
    )