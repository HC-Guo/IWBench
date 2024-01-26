import os
import re

def extract_html_blocks(text):
    # 显式处理不同的大小写组合
    pattern = r'```[Hh][Tt][Mm][Ll](.*?)```'
    blocks = re.findall(pattern, text, re.DOTALL)
    return blocks if blocks else [text]

def process_html_files_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".html"):
                file_path = os.path.join(root, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                html_blocks = extract_html_blocks(content)

                if html_blocks:
                    processed_content = '\n'.join(html_blocks)
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(processed_content)
                        print(f"Processed and updated file: {file_path}")
                else:
                    print(f"File '{file_path}' does not contain the specified HTML pattern, no processing done.")

directory_path = '/Users/yisuanwang/Desktop/image2html/Image2HTML-Benchmark/dataset copy'
process_html_files_in_directory(directory_path)
