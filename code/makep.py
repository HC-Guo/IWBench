import os
import csv

# 设置文件夹路径,这里就是你的LMM推理得到的html代码
folder_path = "/mnt/chenjh/i2h-bench/newgithub/Image2HTML-Benchmark/code/baseline/dataset-qwenvlchat-html"

# 创建一个CSV文件来保存路径
file_pairs = "file_pairs.csv"
csv_filename = f"{folder_path}/{file_pairs}"

# 遍历文件夹并收集.html文件的路径
html_files = []
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith("htmlcoco.html"):
            continue
        if file.endswith(".html"):
            # 第一列的路径
            first_column_path = os.path.join("/mnt/chenjh/i2h-bench/newgithub/Image2HTML-Benchmark/dataset", file)
            # 第二列的路径
            second_column_path = os.path.join(root, file)
            html_files.append((first_column_path, second_column_path))

# 将路径写入CSV文件
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Original', 'Generated'])
    for paths in html_files:
        writer.writerow(paths)

print('save file_pairs.csv to', csv_filename)

