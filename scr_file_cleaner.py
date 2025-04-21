import os
import time
import logging
from datetime import datetime

# 运行后，每10s扫描一次D盘根目录，删除后缀scr的文件，去掉烦人的公司电脑屏保

# 设置日志记录
logging.basicConfig(
    filename='D:\\scr_file_cleaner.log',  # 日志文件路径
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def delete_scr_files():
    target_dir = 'D:\\'  # 监控D盘根目录
    deleted_files = 0

    try:
        # 列出目录下所有文件
        for filename in os.listdir(target_dir):
            if filename.lower().endswith('.scr'):
                file_path = os.path.join(target_dir, filename)
                try:
                    os.remove(file_path)
                    logging.info(f'deleted file: {file_path}')
                    deleted_files += 1
                except Exception as e:
                    logging.error(f'delete file {file_path} failed: {str(e)}')

        if deleted_files > 0:
            logging.info(f'deleted  {deleted_files}  .scr file in this running')
    except Exception as e:
        logging.error(f'check directory error: {str(e)}')


def main():
    logging.info('start to check scr files in this directory...')
    while True:
        delete_scr_files()
        time.sleep(10)  # 每隔10秒检查一次


if __name__ == '__main__':
    # 检查是否以管理员权限运行（可能需要删除系统文件）
    try:
        main()
    except KeyboardInterrupt:
        logging.info('interrupted by user')
    except Exception as e:
        logging.error(f'running error: {str(e)}')