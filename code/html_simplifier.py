from bs4 import BeautifulSoup, Tag
import filecmp
import datetime
import os
from playwright_utils import PlaywrightUtils
import shutil

        
def simplify(playwright_utils=None, content="<html>...</html>", output_file='simplified.html'):
    if playwright_utils is None:
        playwright_utils = PlaywrightUtils()
    tmp_dir = "simplify_tmp/"

    playwright_utils.set_content(content)
    # playwright_utils.goto(url_or_path)
    playwright_utils.take_screenshot(f"{tmp_dir}original.png")

    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
        
    removed_elements = []
    soup = BeautifulSoup(content, 'html.parser')
    # with open(url_or_path, 'r') as file:
    #     soup = BeautifulSoup(file, 'html.parser')
    
    elements_to_check = soup.find_all(True)
    clean_soup = str(soup)
    cnt = 0

    for el in elements_to_check:
        cnt += 1
        # print('='*40, el.name, '='*40, f'{cnt} / {len(elements_to_check)}')
        if isinstance(el, Tag) and el.name not in ['html', 'head', 'body', 'title', 'meta']:
            if el is None or el == None:
                continue
            souptmp = clean_soup
            # 获取最上层节点的子节点
            children = el.findChildren()
            # 从文档中删除最上层节点
            el.extract()
            combined_text = ''
            # 遍历子节点并连接它们的文本内容
            for child in children:
                combined_text += str(child)
            # print('===删除后===')
            # print(combined_text)
            souptmp = souptmp.replace(str(el), combined_text)
            # 对比临时HTML和原始HTML的渲染结果
            # 获取当前时间并格式化为字符串
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S%f")
            # 创建一个临时的HTML文件用于测试
            tmp_html_file = f'{tmp_dir}tmphtml_{timestamp}.html'
            # print(tmp_html_file)
            with open(tmp_html_file, 'w') as file:
                file.write(str(souptmp))
            # 创建tmp渲染图片，加上时间戳
            tmp_screenshot = f'{tmp_dir}tmp_image_{timestamp}.png'

            playwright_utils.goto(f"{tmp_html_file}")
            playwright_utils.take_screenshot(tmp_screenshot)

            # 比较图片
            if filecmp.cmp(f'{tmp_dir}original.png', f'{tmp_screenshot}', shallow=False):
                # 如果临时HTML的渲染结果与原始HTML相同，则soup = tmpsoup
                clean_soup = souptmp
                # print('-'*20, 'remove:', el.name)
                removed_elements.append(el)

    # with open(output_file, 'w') as file:
    #     file.write(clean_soup)

    shutil.rmtree(tmp_dir)

    # print(f"Removed {len(removed_elements)} elements")
    return clean_soup, removed_elements 

if __name__ == "__main__":
    html_file='unit_test_case/simplifier_examlple.html'
    html_content = open(html_file, 'r').read()
    print(simplify(content=html_content, output_file='simplified.html'))

