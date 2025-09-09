import os
import subprocess
import shutil

# 设置需要搜索的根目录
# 将 'your_directory_path' 替换为你要搜索的实际目录
root_directory = '/Users/stephenzhan/Downloads/Car461'

# 获取桌面路径
# 如果你的操作系统不是 macOS 或 Windows，可能需要修改此路径
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')


def find_and_decompile_apk(directory):
    """
    递归遍历目录，找到所有apk文件并进行解包和文件复制。
    """
    if not os.path.exists(directory):
        print(f"Error: Directory does not exist: {directory}")
        return

    for entry in os.walk(directory):
        current_dir, sub_dirs, files = entry
        for file in files:
            if file.endswith('.apk'):
                apk_path = os.path.join(current_dir, file)
                print(f"Found APK: {apk_path}")

                # 获取不带扩展名的APK文件名
                apk_name = os.path.splitext(file)[0]

                # 设置解包后的输出目录
                output_dir = os.path.join(current_dir, apk_name)

                try:
                    # 使用apktool解包APK
                    print(f"Decompiling {file}...")
                    subprocess.run(['apktool', 'd', apk_path, '-o', output_dir], check=True)
                    print(f"Decompilation successful.")

                    # 构建strings.xml的源文件路径
                    source_strings_xml = os.path.join(output_dir, 'res', 'values', 'strings.xml')

                    if os.path.exists(source_strings_xml):
                        # 构建目标文件路径，并重命名
                        destination_strings_xml = os.path.join(desktop_path, f"{apk_name}_strings.xml")

                        # 复制文件
                        print(f"Copying strings.xml to desktop as {os.path.basename(destination_strings_xml)}...")
                        shutil.copy(source_strings_xml, destination_strings_xml)
                        print("File copied successfully.")
                    else:
                        print(f"Warning: strings.xml not found for {file}")

                except subprocess.CalledProcessError as e:
                    print(f"Error during apktool execution for {file}: {e}")
                except FileNotFoundError:
                    print(
                        "Error: apktool command not found. Please ensure apktool is installed and in your system's PATH.")
                finally:
                    # 清理：删除解包后的文件夹
                    print(f"Cleaning up temporary directory: {output_dir}")
                    if os.path.exists(output_dir):
                        shutil.rmtree(output_dir)
                    print("Cleanup complete.")


# 执行脚本
find_and_decompile_apk(root_directory)
print("Script finished.")