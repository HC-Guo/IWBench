from utils.playwright_utils import PlaywrightUtils

def inject_javascript(pu=None, path=""):
    if pu is None:
        pu = PlaywrightUtils()
    pu.goto(path)
    path_to_js_file ="utils/inference/pagemark.js"
    with open(path_to_js_file, 'r') as file:
        content = file.read()
        # The result of the JavaScript execution will be returned here
        coco_result = pu.evaluate(content)
        coco_image_code = pu.take_screenshot_code()
    return coco_image_code, coco_result