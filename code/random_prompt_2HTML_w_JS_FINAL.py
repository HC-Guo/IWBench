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
import os
import sys

import random
import requests
import openai
import argparse

# 原始固定Prompt模板
basic_template = "现在你是设计网站的HTML专家，我会给你一些设计一个网站需要包含的元素, 括号[]内为要包含的元素，即[需要包含的元素]，请你根据这些需要包含的元素生成对应的网站HTML代码，每个网站确保有CSS样式"

# # Medium 模板 1
template_dic = {"prompt1": "现在你是设计网站的HTML专家，我会给你一些设计一个网站的相应要求，请帮设计一个具有现代美学的静态网页，用于展示一个摄影师的作品集。包括一个带有高分辨率图片和光滑过渡效果的图像画廊，一个关于摄影师的专业背景和艺术理念的详细介绍页面，联系信息页以及快速链接到摄影师的各个社交媒体账户。整个网站应该响应式设计，适应不同设备的显示；另外我会给你一些其它在这个网页里需要包含的元素, 括号[]内为要包含的元素，即[需要包含的元素]。另外还需要包含一些JavaScript(JS)的功能，括号[]内为要包含的JS功能，即[需要包含的JS功能]。请你根据这些要求生成对应的网站HTML代码，每个网站确保有CSS样式。需要注意的是千万不能把上面这段文字内容直接显示在生成的网页里，确保HTML是符合需求的和干净的",

# # Medium 模板 2
"prompt2": "现在你是设计网站的HTML专家，我会给你一些设计一个网站的相应要求，请帮创建一个具有地理定位功能的新闻网站主页，能够根据用户的IP地址显示最新的地方新闻、天气更新和紧急通知。页面设计应当现代且用户友好，包含一个动态新闻滚动条、实时天气小组件、以及一个用户可以自定义内容的个人化仪表板。页面还应提供一个高级搜索功能，使用户能够根据关键词、日期或类别查找新闻；另外我会给你一些其它在这个网页里需要包含的元素, 括号[]内为要包含的元素，即[需要包含的元素]。另外还需要包含一些JavaScript(JS)的功能，括号[]内为要包含的JS功能，即[需要包含的JS功能]。请你根据这些要求生成对应的网站HTML代码，每个网站确保有CSS样式。需要注意的是千万不能把上面这段文字内容直接显示在生成的网页里，确保HTML是符合需求的和干净的",

# # Medium 模板 3
"prompt3": "现在你是设计网站的HTML专家，我会给你一些设计一个网站的相应要求，请帮创建设计一个企业内部使用的门户网站，集成关键的公司资源和服务。该网站应包括动态新闻发布板块、一个完整的员工目录，内部论坛支持员工之间的交流和讨论，工作流程管理工具以及安全的文档共享和协作平台。网站界面应简洁、易于导航，且具备强大的搜索功能和个人化设置选项；另外我会给你一些其它在这个网页里需要包含的元素, 括号[]内为要包含的元素，即[需要包含的元素]。另外还需要包含一些JavaScript(JS)的功能，括号[]内为要包含的JS功能，即[需要包含的JS功能]。请你根据这些要求生成对应的网站HTML代码，每个网站确保有CSS样式。需要注意的是千万不能把上面这段文字内容直接显示在生成的网页里，确保HTML是符合需求的和干净的",

# Medium 模板 4
"prompt4": "现在你是设计网站的HTML专家，我会给你一些设计一个网站的相应要求，请帮构建一个在线时尚服装店的网页，专注于展示最新的服饰潮流。网页应包含多个分类，如“新品上市”、“热销商品”、“折扣专区”，每个产品页面应提供高清图片、详细的产品描述、尺码信息、用户评价和一个简单的购物流程。网站还应支持安全支付、订单跟踪和客户服务聊天功能；另外我会给你一些其它在这个网页里需要包含的元素, 括号[]内为要包含的元素，即[需要包含的元素]。另外还需要包含一些JavaScript(JS)的功能，括号[]内为要包含的JS功能，即[需要包含的JS功能]。请你根据这些要求生成对应的网站HTML代码，每个网站确保有CSS样式。需要注意的是千万不能把上面这段文字内容直接显示在生成的网页里，确保HTML是符合需求的和干净的",

# Medium 模板 5
"prompt5": "现在你是设计网站的HTML专家，我会给你一些设计一个网站的相应要求，请帮设计一个以个人旅行和美食体验为主题的博客网站。每篇博客应包含丰富的图文内容，如旅行目的地的详细介绍、美食推荐、个人故事和旅行小贴士。网站应包含一个互动的评论区，允许读者留言和分享，并有一个月度最佳博客展示板块。整个网站应具备优化的SEO功能和自适应不同屏幕大小的设计；另外我会给你一些其它在这个网页里需要包含的元素, 括号[]内为要包含的元素，即[需要包含的元素]。另外还需要包含一些JavaScript(JS)的功能，括号[]内为要包含的JS功能，即[需要包含的JS功能]。请你根据这些要求生成对应的网站HTML代码，每个网站确保有CSS样式。需要注意的是千万不能把上面这段文字内容直接显示在生成的网页里，确保HTML是符合需求的和干净的",

# Medium 模板 6
"prompt6": "现在你是设计网站的HTML专家，我会给你一些设计一个网站的相应要求，请帮创建一个提供多种在线编程课程的教育平台。每个课程应该有详细的概述、学习目标、视频教程、可下载的练习材料、在线编程练习环境和一个用户可以互动的论坛。网站还应包括一个个人成就追踪系统，使用户能够看到他们的学习进度和获得的徽章或证书。另外需要构建一个网站目录，关注教育资源。目录应该有清晰的分类，如“在线课程”、“学术研究”、“学习工具”，并为每个链接提供详细的描述和评级。网站还应包括一个高效的搜索功能和用户推荐系统；另外我会给你一些其它在这个网页里需要包含的元素, 括号[]内为要包含的元素，即[需要包含的元素]。另外还需要包含一些JavaScript(JS)的功能，括号[]内为要包含的JS功能，即[需要包含的JS功能]。请你根据这些要求生成对应的网站HTML代码，每个网站确保有CSS样式。需要注意的是千万不能把上面这段文字内容直接显示在生成的网页里，确保HTML是符合需求的和干净的",

# Medium 模板 7
"prompt7": "现在你是设计网站的HTML专家，我会给你一些设计一个网站的相应要求，请帮设计一个具有现代界面和强大社交功能的社交网络平台。用户可以创建个人资料，发布状态更新，分享图片和视频，与朋友互动。平台应提供高级的隐私设置，允许用户控制谁可以看到他们的内容。此外，还应该有一个推荐系统，根据用户的兴趣和互动展示相关的内容；另外我会给你一些其它在这个网页里需要包含的元素, 括号[]内为要包含的元素，即[需要包含的元素]。另外还需要包含一些JavaScript(JS)的功能，括号[]内为要包含的JS功能，即[需要包含的JS功能]。请你根据这些要求生成对应的网站HTML代码，每个网站确保有CSS样式。需要注意的是千万不能把上面这段文字内容直接显示在生成的网页里，确保HTML是符合需求的和干净的",

# Medium 模板 8
"prompt8": "现在你是设计网站的HTML专家，我会给你一些设计一个网站的相应要求，请帮构建一个以科技新闻为主题的网站，提供最新的科技新闻报道、深度分析文章、播客和视频内容。页面设计应具备现代感和易用性，包括一个新闻滚动条、视频播放区域、热门话题板块以及一个用于订阅电子报的部分；另外我会给你一些其它在这个网页里需要包含的元素, 括号[]内为要包含的元素，即[需要包含的元素]。另外还需要包含一些JavaScript(JS)的功能，括号[]内为要包含的JS功能，即[需要包含的JS功能]。请你根据这些要求生成对应的网站HTML代码，每个网站确保有CSS样式。需要注意的是千万不能把上面这段文字内容直接显示在生成的网页里，确保HTML是符合需求的和干净的",

# Medium 模板 9
"prompt9": "现在你是设计网站的HTML专家，我会给你一些设计一个网站的相应要求，请帮设计一个环保主题的论坛网站，提供多个不同的讨论板块，如“可持续生活方式”、“环境保护法律”、“环保活动和倡议”。论坛应该有一个用户友好的界面，支持用户发布和编辑帖子，进行投票和参与版主监管的讨论；另外我会给你一些其它在这个网页里需要包含的元素, 括号[]内为要包含的元素，即[需要包含的元素]。另外还需要包含一些JavaScript(JS)的功能，括号[]内为要包含的JS功能，即[需要包含的JS功能]。请你根据这些要求生成对应的网站HTML代码，每个网站确保有CSS样式。需要注意的是千万不能把上面这段文字内容直接显示在生成的网页里，确保HTML是符合需求的和干净的",

# Medium 模板 10
"prompt10": "现在你是设计网站的HTML专家，我会给你一些设计一个网站的相应要求，请帮创建一个集中最新电影和电视剧评价的聚合网站。网站应包括一个实时更新的评论板块，用户评分系统，以及直接链接到不同流媒体平台的观看选项。页面设计应简洁且易于导航，支持用户自定义他们的内容偏好；另外我会给你一些其它在这个网页里需要包含的元素, 括号[]内为要包含的元素，即[需要包含的元素]。另外还需要包含一些JavaScript(JS)的功能，括号[]内为要包含的JS功能，即[需要包含的JS功能]。请你根据这些要求生成对应的网站HTML代码，每个网站确保有CSS样式。需要注意的是千万不能把上面这段文字内容直接显示在生成的网页里，确保HTML是符合需求的和干净的"}

# 三个不同复杂程度网页的元素列表
easy = ["标题", "图像", "图标", "卡片布局", "滑动横幅/轮播", "页脚", "边栏", "背景图像和图案"]  # 简单HTML包含元素
medium = ["标题", "超链接和按钮", "图像", "音频", "滑动横幅/轮播", "卡片布局", "导航栏", "页脚", "边栏", "面包屑导航", "背景图像和图案", "视频", "社交分享按钮"]  # 中等HTML包含元素
hard = ["标题", "超链接和按钮", "图像", "音频", "滑动横幅/轮播", "卡片布局", "导航栏", "页脚", "边栏", "面包屑导航", "背景图像和图案", "视频", "社交分享按钮", "进度条和加载动画", "评论区", "选项卡或折叠面板", "模态窗口/弹出框", "表单", "搜索栏"]  # 复杂HTML包含元素

js_events = ['onclick', 'onload', 'onmouseover', 'onmouseout', 
          'onchange', 'onsubmit', 'onmousemove', 'onmouseup', 
          'onmousedown', 'ondblclick', 'onkeydown', 'onkeyup',
          'onkeypress', 'onsubmit', 'onfocus', 'onblur'
          'oninput', 'onload', 'onresize', 'onscroll',
          'onunload', 'ontouchstart', 'ontouchmove', 'ontouchend',
          'onerror', 'oncontextmenu']

# 生成prompts的函数
def generate_prompts(template_contents, list_elements, num_elements, list_js, num_js, num_prompts):
    prompts = []
    for _ in range(num_prompts):
        selected_ele = random.sample(list_elements, num_elements)
        selected_js = random.sample(list_js, num_js)
        # selected_elements = selected_ele + selected_js
        template_contents1 = template_contents.replace('需要包含的元素', ', '.join(selected_ele))
        template_contents2 = template_contents1.replace('需要包含的JS功能', ', '.join(selected_js))
        prompts.append(template_contents2)
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

def generate_and_save_html(html_folder, prompts, api_key, model_name):
    """
    生成并保存HTML代码。
    :param prompts: 一个字典，包含三个列表的prompts。
    :param api_key: GPT-4 API密钥。
    """
    for list_name, prompts_list in prompts.items():
        for i, prompt in enumerate(prompts_list, start=1):
            html_code = call_gpt4_api(prompt, api_key, model_name)

            # file_name = f"/Users/guxiao/Documents/ICML/prompt4_html/{list_name}_{i}.html"  # TODO: 改folder
            file_name = html_folder + f"{list_name}_{i}.html"  # TODO: 改folder

            with open(file_name, 'w') as file:
                file.write(html_code)
            print(f"HTML代码已保存为: {file_name}")

# Parse parameters
parser = argparse.ArgumentParser()
parser.add_argument('-t', type=str, help='Name of prompt template', default=basic_template)
args = parser.parse_args()

# Assign the args value to corresponding prompt
prompt_template = args.t
template_contents = template_dic[args.t]

# 创建每个prompt模板对应的存储路径
if not os.path.exists("/ICML/{}_html_js/".format(prompt_template)):
    os.makedirs("/ICML/{}_html_js/".format(prompt_template))

html_folder = "/ICML/{}_html_js/".format(prompt_template)

# 生成prompts
prompts_list1 = generate_prompts(template_contents, easy, 3, js_events, 3, 10)  # 简单HTML，随机抽样30次
prompts_list2 = generate_prompts(template_contents, medium, 5, js_events, 5, 10)  # 中等HTML，随机抽样30次
prompts_list3 = generate_prompts(template_contents, hard, 8, js_events, 8, 10)  # 复杂HTML，随机抽样30次

stored_prompts_path = html_folder + f"{prompt_template}_easy_medium_hard.txt"
print(f'Type of prompts_list: {type(prompts_list1)}')

with open(stored_prompts_path, 'w') as file:
    file.write("Easy:\n")
    file.write(', '.join(map(str, prompts_list1)) + '\n')
    file.write("Medium:\n")
    file.write(', '.join(map(str, prompts_list2)) + '\n')
    file.write("Hard:\n")
    file.write(', '.join(map(str, prompts_list3)) + '\n')

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
generate_and_save_html(html_folder, prompts, api_key, model_name)

#使用示例：
# 命令行输入：python random_prompt_2HTML_w_JS_FINAL.py -t prompt1



