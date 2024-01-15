# baseline生成html的统一脚本
# 步骤：
# 1.找到GT的html
# 2.clean GThtml：删除注释，替换GT html里的缺失图片资源，删除隐藏元素
# 3.转GT image并且coco标注
# 4.标注好的图输入COT进行image2html
# 6.删除隐藏元素
# 5.比较原始html和生成的html的相似度

from injection_js import inject_javascript_and_get_result
from GPT4vCOT.chatCOT import generateAnswer as GPT4v_answer

def generateImage2Html(GT_html_path: str, model_name: str):
    # GT_path是html的路径
    # coco标注
    coco_image_path = './tmp.png'
    cocores = inject_javascript_and_get_result(GT_html_path, coco_image_path)
    # print(cocores)
    if model_name == 'gpt4v':
        return GPT4v_answer(coco_image_path)
    elif model_name == 'tongyi':
        pass
    elif model_name == 'llava':
        pass
    pass


if __name__ == '__main__':
    # 转换GT html to image

    res = generateImage2Html(GT_html_path='file:///Users/yisuanwang/Desktop/image2html/src/compareHtml/data/case2/google.html',
                       model_name='gpt4v')
    print(res) # 这个地方出来的是llm根据GT html转image生成的html