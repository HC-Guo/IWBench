from playwright.sync_api import sync_playwright
import base64
import os

def process(url_or_path="https://example.com"):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_context().new_page()
        if url_or_path.startswith("http") or url_or_path.startswith("https"):
            page.goto(url_or_path)
        elif url_or_path.startswith("file://"):
            page.goto(url_or_path)
        else:
            page.goto("file://" + os.path.abspath(url_or_path))
        page.screenshot(path=f'{url_or_path}.png',full_page=True)
        screenshot_bytes = page.screenshot(full_page=True)
        html_image_code = base64.b64encode(screenshot_bytes).decode('utf-8')
        html_content = page.content()
        page.close()
        browser.close()
    return html_content, html_image_code


if __name__ == "__main__":
    url_or_path_list = ["https://example.com", "https://google.com"]
    for url_or_path in url_or_path_list:
        print(process(url_or_path=url_or_path))
