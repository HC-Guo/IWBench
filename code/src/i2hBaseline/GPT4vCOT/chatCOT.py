# ----------------------------------------------------------------------------------
# - Author Contact: wei.zhang, zwpride@buaa.edu.cn (Original code)
# ----------------------------------------------------------------------------------

OPENAI_API_KEY = "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" # image2html


from openai import OpenAI
import base64

from html2image import Html2Image
import os

def screenshot(html_file, file_name):
    hti = Html2Image(browser='chrome', size=(1920, 1080))
    hti.screenshot(html_file=html_file, save_as=file_name)  # 仅传递文件名

def chat(message):
    client = OpenAI(
        api_key=OPENAI_API_KEY,
        # base_url="https://openai.zwpride.top/v1"
    )

    completion = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=message
    )
    return completion.choices[0].message.content
    
def parse_solution_answer(solution_answer):
    # print(solution_answer)
   # 这里要对回答的html进行一些过滤和处理，to do
   return solution_answer

def qa(question):
    message.append({"role": "user", "content": question})
    answer = chat(message)
    message.append({"role": "assistant", "content": answer})
    return answer

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def cot(coco_image_path):
    # First QA
    first_question = [
        {
           "type": "text",
           "text": "首先识别图片中的web元素并描述，其中大部分元素已经被boundingboxs标记。页面元素已经使用COCO Annotator进行了数字标记，请分析这张图片，并识别出网页的用途以及各个标记元素的功能。"
        },
        {
            "type": "image",
            "image": encode_image(coco_image_path) # coco标注之后的图像
        }
    ]
    first_answer = qa(first_question)
    
    # Second QA
    second_question = [
        {
           "type": "text",
           "text": "首先识别图片中的web元素并描述，其中大部分元素已经被boundingboxs标记。页面元素已经使用COCO Annotator进行了数字标记，请分析这张图片，并识别出网页的用途以及各个标记元素的功能。"
        },
    ]
    second_answer = qa(second_question)

    # Third QA
    third_question = [
        {
           "type": "text",
           "text": "根据上述web元素描述和整体布局和相对位置关系描述，生成原始图像对应的HTML代码，不需要生成boundingbox"
        },
    ]
    third_answer = qa(third_question)
    print(third_answer)

    # 将第三轮的回答转image作为image3
    file_path = './third_answer_qa.html'
    with open(file_path, 'w') as file:
        file.write(third_answer)

    screenshot(file_path, 'tmp-first.png')


    # Forth QA
    forth_question = [
        {
            "type": "image",
            "image": encode_image(coco_image_path) # coco标注之后的图像
        },
        {
            "type": "image",
            "image": encode_image("./tmp-first.png") # 第一轮生成的图像
        },
        {
           "type": "text",
           "text": "对比这两份web图像，后者是你生成的web代码产生的结果，根据上述的web元素描述和布局信息，分析是否有缺失元素，布局和相对位置是否正确，并给出代码修改意见"
        },
    ]
    
    forth_answer = qa(forth_question)

    # Fifth QA
    fifth_question = [
       {
            "type": "text",
            "text": "根据上述代码修改意见，修改你刚刚提供的代码"
       }
    ]
    fifth_answer = qa(fifth_question)

    return parse_solution_answer(fifth_answer)

message = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

def generateAnswer(coco_image_path: str):
    reshtml= cot(coco_image_path)
    print(reshtml)
    return reshtml
