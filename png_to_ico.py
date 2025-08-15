from PIL import Image

def png_to_ico(png_path, ico_path):
    # 打开PNG图像
    image = Image.open(png_path)

    # 将图像转换为ICO格式
    image.save(ico_path, format='ICO', sizes=[(image.width, image.height)])

# 调用函数并传入PNG图像路径和ICO文件路径
png_to_ico('C:\\Users\\zhanf\\Desktop\\logo.png', 'output.ico')
