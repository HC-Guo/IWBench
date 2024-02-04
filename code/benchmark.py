# ----------------------------------------------------------------------------------
# - Author Contact: wei.zhang, knediny@gmail.com (Original code)
# ----------------------------------------------------------------------------------
from utils.html.html_processor import process
from utils.html.html_simplifier import simplify
from utils.html.html_tree_serializer import serialize
from utils.html.html_comparer import compare
import os
import pandas as pd

def bench(input_dir, output_dir, file_pairs):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    csv_filename = f"{input_dir}/{file_pairs}"
    df = pd.read_csv(csv_filename)
    results = []
    for index, row in df.iterrows():
        file_name1 = row['Original']
        file_name2 = row['Generated']

        gt_html, gt_screenshot = process(file_name1)
        simplify_html, removed_elements = simplify(gt_html)
        data1 = serialize(simplify_html)

        with open(file_name2, "r") as f:
            html2 = f.read()
        data2 = serialize(html2)
        
        threshold = 0.9
        sim = compare(data1, data2, threshold)
        print(file_name1, file_name2, threshold, sim)
        results.append([file_name1, file_name2, threshold, sim[0], sim[1]])
        
        results_csv_filename = f"{output_dir}/{file_pairs}-comparison_results.csv"
        results_df = pd.DataFrame(results, columns=["Original", "Generated", "Threshold", "accuracy", "layout"])
        results_df.to_csv(results_csv_filename, index=False)


import sys
if __name__ == "__main__":
    input_dir = f"/UsersImage2HTML-Benchmark/code/benchmark-input"
    output_dir = f"benchmark-result"
    file_pairs = "file_pairs.csv"
    bench(input_dir, output_dir, file_pairs)