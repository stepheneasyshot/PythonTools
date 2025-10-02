import os
import shutil
import subprocess

"""
将翻译后的strings.xml文件移植到原apk资源下，重新打包
"""

# --- 配置参数 ---
# 待处理的APK文件所在的根目录
ROOT_DIR = '/Users/stephenzhan/Downloads/systemdata'
# 包含strings.xml文件的目录
STRINGS_XML_DIR = '/Users/stephenzhan/Desktop/LAO'
# 打包后APK文件的输出目录
DESKTOP_DIR = os.path.join(os.path.expanduser("~"), "Desktop")


def find_and_process_apks(root_dir, strings_xml_dir, desktop_dir):
    """
    递归查找指定目录下的所有APK文件并进行处理。
    """
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".apk"):
                apk_path = os.path.join(dirpath, filename)
                apk_name = os.path.splitext(filename)[0]

                print(f"找到APK文件: {apk_path}")

                # 1. 使用apktool解包
                output_dir = os.path.join(dirpath, apk_name)
                try:
                    subprocess.run(["apktool", "d", apk_path, "-o", output_dir], check=True)
                    print(f"成功解包到: {output_dir}")
                except subprocess.CalledProcessError as e:
                    print(f"解包失败: {e}")
                    continue

                # 2. 删除原始APK文件
                try:
                    os.remove(apk_path)
                    print(f"已删除原始APK文件: {apk_path}")
                except OSError as e:
                    print(f"删除APK文件失败: {e}")
                    continue

                # 3. 复制并重命名strings.xml文件
                source_strings_xml = os.path.join(strings_xml_dir, f"{apk_name}_strings.xml")
                target_strings_dir = os.path.join(output_dir, "res", "values")
                target_strings_xml = os.path.join(target_strings_dir, "strings.xml")

                if not os.path.exists(source_strings_xml):
                    print(f"未找到对应的XML文件: {source_strings_xml}")
                    continue

                # 确保目标目录存在
                os.makedirs(target_strings_dir, exist_ok=True)

                try:
                    shutil.copy(source_strings_xml, target_strings_xml)
                    print(f"成功复制并重命名strings文件: {target_strings_xml}")
                except shutil.Error as e:
                    print(f"复制文件失败: {e}")
                    continue

                # 4. 使用apktool打包，apk留在原来的文件夹中
                try:
                    subprocess.run(["apktool", "b", output_dir, "-o", f"{output_dir}.apk"], check=True)
                    print(f"成功重新打包APK: {output_dir}.apk")
                except subprocess.CalledProcessError as e:
                    print(f"打包失败: {e}")
                    continue

                # # 5. 将打包后的APK复制到桌面
                # rebuilt_apk_path = f"{output_dir}_rebuilt.apk"
                # final_apk_path = os.path.join(desktop_dir, f"{apk_name}_rebuilt.apk")
                #
                # try:
                #     shutil.move(rebuilt_apk_path, final_apk_path)
                #     print(f"已将打包后的APK复制到桌面: {final_apk_path}")
                # except shutil.Error as e:
                #     print(f"复制到桌面失败: {e}")
                #     continue

                # 清理临时解包目录
                try:
                    shutil.rmtree(output_dir)
                    print(f"已清理临时目录: {output_dir}")
                except OSError as e:
                    print(f"清理临时目录失败: {e}")

                print("-" * 30)


if __name__ == "__main__":
    find_and_process_apks(ROOT_DIR, STRINGS_XML_DIR, DESKTOP_DIR)
    print("所有APK文件处理完毕。")