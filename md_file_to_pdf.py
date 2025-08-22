import pypandoc
import os


def markdown_to_pdf(input_md_file, output_pdf_file):
    """
    将 Markdown 文件转换为 PDF 文件。

    参数:
    input_md_file (str): 输入的 Markdown 文件路径。
    output_pdf_file (str): 输出的 PDF 文件路径。
    """
    if not os.path.exists(input_md_file):
        print(f"错误：找不到文件 '{input_md_file}'")
        return

    try:
        # 使用 pypandoc 将 Markdown 转换为 PDF
        pypandoc.convert_file(input_md_file, 'pdf', outputfile=output_pdf_file)
        print(f"成功将 '{input_md_file}' 转换为 '{output_pdf_file}'")
    except Exception as e:
        print(f"转换过程中发生错误: {e}")


if __name__ == "__main__":
    # 指定你的输入和输出文件路径
    input_file = "C:\\Users\\zhanf\\Desktop\\tesettestsetes.md"  # 替换成你的Markdown文件路径
    output_file = "C:\\Users\\zhanf\\Desktop\\OUTPUT_PDF_FILE.pdf"  # 替换成你想要的PDF文件路径

    markdown_to_pdf(input_file, output_file)