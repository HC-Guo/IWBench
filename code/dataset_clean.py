import os
import re

def extract_html_blocks(text):
    pattern = r'```html(.*?)```'
    return re.findall(pattern, text, re.DOTALL)

def process_html_files_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".html"):
                file_path = os.path.join(root, filename)

                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # 检查并提取文件中的 HTML 模块
                html_blocks = extract_html_blocks(content)

                if html_blocks:
                    # 对提取的 HTML 块进行处理
                    processed_content = '\n'.join(html_blocks)

                    # 将处理后的内容写回原文件
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(processed_content)
                        print(f"已处理并更新文件：{file_path}")
                else:
                    # 没有找到指定模式时不执行操作
                    print(f"文件 '{file_path}' 不包含指定的 HTML 模式，未进行处理。")



directory_path = 'D:\Desktop\i2h-bench\Image2HTML-Benchmark\dataset'
process_html_files_in_directory(directory_path)
