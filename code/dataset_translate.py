import os
import goslate
from bs4 import BeautifulSoup
import requests
import hashlib 

def translate_text_with_goslate(text, target_language='en'):
    gs = goslate.Goslate()
    translated_text = gs.translate(text, target_language)
    return translated_text

# 百度翻译API的配置信息
BAIDU_API_URL = "https://fanyi-api.baidu.com/api/trans/vip/translate"
BAIDU_APP_ID = "20220410001167159"
BAIDU_APP_KEY = "NhAQcnidiQ_qresygoNa"

def translate_text_with_baidu(text, target_language='en'):
    # 检查text是否为空或只包含空格
    if not text.strip():
        return text
    
    # 构建API请求参数
    params = {
        'q': text,
        'from': 'auto',  # 源语言设置为自动检测
        'to': target_language,
        'appid': BAIDU_APP_ID,
        'salt': '123456',  # 随机数，可以自行生成
        'sign': '',  # 此处留空，将在下一步生成
    }

    # 生成签名
    sign_str = f"{BAIDU_APP_ID}{text}{params['salt']}{BAIDU_APP_KEY}"
    params['sign'] = hashlib.md5(sign_str.encode()).hexdigest()

    # 发送API请求
    response = requests.get(BAIDU_API_URL, params=params)
    translation = response.json()

    if 'trans_result' in translation:
        return translation['trans_result'][0]['dst']
    else:
        return text  # 如果翻译失败，返回原文本
    
def translate_html(file_path, target_language='en'):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')
    texts = soup.find_all(string=True)

    for text in texts:
        if text.parent.name in ['script', 'style']:
            continue
        translated_text = translate_text_with_baidu(text, target_language)
        text.replace_with(translated_text)

    new_file_path = f'translated_{os.path.basename(file_path)}'
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))

def process_directory(directory, target_language='en'):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                print(f"Translating: {file_path}")
                translate_html(file_path, target_language)

# Replace this path with your actual directory path
directory_path = '/Users/yisuanwang/Desktop/image2html/Image2HTML-Benchmark/dataset_clean_imgrep_en'
process_directory(directory_path)
