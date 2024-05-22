from bs4 import BeautifulSoup, Tag
import filecmp
import datetime
import os
import shutil
from playwright.sync_api import sync_playwright
        
def simplify(content="<html>...</html>"):
    tmp_dir = "simplify_tmp/"

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_context().new_page()
        page.set_content(content)
        page.screenshot(path=f'{tmp_dir}original.png',full_page=True)
        page.close()
        browser.close()

    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
        
    removed_elements = []
    soup = BeautifulSoup(content, 'html.parser')
    # with open(url_or_path, 'r') as file:
    #     soup = BeautifulSoup(file, 'html.parser')
    
    elements_to_check = soup.find_all(True)
    clean_soup = str(soup)
    cnt = 0

    for el in elements_to_check:
        cnt += 1
        # print('='*40, el.name, '='*40, f'{cnt} / {len(elements_to_check)}')
        if isinstance(el, Tag) and el.name not in ['html', 'head', 'body', 'title', 'meta']:
            if el is None or el == None:
                continue
            souptmp = clean_soup

            children = el.findChildren()

            el.extract()
            combined_text = ''

            for child in children:
                combined_text += str(child)
       
            souptmp = souptmp.replace(str(el), combined_text)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S%f")

            tmp_html_file = f'{tmp_dir}tmphtml_{timestamp}.html'

            with open(tmp_html_file, 'w') as file:
                file.write(str(souptmp))

            tmp_screenshot = f'{tmp_dir}tmp_image_{timestamp}.png'

            with sync_playwright() as playwright:
                browser = playwright.chromium.launch()
                page = browser.new_context().new_page()
                page.set_content(souptmp)
                page.screenshot(path=tmp_screenshot,full_page=True)
                page.close()
                browser.close()

            if filecmp.cmp(f'{tmp_dir}original.png', f'{tmp_screenshot}', shallow=False):

                clean_soup = souptmp
                # print('-'*20, 'remove:', el.name)
                removed_elements.append(el)

    # with open(output_file, 'w') as file:
    #     file.write(clean_soup)

    shutil.rmtree(tmp_dir)

    # print(f"Removed {len(removed_elements)} elements")
    return clean_soup, removed_elements 

if __name__ == "__main__":
    html_file='unit_test_case/simplifier_examlple.html'
    html_content = open(html_file, 'r').read()
    print(simplify(content=html_content, output_file='simplified.html'))

