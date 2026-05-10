import os
from PIL import Image
from pathlib import Path

def convert_jpg_to_png(source_path, target_folder=None):
    # 如果没有指定目标文件夹，则保存在原路径
    if target_folder and not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # 检查输入是单个文件还是文件夹
    if os.path.isfile(source_path):
        files = [source_path]
    else:
        files = [os.path.join(source_path, f) for f in os.listdir(source_path) if f.lower().endswith('.jpg')]

    for file_path in files:
        try:
            # 打开图片
            with Image.open(file_path) as img:
                # 构建新文件名
                file_name = os.path.splitext(os.path.basename(file_path))[0]
                save_dir = target_folder if target_folder else os.path.dirname(file_path)
                out_path = os.path.join(save_dir, f"{file_name}.png")

                # 转换并保存
                img.save(out_path, "PNG")
                print(f"成功转换: {file_path} -> {out_path}")
        except Exception as e:
            print(f"转换 {file_path} 出错: {e}")


if __name__ == "__main__":
    # 使用示例：
    # 1. 转换单个文件
    # convert_jpg_to_png("example.jpg")

    # 2. 批量转换文件夹内的所有 jpg
    input_dir = Path("~/Downloads/app_icon.jpg").expanduser()
    output_dir = "./converted_pngs"
    convert_jpg_to_png(input_dir, output_dir)