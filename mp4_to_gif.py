from moviepy.video.io.VideoFileClip import VideoFileClip


"""

将 MP4 文件转换为 GIF 图片的工具

"""


def mp4_to_gif(input_file, output_file, fps=10):
    """
    将 MP4 文件转换为 GIF 图片。

    :param input_file: 输入的 MP4 文件路径
    :param output_file: 输出的 GIF 文件路径
    :param fps: GIF 的帧率，默认为 10
    """
    try:
        # 加载视频文件
        clip = VideoFileClip(input_file)
        # 转换为 GIF 并保存
        clip.write_gif(output_file, fps=fps)
        # 关闭视频文件
        clip.close()
        print(f"转换成功，文件已保存至 {output_file}")
    except Exception as e:
        print(f"转换失败: {e}")

if __name__ == "__main__":
    input_mp4 = "C:\\Users\\zhanf\\Desktop\\AndroidTempFiles\\screen-20250526-161926.mp4"  # 替换为你的 MP4 文件路径
    output_gif = "C:\\Users\\zhanf\\Desktop\\AndroidTempFiles\\screen-20250526-161926.gif"
    mp4_to_gif(input_mp4, output_gif, fps=10)