"""Convert MP4 video files to animated GIF images."""

from moviepy.video.io.VideoFileClip import VideoFileClip


def convert_mp4_to_gif(input_file, output_file, fps=10):
    """Convert an MP4 video to GIF format.

    Args:
        input_file: Path to the input MP4 file.
        output_file: Path for the output GIF file.
        fps: Frame rate for the output GIF. Defaults to 10.

    Raises:
        FileNotFoundError: If the input file does not exist.
        ValueError: If the video cannot be loaded.
    """
    try:
        clip = VideoFileClip(input_file)
        clip.write_gif(output_file, fps=fps)
        clip.close()
        print(f"Converted successfully: {output_file}")
    except FileNotFoundError:
        print(f"Error: file not found - {input_file}")
        raise
    except Exception as e:
        print(f"Conversion failed: {e}")
        raise


if __name__ == "__main__":
    # Example usage
    convert_mp4_to_gif("input.mp4", "output.gif", fps=10)