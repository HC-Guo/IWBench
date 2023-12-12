import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

class WebDriverManager:
    def __init__(self, headless=True, driver_path='./chromedriver-win64/chromedriver.exe'):
        self.driver_path = driver_path
        self.headless = headless
        self.driver = None
    
    def __enter__(self):
        # 设置Chrome选项（无头模式）
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        options.add_argument("--start-maximized")
        
        # 初始化webdriver，并指定ChromeDriver的路径
        service = Service(executable_path=self.driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        return self.driver
    
    def __exit__(self, exc_type, exc_value, traceback):
        # 关闭浏览器
        if self.driver is not None:
            self.driver.quit()

def get_rendered_html(source, is_url=True, driver_manager=None):
    with driver_manager as driver:
        # 加载页面
        if is_url:
            driver.get(source)
        else:
            with open(source, 'r', encoding='utf-8') as f:
                html_content = f.read()
                driver.get("data:text/html;charset=utf-8,{html_content}".format(html_content=html_content))

        # 等待JavaScript加载完成
        time.sleep(3)  # 根据实际情况，可能需要调整等待时间

        # 获取渲染后的HTML
        rendered_html = driver.page_source
        
        # 存储到文件
        output_path = 'rendered_page.html'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rendered_html)

    return output_path

def get_screenshot(file_path, output_file="screenshot.png", driver_manager=None):
    with driver_manager as driver:
        # 调整窗口大小以适应内容长度
        driver.set_window_size(1920, 1080)
        
        # 加载本地HTML文件
        html_path = os.path.join(os.getcwd(), file_path)
        driver.get(html_path)

        # 滚动到底部以确保所有懒加载元素都被加载
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # 等待滚动加载完成
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # 截长图
        total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
        driver.set_window_size(1920, total_height)  # 临时改变窗口尺寸以适应全身高度
        driver.save_screenshot(output_file)

    return output_file


# Example usage:

driver_path = './chromedriver-win64/chromedriver.exe'  # 替换为你的chromedriver路径
driver_manager = WebDriverManager(driver_path=driver_path)

# url = 'http://example.com'  # 替换为你想要访问的URL
url = 'https://chromewebstore.google.com/?hl=en_us'  # 替换为你想要访问的URL
rendered_html_path = get_rendered_html(url, is_url=True, driver_manager=driver_manager)
screenshot_file = get_screenshot(rendered_html_path, driver_manager=driver_manager)

print(f"Screenshot saved as {screenshot_file}")
