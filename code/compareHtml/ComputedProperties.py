from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json

def getTagAttributes(local_html_file_path='file:////Users/yisuanwang/Desktop/image2html/src/ignoreAttr/data/case3/email.html', output_path='./tag_properties.json'):
    # 初始化 WebDriver
    webdriver_path = "/usr/local/bin/chromedriver-mac-arm64/chromedriver"
    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    service = Service(executable_path=webdriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 打开本地 HTML 文件
    driver.get(local_html_file_path)

    # 获取所有元素
    elements = driver.find_elements(By.XPATH, '//*')

    # 收集每个元素的属性
    tag_properties = {}
    for element in elements:
        attributes = element.get_property('attributes')
        properties = {attr['name']: attr['value'] for attr in attributes}
        html_string = element.get_attribute('outerHTML')
        html_string = html_string.replace('\n', '').replace('\t', '').replace('&nbsp;', '').replace('&#160;', '').replace('"', '').replace('\"', '').replace(' ', '').replace('<tbody>', '').replace('</tbody>', '')
        # html_string = ' '.join(html_string.split())

        tag_properties[html_string] = properties

    # 保存标签属性到文件
    with open(output_path, 'w') as file:
        json.dump(tag_properties, file, indent=4)

    # 关闭 WebDriver
    driver.quit()

    return tag_properties

if __name__ == '__main__':
    getTagAttributes()