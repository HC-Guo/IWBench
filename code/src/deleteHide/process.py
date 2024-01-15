from html2image import Html2Image
from bs4 import BeautifulSoup, Comment, Tag
import os
import shutil
import filecmp
import datetime
import time

# 临时文件保存目录
tmp_dir = '/Users/yisuanwang/Desktop/image2html/src/deleteHide/tmp/'

def screenshot(html_file, save_as):
    hti = Html2Image(browser='chrome', size=(1920, 1080))
    hti.output_path = tmp_dir
    hti.screenshot(html_file=html_file, save_as=save_as)

def clean_html(html_file, clean_html_file):
    removed_elements = []
    with open(html_file, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')

    elements_to_check = soup.find_all(True)
    clean_soup = str(soup)
    cnt  = 0

    for el in elements_to_check:
        # 清理临时文件
        shutil.rmtree(tmp_dir)

        # print(el.name)
        cnt += 1
        print('='*40, el.name,'='*40 ,f'{cnt} / {len(elements_to_check)}')
        if isinstance(el, Tag) and el.name not in ['html', 'head', 'body', 'title']:
            if el is None or el == None:
                continue
            # print(el)
            # print('^'*50)

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
            print(tmp_html_file)
            with open(tmp_html_file, 'w') as file:
                file.write(str(souptmp))
            
            # 创建tmp渲染图片，加上时间戳
            tmp_screenshot = f'tmp_image_{timestamp}.png'
            screenshot(tmp_html_file, tmp_screenshot)

            # 比较图片
            if filecmp.cmp(f'{tmp_dir}original.png', f'{tmp_dir}{tmp_screenshot}', shallow=False):
                # 如果临时HTML的渲染结果与原始HTML相同，则soup = tmpsoup
                clean_soup = souptmp
                print('-'*20,'remove:', el.name)
                removed_elements.append(el)
                
    with open(clean_html_file, 'w') as file:
        file.write(clean_soup)
    
    os.remove(tmp_html_file)

    return removed_elements

def cleanHtml(html_file='/Users/yisuanwang/Desktop/image2html/src/deleteHide/h1.html', clean_html_file = '/Users/yisuanwang/Desktop/image2html/src/deleteHide/h1_clean.html'):
    # 示例使用
    # html_file = '/Users/yisuanwang/Desktop/image2html/src/deleteHide/h1.html' # 要清理的html文件
    # clean_html_file = '/Users/yisuanwang/Desktop/image2html/src/deleteHide/h1_clean.html' # 清理后的html文件保存路径

    # 原始的html渲染图片
    original_screenshot = f'original.png'
    screenshot(html_file, original_screenshot)

    # 尝试移除每一个element
    removed_elements = clean_html(html_file, clean_html_file)

    # 移除结束后的html渲染图片，应该和ori是一样的
    screenshot(clean_html_file, 'clean.png')

    # 移除元素的数量
    print(f"Removed {len(removed_elements)} elements:")

    # 清理临时文件
    shutil.rmtree(tmp_dir)

if __name__ == '__main__':
    cleanHtml()