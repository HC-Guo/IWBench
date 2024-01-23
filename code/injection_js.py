from playwright_utils import PlaywrightUtils

def inject_javascript(playwright_utils=None, path=""):
    if playwright_utils is None:
        playwright_utils = PlaywrightUtils()
    playwright_utils.goto(path)
    path_to_js_file ="pagemark.js"
    with open(path_to_js_file, 'r') as file:
        content = file.read()
        # The result of the JavaScript execution will be returned here
        result = playwright_utils.evaluate(content)
        playwright_utils.take_screenshot("evaluate.png")
        screenshot = playwright_utils.take_screenshot_code()
    return screenshot, result


if __name__ == "__main__":    
    # path = "https://www.google.com/"
    # path = "file:///Users/knediny/html/Image2HTML-Benchmark/code/evaluate/url-herokucdn-404/index.html"
    # path = "file:///Users/knediny/html/Image2HTML-Benchmark/code/evaluate/responsive-html-email-template/email.html"
    # path = "file:///Users/knediny/html/Image2HTML-Benchmark/code/evaluate/simple-html-invoice-template/invoice.html"
    path = "file:///Users/knediny/html_code/code_/unit_test_case/Google.html"

    playwright_utils = PlaywrightUtils(headless=False)
    screenshot, result = inject_javascript(playwright_utils=playwright_utils, path=path)
    # playwright_utils.wait(10000)
    print(screenshot)
    print(result)

    # from coco_merge import merge_bboxes
    # a = merge_bboxes(result)
    # print(result)
    # print(a)

