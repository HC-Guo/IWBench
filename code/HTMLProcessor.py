import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from urllib.parse import urlparse
import requests

class WebDriverManager:
    def __init__(self, headless=True, executable_path='./chromedriver-win64/chromedriver.exe'):
        self.executable_path = executable_path
        self.headless = headless
        self.driver = None

    def __enter__(self):
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        options.add_argument("--start-maximized")
        
        service = Service(executable_path=self.executable_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        return self.driver
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.driver is not None:
            self.driver.quit()

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def generate_file_path(base_dir, filename, extension):
    ensure_directory_exists(base_dir)
    return os.path.join(base_dir, f"{filename}.{extension}")

def get_base_filename(url_or_path, is_url=True):
    if is_url:
        parsed_url = urlparse(url_or_path)
        base_filename = f"{parsed_url.netloc}{parsed_url.path}".replace("/", "_").replace(":", "_").rstrip("_")
    else:
        base_filename = os.path.splitext(os.path.basename(url_or_path))[0]
    return base_filename

def rendering_html(source, is_url=True, driver_manager=None):
    with driver_manager as driver:
        if is_url:
            driver.get(source)
        else:
            html_path = "file:///" + os.path.abspath(source)
            driver.get(html_path)
        
        time.sleep(3)
        rendered_html = driver.page_source
        
        base_filename = get_base_filename(source, is_url)
        output_path = generate_file_path("rendered_html_files", base_filename, "html")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rendered_html)
    return output_path

def get_rendered_html(sources, driver_manager=None, is_url=True):
    rendered_html_paths = []
    for source in sources:
        output_path = rendering_html(source, is_url=is_url, driver_manager=driver_manager)
        rendered_html_paths.append(output_path)
        print(f"Rendered HTML for {source} saved as {output_path}")
    return rendered_html_paths

def convert_html_to_screenshot(file_path, driver_manager=None):
    with driver_manager as driver:
        driver.set_window_size(1920, 1080)
        html_path = "file:///" + os.path.abspath(file_path)
        driver.get(html_path)
        time.sleep(3)  # Wait for the page to load.
        
        base_filename = get_base_filename(file_path, is_url=False)
        screenshot_path = generate_file_path("screenshots", base_filename, "png")
        
        driver.save_screenshot(screenshot_path)
        
    return screenshot_path

def get_screenshot(file_paths, driver_manager=None):
    screenshots = []
    for file_path in file_paths:
        output_file = convert_html_to_screenshot(file_path, driver_manager)
        screenshots.append(output_file)
        print(f"Screenshot saved as {output_file}")
    return screenshots

def fetch_and_save_html(urls):
    html_paths = []
    output_dir = "html_files"
    ensure_directory_exists(output_dir)
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            filename = get_base_filename(url) + ".html"
            filepath = generate_file_path(output_dir, filename, "html")
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print(f"Saved HTML for {url} in {filepath}")
            html_paths.append(filepath)
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
    return html_paths


if __name__ == "__main__":
    # 输入数据
    urls_to_fetch = ["https://example.com"]
    local_html_to_render = ["./test/index1.html", "./test/index2.html"]
    local_html_to_screenshot = ["./test/index1.html", "./test/index2.html"]

    # 初始化WebDriverManager
    chrome_driver_path = "./chromedriver-win64/chromedriver.exe"
    driver_manager = WebDriverManager(executable_path=chrome_driver_path)


    # 爬取并保存URL列表中的HTML内容
    fetched_html_paths = fetch_and_save_html(urls_to_fetch)

    # 渲染爬取的HTML并获取截图
    rendered_html_paths_from_urls = get_rendered_html(fetched_html_paths, driver_manager=driver_manager, is_url=False)
    screenshots_from_urls = get_screenshot(rendered_html_paths_from_urls, driver_manager=driver_manager)

    # 渲染本地需要渲染的HTML文件并获取截图
    rendered_html_paths_local = get_rendered_html(local_html_to_render, driver_manager=driver_manager, is_url=False)
    screenshots_from_local_rendered = get_screenshot(rendered_html_paths_local, driver_manager=driver_manager)

    # 直接对本地无需渲染的HTML文件获取截图
    screenshots_from_local_direct = get_screenshot(local_html_to_screenshot, driver_manager=driver_manager)

    print("done")