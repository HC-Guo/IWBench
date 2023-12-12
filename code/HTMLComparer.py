from lxml import html
import difflib

def read_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def serialize_html_elements(tree):
    elements = []
    
    for element in tree.iter():
        # 忽略 <style> 和外部 CSS 的 <link>
        if element.tag == 'style' or (element.tag == 'link' and element.get('rel', '') == 'stylesheet'):
            continue
            
        tag = element.tag
        attributes = dict(element.attrib)  # 使用 dict() 来复制属性
        # 如果有 style 属性，移除它以保持 HTML 和 CSS 分离
        attributes.pop('style', None)
        attributes_str = ' '.join([f'{k}="{v}"' for k, v in attributes.items()])
        text = (element.text or "").strip()

        # 序列化非 CSS 元素
        serialized_element = f"<{tag} {attributes_str}>{text}</{tag}>"
        elements.append(serialized_element)
    
    return elements

def serialize_styles(tree):
    styles = []

    # 提取所有 `<link rel="stylesheet">` 和 `<style>` 标签
    for element in tree.xpath('//link[@rel="stylesheet"] | //style'):
        if element.tag == 'link':
            href = element.get('href', '')
            styles.append(f'<link rel="stylesheet" href="{href}">')
        elif element.tag == 'style':
            text = element.text.strip() if element.text else ""
            styles.append(f'<style>{text}</style>')

    return styles

def compare_sequences(seq1, seq2):
    d = difflib.Differ()
    diff = list(d.compare(seq1, seq2))
    return diff


file1 = 'index1.html'
file2 = 'index2.html'

html_content1 = read_html_file(file1)
html_content2 = read_html_file(file2)

tree1 = html.fromstring(html_content1)
tree2 = html.fromstring(html_content2)

serialized_elements1 = serialize_html_elements(tree1)
serialized_elements2 = serialize_html_elements(tree2)
serialized_styles1 = serialize_styles(tree1)
serialized_styles2 = serialize_styles(tree2)

html_diffs = compare_sequences(serialized_elements1, serialized_elements2)
css_diffs = compare_sequences(serialized_styles1, serialized_styles2)


print("Differences in HTML:")
for diff in html_diffs:
    print(diff)

print("\nDifferences in CSS:")
for diff in css_diffs:
    print(diff)

# print(f"Length of the first HTML document sequence: {len(serialized_elements1)}")
# print(f"Length of the second HTML document sequence: {len(serialized_elements2)}")
# print("Differences between two sequences:")
# for diff in diffs:
#     print(diff)