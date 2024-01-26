import os

def replace_html_start(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 检查文件是否以 'html' 开头（忽略空格和换行符）
    if content.lstrip().startswith('html'):
        # 替换开头
        new_content = '<!DOCTYPE html>' + content.lstrip()[4:]
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f"Updated: {file_path}")

def main():
    root_dir = "/Users/yisuanwang/Desktop/image2html/Image2HTML-Benchmark/dataset_clean_imgrep_en"

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                replace_html_start(file_path)

if __name__ == "__main__":
    main()
