import os
import pandas as pd

def main():
    output_dir = "benchmark-result/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    csv_filename = "inference-result/file_pairs.csv"
    df = pd.read_csv(csv_filename)
    results = []
    for index, row in df.iterrows():
        file_name1 = row['Original']
        file_name2 = row['Generated']

        pu = PlaywrightUtils()
        gt_html, gt_screenshot = process(pu, file_name1)
        simplify_html, removed_elements = simplify(pu, gt_html)
        data1 = serialize(pu, simplify_html)

        with open(file_name2, "r") as f:
            html2 = f.read()
        data2 = serialize(pu, html2)
        
        sim = compare(data1, data2, 0.4)
        
        results.append([file_name1, file_name2, sim])
        pu.close_browser()
        
        results_csv_filename = "benchmark-result/comparison_results.csv"
        results_df = pd.DataFrame(results, columns=["Original", "Generated", "Similarity"])
        results_df.to_csv(results_csv_filename, index=False)

if __name__ == "__main__":
    main()
