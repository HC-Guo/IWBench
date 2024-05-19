from playwright.sync_api import sync_playwright
import os
import base64

class PlaywrightUtils:
    def __init__(self, headless=True) -> None:
        self.playwright = None
        self.browser = None
        self.page = None
        self.headless = headless

    def start_browser(self):
        if self.playwright is None:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=self.headless)
            self.page = self.browser.new_page()
        return self.playwright, self.browser, self.page

    def check(self):
        if self.page is None:
            self.start_browser()

    def wait(self, t=5000):
        self.check()
        self.page.wait_for_timeout(t)

    def evaluate(self, js):
        self.check()
        return self.page.evaluate(js)

    def take_screenshot(self, path):
        self.check()
        self.page.screenshot(path=path, full_page=True)

    def take_screenshot_code(self):
        self.check()
        screenshot_bytes = self.page.screenshot(full_page=True)
        return base64.b64encode(screenshot_bytes).decode('utf-8')

    def render_html(self):
        self.check()
        c = self.page.content()
        return c

    def goto(self, url_or_path):
        self.check()
        if url_or_path.startswith("http") or url_or_path.startswith("https"):
            self.page.goto(url_or_path)
        elif url_or_path.startswith("file://"):
            self.page.goto(url_or_path)
        else:
            self.page.goto("file://" + os.path.abspath(url_or_path))

    def set_content(self, content):
        self.check()
        self.page.set_content(content)
            
    def close_browser(self):
        self.browser.close()
        self.playwright.stop()

    def __del__(self):
        try:
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
        except Exception as e:
            print(f"Error closing Playwright: {e}")

if __name__ == "__main__":
    pu = PlaywrightUtils(headless=False)
    pu.goto("https://www.baidu.com")
    pu.take_screenshot("baidu.png")
    print(pu.take_screenshot_code())
    pu.close_browser()