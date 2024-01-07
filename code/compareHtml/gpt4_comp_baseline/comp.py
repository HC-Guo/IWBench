import difflib
from .service import Service
from .gpt4_api import OpenaiService

def read_file(file_path):
    """读取文件内容并返回其行列表"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def compare_files(file1_path, file2_path):
    """比较两个文件并打印它们的不同之处"""
    file1_lines = read_file(file1_path)
    file2_lines = read_file(file2_path)

    # 使用difflib比较文件内容
    d = difflib.Differ()
    diff = d.compare(file1_lines, file2_lines)

    # 打印结果
    print('\n'.join(diff))

def comp_html_file(path1='./data/index1.html', path2='./data/index2.html'):
    htmlA = read_file(path1)
    htmlB = read_file(path2)
    service = OpenaiService('gpt-3.5-turbo')


    input = f'''
I have the code for two HTML files, File A and File B. Please carefully compare the HTML elements in these two files and point out the major differences in their structure, style and functionality.

Example 1:
HTML A: '<div><p>Hello World</p></div>'
HTML B: '<div><p>Hello World</p></div>'
Comparison: No differences.
Score: 0

Example 2:
HTML A: '<header><h1>Title</h1></header>'
HTML B: '<header><h2>Title</h2></header>'
Comparison: Minor difference in header tag size (h1 vs h2).
Score: 2

Example 3:
HTML A: '<body style="background-color: blue;"></body>'
HTML B: '<body style="background-color: red;"></body>'
Comparison: Difference in background color style (blue vs red).
Score: 3

Now, compare and score the following HTML snippets:
HTML A: '{htmlA}'

HTML B: '{htmlB}'

The expected JSON output format:
{{
"comparison": "[Your Comparison Here]",
"score": "[Your Score Here]"
}}
'''

    res = service.make_request(input)
    print(res) # json
