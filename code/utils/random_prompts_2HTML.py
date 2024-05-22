# Author: Yaonan Gu, yaonangu@u.nus.edu
# Date: 2024.01.12

"""
这个脚本使用OpenAI的GPT-4 API来自动生成HTML代码。它首先定义了两个函数：一个用于调用API生成HTML代码，
另一个用于将生成的HTML代码保存到文件中。这个脚本旨在通过提供的prompts生成HTML代码，并将每个生成的HTML文件
按照特定的命名规则保存。

主要步骤如下：
1. `call_gpt4_api` 函数接收一个prompt和API密钥，调用OpenAI的GPT-4 API，并返回生成的HTML代码。
2. `generate_and_save_html` 函数接收一个prompts字典和API密钥，使用`call_gpt4_api`函数处理每个prompt，
   并将结果保存为HTML文件，文件名由列表名称和序号组成。
3. 脚本最后部分调用 `generate_and_save_html` 函数，实际执行HTML代码的生成和保存操作。

请注意，在实际使用此脚本之前，需要替换 `api_key` 变量的值为自己的OpenAI API密钥。
"""

import random
import requests
import openai

# 原始固定Prompt模板
base_prompt = "现在你是设计网站的HTML专家，我会给你一些设计一个网站需要包含的元素, 括号[]内为要包含的元素，即[需要包含的元素]，请你根据这些需要包含的元素生成对应的网站HTML代码，每个网站确保有CSS样式"

# 三个不同复杂程度网页的元素列表
easy = ["标题", "图像", "图标", "卡片布局", "滑动横幅/轮播", "页脚", "边栏", "背景图像和图案"]  # 简单HTML包含元素
medium = ["标题", "超链接和按钮", "图像", "音频", "滑动横幅/轮播", "卡片布局", "导航栏", "页脚", "边栏", "面包屑导航", "背景图像和图案", "视频", "社交分享按钮"]  # 中等HTML包含元素
hard = ["标题", "超链接和按钮", "图像", "音频", "滑动横幅/轮播", "卡片布局", "导航栏", "页脚", "边栏", "面包屑导航", "背景图像和图案", "视频", "社交分享按钮", "进度条和加载动画", "评论区", "选项卡或折叠面板", "模态窗口/弹出框", "表单", "搜索栏"]  # 复杂HTML包含元素

# 生成prompts的函数
def generate_prompts(list_elements, num_elements, num_prompts):
    prompts = []
    for _ in range(num_prompts):
        selected_elements = random.sample(list_elements, num_elements)
        prompts.append(base_prompt.replace('需要包含的元素', ', '.join(selected_elements)))
    return prompts

# Prompt传到GPT4的API，生成HTML，分别命名并保存
def call_gpt4_api(prompt, api_key, model_name):
    """
    使用OpenAI库调用GPT-4 API以生成HTML代码。
    :param prompt: 输入的prompt。
    :param api_key: GPT-4 API密钥。
    :return: 生成的HTML代码。
    """
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model= model_name,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return "Error: " + str(e)

def generate_and_save_html(prompts, api_key, model_name):
    """
    生成并保存HTML代码。
    :param prompts: 一个字典，包含三个列表的prompts。
    :param api_key: GPT-4 API密钥。
    """
    for list_name, prompts_list in prompts.items():
        for i, prompt in enumerate(prompts_list, start=1):
            html_code = call_gpt4_api(prompt, api_key, model_name)
            file_name = f"{list_name}_{i}.html"
            with open(file_name, 'w') as file:
                file.write(html_code)
            print(f"HTML代码已保存为: {file_name}")

# 生成prompts
prompts_list1 = generate_prompts(easy, 3, 30)  # 简单HTML，随机抽样30次
prompts_list2 = generate_prompts(medium, 5, 30)  # 中等HTML，随机抽样30次
prompts_list3 = generate_prompts(hard, 8, 30)  # 复杂HTML，随机抽样30次

# OpenAI API密钥
api_key = "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"
model_name = 'gpt-4'

# 写入之前生成的prompts
prompts = {
    "easy": prompts_list1,
    "medium": prompts_list2,
    "hard": prompts_list3
}

# 生成并保存HTML代码
generate_and_save_html(prompts, api_key, model_name)


