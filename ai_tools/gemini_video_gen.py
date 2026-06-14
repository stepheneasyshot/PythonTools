"""Generate videos using Google Gemini/Veo API."""

import time
from google import genai
from google.genai import types


def generate_video(
    api_key=None,
    prompt="A short video of a person walking on a beach at sunset.",
    model="veo-3.0-generate-001",
    poll_interval=10,
    output_path="generated_video.mp4",
):
    """Generate a video using the Gemini Veo API and download the result.

    Args:
        api_key: Google API key. If None, uses the default client configuration.
        prompt: Text description of the video to generate.
        model: Model name. Defaults to "veo-3.0-generate-001".
        poll_interval: Seconds between status checks. Defaults to 10.
        output_path: Path to save the generated video. Defaults to "generated_video.mp4".
    """
    client = genai.Client(api_key=api_key) if api_key else genai.Client()

    print("Starting video generation...")
    operation = client.models.generate_videos(model=model, prompt=prompt)

    while not operation.done:
        print("Waiting for video generation...")
        time.sleep(poll_interval)
        operation = client.operations.get(operation)

    generated_video = operation.response.generated_videos[0]
    client.files.download(file=generated_video.video)
    generated_video.video.save(output_path)
    print(f"Video saved to {output_path}")


if __name__ == "__main__":
    generate_video(
        prompt="A close up of two people staring at a cryptic drawing on a wall, torchlight flickering.",
        output_path="dialogue_example.mp4",
    )