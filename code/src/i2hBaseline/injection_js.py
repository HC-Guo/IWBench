from playwright.sync_api import sync_playwright
import base64

def inject_javascript_and_get_result(path, image_save_path):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(path)
        path_to_js_file ="/Users/yisuanwang/Desktop/image2html/src/baseline/pagemark_.js"
        with open(path_to_js_file, 'r') as file:
            content = file.read()
            # The result of the JavaScript execution will be returned here
            result = page.evaluate(content)
        # page.wait_for_timeout(5000)
        page.screenshot(path=image_save_path, full_page=True)
        # screenshot_bytes = page.screenshot()
        # print(base64.b64encode(screenshot_bytes).decode())
        context.close()
        browser.close()
    return result


if __name__ == "__main__":    
    # path = "https://www.google.com/"
    # path = "file:///Users/knediny/html/Image2HTML-Benchmark/code/evaluate/url-herokucdn-404/index.html"
    # path = "file:///Users/knediny/html/Image2HTML-Benchmark/code/evaluate/responsive-html-email-template/email.html"
    # path = "file:///Users/knediny/html/Image2HTML-Benchmark/code/evaluate/simple-html-invoice-template/invoice.html"
    path = "file:///Users/yisuanwang/Desktop/image2html/src/compareHtml/data/case2/google.html" # GT
    result = inject_javascript_and_get_result(path, './tmp.png')

    # import coco_mege
    # a = coco_mege.merge_bboxes(result)
    # print(result)
    # print(a)

