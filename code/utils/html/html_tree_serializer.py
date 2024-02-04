import json
import os
from playwright.sync_api import sync_playwright

def serialize(content="<html>...</html>"):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_context().new_page()
        page.set_content(content)
        elements = page.query_selector_all("html, html *")
        
        serialized_elements = []
        for element in elements:
            data = element.evaluate("""(element) => {
                const computedStyle = getComputedStyle(element);
                const style = Object.entries(computedStyle).reduce((acc, [key, value]) => {
                    acc[key] = value;
                    return acc;
                }, {});

                const attributes = Array.from(element.attributes).reduce((acc, attr) => {
                    acc[attr.name] = attr.value;
                    return acc;
                }, {});

                const events = ['onclick', 'onload', 'onmouseover', 'onmouseout', 'onchange', 'onsubmit'];
                const jsBindings = events.reduce((acc, event) => {
                    if (element[event] !== null) {
                        acc[event] = element[event].toString();
                    }
                    return acc;
                }, {});

                const textContent = Array.from(element.childNodes)
                                .filter(node => node.nodeType === Node.TEXT_NODE)
                                .map(node => node.textContent.trim())
                                .join(' ');
                const tag = element.tagName.toLowerCase();
                const outerHTML = element.outerHTML;
                const children = Array.from(element.children).map(child => child.tagName.toLowerCase());

                return { tag, outerHTML, style, attributes, jsBindings, textContent, children };
            }""")

            serialized_elements.append(data)
        page.close()
        browser.close()
    return serialized_elements

if __name__ == "__main__":
    url_or_path = "/Users/knediny/html_code/code_/unit_test_case/serialized_example.html"
    content = open(url_or_path, 'r').read()
    serialized_elements = serialize(content=content)
    print(json.dumps(serialized_elements, indent=4))

