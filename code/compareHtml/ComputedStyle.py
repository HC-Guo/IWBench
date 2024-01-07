# 获取html中每个元素的computed style，保存到json文件


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json

def getComputedStyle(local_html_file_path = 'file:////Users/yisuanwang/Desktop/image2html/src/ignoreAttr/data/case1/404errorpage.html', output_path = './computed_styles.json'):
    # 初始化 WebDriver
    webdriver_path = "/usr/local/bin/chromedriver-mac-arm64/chromedriver"  # 指定 WebDriver 的路径
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # 使用无头模式

    service = Service(executable_path=webdriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 打开本地 HTML 文件
    driver.get(local_html_file_path)

    # 获取所有元素
    elements = driver.find_elements(By.XPATH, '//*')

    # 计算每个元素的计算样式
    computed_styles = {}
    for element in elements:
        style = driver.execute_script("""
            var computed = window.getComputedStyle(arguments[0]);
            var styles = {};
            for (var i = 0; i < computed.length; i++) {
                styles[computed[i]] = computed.getPropertyValue(computed[i]);
            }
            return styles;
        """, element)
        # 替换换行符和制表符
        html_string = element.get_attribute('outerHTML')
        html_string = html_string.replace('\n', '').replace('\t', '').replace('&nbsp;', '').replace('&#160;', '').replace('"','').replace('\"','').replace(' ','').replace('<tbody>', '').replace('</tbody>', '')

        # 替换多个连续空格为单个空格
        # html_string = ' '.join(html_string.split())

        computed_styles[html_string] = style

    # 保存计算样式到文件
    with open(output_path, 'w') as file:
        json.dump(computed_styles, file, indent=4)

    # 关闭 WebDriver
    driver.quit()

    return computed_styles
