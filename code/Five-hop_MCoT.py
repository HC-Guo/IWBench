
from openai import OpenAI
from injection_js import inject_javascript
from upload_file import upload_file_by_file_content
import os
import pandas as pd
import re
from setting import OPENAI_API_KEY
import uuid
from playwright.sync_api import sync_playwright, TimeoutError
import base64
import random

def image_code2image_url(image_code):
    return upload_file_by_file_content(image_code)

def html_content2image_url(html_content):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_context().new_page()
        page.set_content(html_content)
        screenshot_bytes = page.screenshot(full_page=True)
        image_code = base64.b64encode(screenshot_bytes).decode('utf-8')
        page.close()
        browser.close()
    url = image_code2image_url(image_code)
    return url

def chat(shared_messages):
    client = OpenAI(
        api_key=OPENAI_API_KEY,
    )
    completion = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=shared_messages,
        max_tokens=4096
    )
    return completion.choices[0].message.content
    
def parse_solution_answer(solution_answer):
    pattern = r'```html(.*?)```'
    solution_answer = re.findall(pattern, solution_answer, re.DOTALL)
    solution_answer = "\n".join(solution_answer)
    solution_answer = re.sub(r'<img\s+[^>]*src="[^"]*"[^>]*>', 
                            f'<img src="https://picsum.photos/seed/picsum/200/300" alt="Image">', 
                            solution_answer)
    solution_answer = solution_answer.encode('utf-8', 'replace').decode('utf-8')
    return solution_answer

def qa(shared_messages, question):
    shared_messages.append({"role": "user", "content": question})
    answer = chat(shared_messages)
    shared_messages.append({"role": "assistant", "content": answer})
    return shared_messages, answer

def cot(shared_messages, coco_image_code):
    # First QA
    first_question = [
        {
           "type": "text",
           "text": "First, analyze this screenshot of the webpage, please try your best to identify and describe this webpage’s functions and its web elements. Some of these elements have been numerically labeled in sequence with bounding boxes."
        },
        {
            "type": "image_url",
            "image_url": {
                "url": image_code2image_url(coco_image_code)
            },
        }
    ]
    shared_messages, first_answer = qa(shared_messages, first_question)
    
    # Second QA
    second_question = [
        {
           "type": "text",
           "text": "The second step is to demonstrate the positional relationships of the marked web page elements based on the provided bounding boxes, including the overall layout and the relative positions between elements."
        },
    ]
    shared_messages, second_answer = qa(shared_messages, second_question)

    # Third QA
    third_question = [
        {
           "type": "text",
           "text": "Please as per the above descriptions of the webpage’s overall layout and web elements together with their relative positioning, generate HTML code for the corresponding original web image by skipping the step of assigning bounding boxes to elements."
        },
    ]
    shared_messages, third_answer = qa(shared_messages, third_question)
    return shared_messages, third_answer

def reflect(shared_messages, coco_image_code, generate_html):
    # Forth QA
    forth_question = [
        {
            "type": "image_url",
            "image_url": {
                "url": image_code2image_url(coco_image_code)
            },
        },
        {
            "type": "image_url",
            "image_url": {
                "url": html_content2image_url(generate_html)
            },
        },
        {
           "type": "text",
           "text": "Please compare the two screenshots of webpages. The latter is the screenshot of the webpage by the HTML code you just provided. Based on the above web element descriptions and layout information, please identify whether there are missing elements and access whether the layout and elements’ relative positioning are correct. Afterwards, please improve the HTML code accordingly."
        },
    ]
    
    shared_messages, forth_answer = qa(shared_messages, forth_question)
    return shared_messages, forth_answer


directory = "ICML_"
output_dir = "reflect-times-inference-result/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
html_pairs = []
for root, dirs, files in os.walk(directory):
    for filename in files:
        if filename.endswith(".htmlcoco.base64"):
            if (random.random() < 0.05):
                continue
            file_path = os.path.join(root, filename)
            print("Processing: ", file_path)
            try:
                htmls = []
                shared_messages = [
                    {"role": "system", "content": "You are a helpful assistant."}
                ]
                # pu = PlaywrightUtils()
                # coco_image_code, _ = inject_javascript(pu, file_path)
                # pu.close_browser()

                with open(file_path, "r") as f:
                    coco_image_code = f.read()
                shared_messages, cot_answer = cot(shared_messages, coco_image_code)
                pre_answer_html = parse_solution_answer(cot_answer)
                print(f"COT Answer >>> {pre_answer_html}")
                htmls.append(pre_answer_html)
                reflect_times = 10
                for i in range(reflect_times):
                    shared_messages, reflect_answer = reflect(shared_messages, coco_image_code, pre_answer_html)
                    pre_answer_html = parse_solution_answer(reflect_answer)
                    print(f"Reflect Answer >>> {reflect_answer}")
                    htmls.append(pre_answer_html)
                
                print(shared_messages)
                shared_messages = [
                    {"role": "system", "content": "You are a helpful assistant."}
                ]
                for index, generated_html in enumerate(htmls):
                    generated_filename = f"{str(uuid.uuid4())}{filename.replace('.html', f'-{index}.html')}"
                    generated_file_path = f"{output_dir}/{generated_filename}"

                    html_pairs.append((file_path, generated_file_path))

                    with open(generated_file_path, "w") as f:
                        f.write(generated_html)
                print("Generated HTMLs >>> ", len(htmls))
                print("HTML Pairs >>> ", len(html_pairs))
                print("HTML Pairs >>> ", html_pairs)
            except TimeoutError as e:
                print(f"Timeout occurred while processing {file_path}: {e}")

csv_filename = f"{output_dir}/file_pairs.csv"
df = pd.DataFrame(html_pairs, columns=["Original", "Generated"])
df.to_csv(csv_filename, index=False)
