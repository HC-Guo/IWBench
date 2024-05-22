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
        self.device_name = "desktop"

    def start_driver(self):
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        options.add_argument("--start-maximized")

        service = Service(executable_path=self.executable_path)
        self.driver = webdriver.Chrome(service=service, options=options)

    def set_device(self, device_name):
        self.device_name = device_name.lower()
        if self.driver is None:
            raise RuntimeError("Driver not initialized. Call 'start_driver' before setting device.")
            
        mobile_emulation = {
            "deviceMetrics": {"width": 400, "height": 1100, "pixelRatio": 3.0},
            "userAgent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36"
        }

        if self.device_name == "mobile":
            self.driver.set_window_size(mobile_emulation["deviceMetrics"]["width"],
                                        mobile_emulation["deviceMetrics"]["height"])
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": mobile_emulation["userAgent"]})
        elif self.device_name == "desktop":
            self.driver.set_window_size(1920, 1080)
        else:
            print(f"Device type '{self.device_name}' is not recognized. Defaulting to desktop settings.")
            self.driver.set_window_size(1920, 1080)

    def quit_driver(self):
        if self.driver is not None:
            self.driver.quit()

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def generate_file_path(base_dir, filename, extension, device_name=""):
    ensure_directory_exists(base_dir)
    if device_name:
        filename = f"{filename}_{device_name}"
    return os.path.join(base_dir, f"{filename}.{extension}")

def get_base_filename(url_or_path, is_url=True):
    if is_url:
        parsed_url = urlparse(url_or_path)
        base_filename = f"{parsed_url.netloc}{parsed_url.path}".replace("/", "_").replace(":", "_").rstrip("_")
    else:
        base_filename = os.path.splitext(os.path.basename(url_or_path))[0]
    return base_filename

def rendering_html(source, is_url=True, driver_manager=None):
    if is_url:
        driver_manager.driver.get(source)
    else:
        html_path = "file:///" + os.path.abspath(source)
        driver_manager.driver.get(html_path)
    
    time.sleep(3)
    rendered_html = driver_manager.driver.page_source
    
    base_filename = get_base_filename(source, is_url)
    output_path = generate_file_path("rendered_html_files", base_filename, "html", driver_manager.device_name)

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
    html_path = "file:///" + os.path.abspath(file_path)
    driver_manager.driver.get(html_path)
    time.sleep(3)  # Wait for the page to load.
    base_filename = get_base_filename(file_path, is_url=False)
    screenshot_path = generate_file_path("screenshots", base_filename, "png", driver_manager.device_name)
    driver_manager.driver.save_screenshot(screenshot_path)
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
    urls = ["https://example.com"]
    local_htmls = ["./test/index1.html", "./test/index2.html"]
    
    chrome_driver_path = "xx\chromedriver.exe"
    driver_manager = WebDriverManager(executable_path=chrome_driver_path, headless=False)
    driver_manager.start_driver()
    device_type = 'mobile'
    device_type = 'desktop'
    driver_manager.set_device(device_type)

    # 1. url => local_html => rendered_html => screenshot
    local_html_paths = fetch_and_save_html(urls)
    rendered_html_paths = get_rendered_html(local_html_paths, driver_manager=driver_manager, is_url=False)
    screenshots = get_screenshot(rendered_html_paths, driver_manager=driver_manager)

    # 2. url => rendered_html => screenshot
    rendered_html_paths = get_rendered_html(urls, driver_manager=driver_manager, is_url=True)
    screenshots = get_screenshot(rendered_html_paths, driver_manager=driver_manager)

    # 3. local_html => screenshot
    screenshots = get_screenshot(local_htmls, driver_manager=driver_manager)

    # 4. local_html => rendered_html => screenshot
    rendered_html_paths = get_rendered_html(local_htmls, driver_manager=driver_manager, is_url=False)
    screenshots = get_screenshot(rendered_html_paths, driver_manager=driver_manager)
    
    driver_manager.quit_driver()
    
    print("done")
