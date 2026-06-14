"""Interactive chat with a local HuggingFace transformer model."""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


def load_model(model_path, device=None):
    """Load a tokenizer and causal language model from a local path.

    Args:
        model_path: Path to the local model directory.
        device: Computation device ('cuda', 'cpu', 'mps', or None for auto-detect).

    Returns:
        Tuple of (tokenizer, model, device_string).

    Raises:
        OSError: If the model path does not exist or is invalid.
    """
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"Loading model from: {model_path}")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)
    model.to(device)
    print(f"Model loaded and running on: {device}")
    return tokenizer, model, device


def chat_loop(tokenizer, model, device, max_length=100, temperature=0.6, top_k=20):
    """Start an interactive chat loop with the loaded model.

    Args:
        tokenizer: The model's tokenizer.
        model: The loaded language model.
        device: Device string the model is on.
        max_length: Maximum generation length. Defaults to 100.
        temperature: Sampling temperature. Defaults to 0.6.
        top_k: Top-k sampling parameter. Defaults to 20.
    """
    print("Starting chat. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        inputs = tokenizer(user_input, return_tensors="pt").to(device)
        output_ids = model.generate(
            **inputs,
            max_length=max_length,
            do_sample=True,
            top_k=top_k,
            temperature=temperature,
        )
        response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        print(f"Model: {response}")


if __name__ == "__main__":
    model_path = "path/to/local/model"
    tokenizer, model, device = load_model(model_path)
    chat_loop(tokenizer, model, device)