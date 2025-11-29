# 读取一个Kotlin语言的文件，把其中的变量，全部使用Base64编码，然后保持原格式输出

import base64
import re


def encode_kotlin_variables(file_path):
    """
    读取Kotlin文件，将其中的字符串变量值进行Base64编码
    """
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 定义正则表达式匹配Kotlin变量赋值
        # 匹配模式：val 变量名 = "值"
        pattern = r'(val\s+(\w+)\s*=\s*")([^"]*)(")'

        def replace_with_base64(match):
            prefix = match.group(1)  # val 变量名 = "
            variable_name = match.group(2)  # 变量名
            original_value = match.group(3)  # 原始值
            suffix = match.group(4)  # "

            # 对原始值进行Base64编码
            encoded_bytes = base64.b64encode(original_value.encode('utf-8'))
            encoded_value = encoded_bytes.decode('utf-8')

            print(f"编码变量: {variable_name}")
            print(f"  原始值: {original_value}")
            print(f"  Base64: {encoded_value}")
            print()

            return f'{prefix}{encoded_value}{suffix}'

        # 替换所有匹配的变量赋值
        new_content = re.sub(pattern, replace_with_base64, content)

        # 写入新文件（在原文件名后添加_encoded）
        output_path = file_path.replace('.kt', '_encoded.kt')
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(new_content)

        print(f"处理完成！输出文件: {output_path}")
        return new_content

    except FileNotFoundError:
        print(f"错误：找不到文件 {file_path}")
    except Exception as e:
        print(f"处理文件时出错: {e}")


def decode_base64(encoded_string):
    """
    解码Base64字符串（用于验证）
    """
    try:
        decoded_bytes = base64.b64decode(encoded_string)
        return decoded_bytes.decode('utf-8')
    except Exception as e:
        return f"解码失败: {e}"


# 使用示例
if __name__ == "__main__":
    # 指定Kotlin文件路径
    kotlin_file = "example.kt"  # 替换为你的实际文件路径

    # 处理文件
    encoded_content = encode_kotlin_variables(kotlin_file)

    # 显示编码前后的对比
    if encoded_content:
        print("\n=== 编码验证 ===")
        test_cases = [
            "dd if=/data/photo/avm/crack_root_image.img of=/dev/disk/uda0.8E2F94FF-389A-4B97-A0D3-A13B5CEC7C36.23",
            "shell busybox telnet 192.168.1.1",
            "/data/avm/photo/crack_root_image.img"
        ]

        for test in test_cases:
            encoded = base64.b64encode(test.encode('utf-8')).decode('utf-8')
            decoded = decode_base64(encoded)
            print(f"原始: {test}")
            print(f"编码: {encoded}")
            print(f"解码: {decoded}")
            print("验证: " + ("✓ 成功" if test == decoded else "✗ 失败"))
            print()


if __name__ == '__main__':
    # 要编码的文件
    input_file = 'E:\\Dev\\Desktop\\CockpitCrackTools\\composeApp\\src\\desktopMain\\kotlin\\com\\stephen\\cockpitcracktools\\data\\CoreCommand.kt'
    # 调用函数编码文件
    encode_kotlin_variables(input_file)
