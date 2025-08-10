import os
import socket
import zipfile
from flask import Flask, render_template_string, send_from_directory
from flask import Response
import io

# 配置共享文件夹路径（请修改为您要共享的实际文件夹路径）
SHARED_FOLDER = "D:\\BaiduNetdiskDownload"

app = Flask(__name__)

# 确保共享文件夹存在
if not os.path.exists(SHARED_FOLDER):
    os.makedirs(SHARED_FOLDER)
    print(f"已创建共享文件夹: {SHARED_FOLDER}")


@app.route('/')
@app.route('/browse/<path:subfolder>')
def list_files(subfolder=''):
    """显示共享文件夹中的文件和文件夹列表，支持递归浏览"""
    # 计算当前浏览路径
    current_path = os.path.join(SHARED_FOLDER, subfolder)

    # 安全检查：防止目录遍历攻击
    if not os.path.abspath(current_path).startswith(os.path.abspath(SHARED_FOLDER)):
        return "访问被拒绝：不允许访问共享文件夹外的路径", 403

    # 获取当前路径中的所有项目
    items = os.listdir(current_path)
    files = []
    folders = []

    for item in items:
        item_path = os.path.join(current_path, item)
        relative_path = os.path.join(subfolder, item)

        if os.path.isdir(item_path):
            # 文件夹处理
            folders.append({
                'name': item,
                'path': relative_path
            })
        else:
            # 文件处理
            size = os.path.getsize(item_path) / (1024 * 1024)
            files.append({
                'name': item,
                'size': f"{size:.2f} MB",
                'path': relative_path
            })

    # 生成面包屑导航
    breadcrumbs = []
    parts = subfolder.split(os.sep)
    current_browse_path = ''

    breadcrumbs.append({'name': '根目录', 'path': ''})

    for part in parts:
        if part:
            current_browse_path = os.path.join(current_browse_path, part)
            breadcrumbs.append({
                'name': part,
                'path': current_browse_path
            })

    # 生成HTML页面
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>局域网文件共享</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            h1 { color: #333; }
            .breadcrumb { margin: 20px 0; }
            .breadcrumb-item { display: inline-block; margin-right: 5px; }
            .breadcrumb-item::after { content: ">"; margin-left: 5px; }
            .breadcrumb-item:last-child::after { content: ""; }
            .folder-list, .file-list { list-style: none; padding: 0; margin: 20px 0; }
            .folder-item, .file-item { margin: 8px 0; padding: 10px; border-radius: 4px; }
            .folder-item { background-color: #f0f7ff; }
            .file-item { background-color: #f5f5f5; }
            .folder-link, .file-link { text-decoration: none; color: #0066cc; }
            .folder-link::before { content: "📁 "; }
            .file-link::before { content: "📄 "; }
            .file-size { color: #666; margin-left: 10px; font-size: 0.9em; }
        </style>
    </head>
    <body>
        <h1>局域网文件共享</h1>

        <div class="breadcrumb">
            {% for crumb in breadcrumbs %}
            <div class="breadcrumb-item">
                <a href="/browse/{{ crumb.path }}">{{ crumb.name }}</a>
            </div>
            {% endfor %}
        </div>

        {% if folders %}
        <h2>文件夹</h2>
        <ul class="folder-list">
            {% for folder in folders %}
            <li class="folder-item">
                <a href="/browse/{{ folder.path }}" class="folder-link">{{ folder.name }}</a>
                <a href="/download_folder/{{ folder.path }}" class="folder-download" style="margin-left: 10px; color: #4CAF50;">📥 下载文件夹</a>
            </li>
            {% endfor %}
        </ul>
        {% endif %}

        {% if files %}
        <h2>文件</h2>
        <ul class="file-list">
            {% for file in files %}
            <li class="file-item">
                <a href="/download/{{ file.path }}" class="file-link">{{ file.name }}</a>
                <span class="file-size">{{ file.size }}</span>
            </li>
            {% endfor %}
        </ul>
        {% endif %}

        {% if not folders and not files %}
        <p>当前目录为空</p>
        {% endif %}
    </body>
    </html>
    '''
    return render_template_string(html, folders=folders, files=files, breadcrumbs=breadcrumbs)


@app.route('/download/<path:filename>')
def download_file(filename):
    """处理文件下载请求，支持子文件夹中的文件"""
    # 计算完整文件路径
    file_path = os.path.join(SHARED_FOLDER, filename)

    # 安全检查
    if not os.path.abspath(file_path).startswith(os.path.abspath(SHARED_FOLDER)) or not os.path.isfile(file_path):
        return "文件不存在或无法访问", 404

    # 获取文件名
    file_name = os.path.basename(file_path)

    # 读取文件内容到内存缓冲区，然后关闭文件
    with open(file_path, 'rb') as f:
        file_content = f.read()

    # 创建响应对象，发送内存中的文件内容
    response = Response(
        io.BytesIO(file_content),
        mimetype='application/octet-stream',
        headers={
            'Content-Disposition': f'attachment; filename="{file_name}"',
            'Content-Length': str(len(file_content))
        }
    )
    return response


@app.route('/download_folder/<path:folderpath>')
def download_folder(folderpath):
    """下载文件夹为ZIP压缩包"""
    # 计算实际文件夹路径
    folder_path = os.path.join(SHARED_FOLDER, folderpath)

    # 安全检查：防止目录遍历攻击
    if not os.path.abspath(folder_path).startswith(os.path.abspath(SHARED_FOLDER)):
        return "访问被拒绝：不允许访问共享文件夹外的路径", 403

    if not os.path.isdir(folder_path):
        return "文件夹不存在", 404

    # 创建内存中的ZIP文件
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 遍历文件夹中的所有文件和子文件夹
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                # 计算ZIP中的相对路径，避免包含完整系统路径
                arcname = os.path.relpath(file_path, os.path.dirname(folder_path))
                zipf.write(file_path, arcname=arcname)

    # 准备响应
    zip_buffer.seek(0)
    folder_name = os.path.basename(folderpath)
    response = Response(
        zip_buffer,
        mimetype='application/zip',
        headers={
            'Content-Disposition': f'attachment; filename="{folder_name}.zip"',
            'Content-Length': str(len(zip_buffer.getvalue()))
        }
    )
    return response


if __name__ == '__main__':
    # 获取本机局域网IP地址
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 连接到外部服务器以获取本机IP（不会实际建立连接）
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
    finally:
        s.close()

    print("=" * 50)
    print(f"文件夹共享服务器已启动！")
    print(f"共享文件夹路径: {SHARED_FOLDER}")
    print(f"请在同一局域网内的设备上，用浏览器访问:")
    print(f"http://{ip_address}:5000")
    print("=" * 50)

    # 启动Flask服务器，监听所有网络接口
    app.run(host='0.0.0.0', port=5000, debug=False)