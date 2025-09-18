import os
import subprocess
import sys


def sign_apk_in_directory(directory, keystore_path, key_alias, key_pass):
    """
    递归遍历指定目录，找到所有.apk文件并使用apksigner进行签名。
    签名后的APK将直接替换原文件。

    Args:
        directory (str): 要搜索的目录路径。
        keystore_path (str): 签名文件(.jks)的路径。
        key_alias (str): 签名文件的别名。
        key_pass (str): 签名文件的密码。
    """
    # 检查签名文件是否存在
    if not os.path.exists(keystore_path):
        print(f"错误: 签名文件未找到 - {keystore_path}")
        return

    # 检查apksigner工具是否可用
    try:
        subprocess.run(['apksigner', '--version'], check=True, capture_output=True)
    except FileNotFoundError:
        print("错误: 找不到apksigner命令。请确保它已添加到系统的PATH环境变量中。")
        print("提示: apksigner位于Android SDK的build-tools目录下。")
        return
    except subprocess.CalledProcessError:
        print("警告: apksigner命令存在，但执行失败。")

    signed_count = 0
    print(f"开始在目录 '{directory}' 中查找APK文件...")

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.apk'):
                apk_path = os.path.join(root, file)
                print(f"\n正在处理文件: {apk_path}")

                try:
                    command = [
                        'apksigner', 'sign',
                        '--ks', keystore_path,
                        '--ks-key-alias', key_alias,
                        '--ks-pass', f'pass:{key_pass}',
                        '--key-pass', f'pass:{key_pass}',
                        '--out', apk_path,
                        apk_path
                    ]

                    result = subprocess.run(command, check=True, capture_output=True, text=True)

                    if result.returncode == 0:
                        print(f"成功签名: {apk_path}")
                        # 删除同目录下后缀为 .idsig 类型的文件
                        idsig_path = apk_path.replace('.apk', '.apk.idsig')
                        if os.path.exists(idsig_path):
                            os.remove(idsig_path)
                            print(f"删除 idsig 文件成功: {idsig_path}")
                        signed_count += 1
                    else:
                        print(f"签名失败，错误信息: {result.stderr}")

                except subprocess.CalledProcessError as e:
                    print(f"签名命令执行失败，错误: {e.stderr}")
                except Exception as e:
                    print(f"处理文件 {apk_path} 时发生未知错误: {e}")

    print(f"\n批量签名完成。共计签名 {signed_count} 个APK文件。")


if __name__ == '__main__':
    # ==========================
    # 请在这里修改你的配置信息
    # ==========================
    APK_DIRECTORY = '/Users/stephenzhan/Downloads/systemdata'
    KEYSTORE_PATH = 'android_sign_keys/stephen-release-key.keystore'
    KEY_ALIAS = "stephen"
    KEY_PASSWORD = "stephen"

    # 调用签名函数
    sign_apk_in_directory(APK_DIRECTORY, KEYSTORE_PATH, KEY_ALIAS, KEY_PASSWORD)