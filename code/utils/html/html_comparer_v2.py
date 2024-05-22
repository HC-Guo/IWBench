from lxml import html
import difflib

def read_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def serialize_html_elements(tree, include_styles=False):
    elements = []
    for element in tree.iter():
        if element.tag.lower() in ['script', 'style'] and not include_styles:
            continue
        tag = element.tag
        attributes = dict(element.attrib)
        if 'style' in attributes and not include_styles:
            del attributes['style']
        attributes_str = ' '.join([f'{k}="{v}"' for k, v in attributes.items()])
        text = (element.text or "").strip()
        serialized_element = f"<{tag} {attributes_str}>{text}</{tag}>"
        elements.append(serialized_element)
    return elements

def map_semantic_roles(elements):
    roles = {
        'header': ['header', 'head', 'top', 'branding'],
        'footer': ['footer', 'foot', 'bottom'],
        'navigation': ['nav', 'menu', 'navigation'],
        'main-content': ['main', 'content', 'article', 'body'],
        'sidebar': ['sidebar', 'side', 'aside'],
        'advertisement': ['ad', 'ads', 'advert', 'sponsor']
    }
    
    role_mapping = {role: [] for role in roles}
    
    for element in elements:
        for role, keywords in roles.items():
            if any(keyword in element for keyword in keywords):
                role_mapping[role].append(element)
    return role_mapping

def build_visible_dom_tree(element, depth=0):
    visible_tags = ['div', 'span', 'a', 'ul', 'ol', 'li', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img', 
                    'table', 'thead', 'tbody', 'tfoot', 'tr', 'td', 'th', 'button', 'input', 'textarea', 'select', 'form']
    visible_elements = []
    if element.tag.lower() in visible_tags:
        tag = element.tag.lower()
        attributes = {k: v for k, v in element.attrib.items() if k.lower() not in ['onclick', 'onload', 'onmouseover']}
        attributes_str = ' '.join([f'{k}="{v}"' for k, v in attributes.items()])
        text_content = element.text_content().strip() if element.text_content().strip() else ''
        serialized_element = f"{' ' * depth}< {tag} {attributes_str} >{text_content}"
        visible_elements.append(serialized_element)

    for child in element:
        visible_elements.extend(build_visible_dom_tree(child, depth + 1))

    return visible_elements

def serialize_styles(tree):
    styles = []
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

def compare_and_print_differences(label, seq1, seq2):
    # This function prints the differences between two sequences with a given label
    print(f"\nDifferences in {label}:")
    diff = compare_sequences(seq1, seq2)
    for line in diff:
        if line.startswith('+ ') or line.startswith('- '):
            print(line)

file1 = 'test/index1.html'
file2 = 'test/index2.html'

html_content1 = read_html_file(file1)
html_content2 = read_html_file(file2)

tree1 = html.fromstring(html_content1)
tree2 = html.fromstring(html_content2)

serialized_elements1 = serialize_html_elements(tree1)
serialized_elements2 = serialize_html_elements(tree2)

semantic_map1 = map_semantic_roles(serialized_elements1)
semantic_map2 = map_semantic_roles(serialized_elements2)

visible_dom_tree1 = build_visible_dom_tree(tree1)
visible_dom_tree2 = build_visible_dom_tree(tree2)

serialized_styles1 = serialize_styles(tree1)
serialized_styles2 = serialize_styles(tree2)

compare_and_print_differences("HTML", serialized_elements1, serialized_elements2)
compare_and_print_differences("CSS", serialized_styles1, serialized_styles2)
compare_and_print_differences("Visible DOM Tree", visible_dom_tree1, visible_dom_tree2)



for role in semantic_map1.keys():
    compare_and_print_differences(f"Semantic Mapping for role '{role}'", semantic_map1[role], semantic_map2[role])
