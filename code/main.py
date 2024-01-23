from playwright_utils import PlaywrightUtils
from html_processor import process
from html_simplifier import simplify
from html_tree_serializer import serialize
from html_comparer import compare
from injection_js import inject_javascript
from cot import cot
import os

def main():
    # url_or_path_list = ["https://example.com", "https://google.com", "code_/unit_test_case/google_301.html"]
    url_or_path = "unit_test_case/google_301.html"
    output_dir = "result/data/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    

    playwright_utils = PlaywrightUtils()
    gt_html, gt_screenshot = process(playwright_utils, url_or_path=url_or_path)
    simplify_html, removed_elements = simplify(playwright_utils, gt_html)
    screenshot, result = inject_javascript(playwright_utils, url_or_path)
    cot_result = cot(screenshot)

    data1 = serialize(playwright_utils, simplify_html)
    data2 = serialize(playwright_utils, cot_result)
    
    sim = compare(data1, data2, 0.4)
    print(data1, "\n" * 10, data2, "\n" * 10, sim)
    
if __name__ == "__main__":
    main()