import os
import re

def replace_img_src(directory, new_src):
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r+', encoding='utf-8') as file:
                content = file.read()

                # 使用正则表达式查找并替换 img 标签的 src 属性
                updated_content = re.sub(r'<img\s+[^>]*src="[^"]*"[^>]*>', 
                                         f'< img src="{new_src}" alt="Image">', 
                                         content)

                file.seek(0)
                file.write(updated_content)
                file.truncate()

# 替换指定目录下所有 HTML 文件中的 img 标签
directory = 'data'
replace_img_src(directory, 'https://picsum.photos/seed/picsum/200/300')