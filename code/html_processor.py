import os
from playwright_utils import PlaywrightUtils


def process(playwright_utils=None, url_or_path="https://example.com", output_file="process.html"):
    if playwright_utils is None:
        playwright_utils = PlaywrightUtils()
    playwright_utils.goto(url_or_path)
    html_content = playwright_utils.render_html()
    html_screenshot = playwright_utils.take_screenshot_code()
    # with open(output_file, 'w') as f:
    #     f.write(c)
    # html_screenshot = playwright_utils.take_screenshot(output_file.replace(".html", ".png"))
    # playwright_utils.take_screenshot(output_file.replace(".html", ".png"))
    return html_content, html_screenshot


if __name__ == "__main__":
    url_or_path_list = ["https://example.com", "https://google.com"]
    playwright_utils = PlaywrightUtils()
    for url_or_path in url_or_path_list:
        print(process(playwright_utils=playwright_utils, url_or_path=url_or_path))
