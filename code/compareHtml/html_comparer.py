from difflib import SequenceMatcher
import difflib
from collections import Counter
from lxml import html, etree
import numpy as np
from ComputedStyle import getComputedStyle
from ComputedProperties import getTagAttributes

# TODO: 1. 从 HTML 中提取出可见（去除不可见元素）的 DOM 树
# TODO: 2. 从 DOM 树中提取出语义簇，如 header, footer, navigation, main-content, sidebar, advertisement
# TODO: 3. 从 DOM 树中提取出 CSS 信息，在现有的基础上完善代码
# TODO: 4. 实现JS可能被绑定的评价指标，如 onclick, onload, onmouseover，类比HTML-Element的比较给出定性指标
# TODO: 5. 优化HTML-Element-Attribute的比较逻辑，比如IMG标签，URL属性判断是否存在，alt则需要文本相似度，width、height不需要比较

computed_styles1 = {}
computed_styles2 = {}

computed_Attributes1 = {}
computed_Attributes2 = {}

class CustomTreeElement:
    # def __init__(self, tag, text, attributes):
    #     self.tag = tag
    #     self.text = text
    #     self.attributes = attributes
    #     self.children = []
    #     self.children_summary = self.summarize_children()

    def __init__(self, element, include_styles=False):
        self.element = element
        self.tag = element.tag
        self.text = (element.text or "").strip()
        self.attributes = self.filter_attributes(element.attrib, include_styles)
        self.children = [CustomTreeElement(child, include_styles) for child in element]
        self.children_summary = self.summarize_children()

    @staticmethod
    def filter_attributes(attributes, include_styles):
        filtered_attributes = dict(attributes)
        # if "style" in filtered_attributes and not include_styles:
        #     del filtered_attributes["style"]
        return filtered_attributes

    def summarize_children(self):
        return Counter(child.tag for child in self.children)

    def serialize(self):
        attributes_str = " ".join(
            [f'{k}="{v}"' for k, v in sorted(self.attributes.items())]
        )
        serialized_element = f"<{self.tag} {attributes_str}>{self.text}</{self.tag}>"
        return serialized_element

    @staticmethod
    def compare_tags(tag1, tag2):
        """比较两个标签名"""
        return 1.0 if tag1 == tag2 else 0.0

    @staticmethod
    def compare_text_content(text1, text2):
        """比较两个元素的文本内容"""
        # 使用一种文本相似度算法，如Levenshtein距离
        # if text1 == '' and text2 == '':
        #     return 0.0
        return CustomTreeElement.similar(text1, text2)

    @staticmethod
    def compare_styles(element1, element2 ):
        """比较两个元素的属性，使用计算样式"""
        element_string = etree.tostring(element1.element, pretty_print=True, method="html").decode()
        element_string = element_string.replace('\n', '').replace('\t', '').replace('&nbsp;', '').replace('&#160;', '').replace('"','').replace('\"','').replace(' ','').replace('<tbody>', '').replace('</tbody>', '')
        
        element_string2 = etree.tostring(element2.element, pretty_print=True, method="html").decode()
        element_string2 = element_string2.replace('\n', '').replace('\t', '').replace('&nbsp;', '').replace('&#160;', '').replace('"','').replace('\"','').replace(' ','').replace('<tbody>', '').replace('</tbody>', '')
        
        style1 = computed_styles1.get(element_string, {})
        style2 = computed_styles2.get(element_string2, {})

        """比较两个样式字典"""
        # 过滤掉默认值
        default_values = ["none", "0", "normal", "0px", "auto", "rgba(0, 0, 0, 0)", "rgb(0, 0, 0)"]
        style1 = {k: v for k, v in style1.items() if v not in default_values}
        style2 = {k: v for k, v in style2.items() if v not in default_values}

        keep_properties = [
            "color", "display", "font-family", "font-size", "height", "line-height", "margin-top", "text-align", "width",
            "background-color", "border-bottom-color", "border-bottom-left-radius", "border-bottom-right-radius",
            "border-bottom-style", "border-bottom-width", "border-image-outset", "border-image-repeat", "border-image-slice",
            "border-image-source", "border-image-width", "border-left-color", "border-left-style", "border-left-width",
            "border-right-color", "border-right-style", "border-right-width", "border-top-color", "border-top-left-radius",
            "border-top-right-radius", "border-top-style", "border-top-width", "box-shadow", "z-index",
            "margin-bottom", "margin-left", "margin-right", "padding-bottom", "padding-left", "padding-right", "padding-top",
            "position", "font-weight", "overflow-x", "overflow-y", "outline-color", "outline-style", "outline-width",
            "text-indent", "vertical-align", "background-attachment", "background-clip", "background-image", "background-origin",
            "background-position-x", "background-position-y", "background-repeat", "background-size", "border-style", 
            "border-width", "box-sizing", "cursor", "font-feature-settings", "font-kerning", "font-optical-sizing", 
            "font-variant-alternates", "font-variant-caps", "font-variant-east-asian", "font-variant-ligatures", 
            "font-variant-numeric", "font-variant-position", "font-variation-settings", "letter-spacing", "opacity", 
            "text-decoration", "text-decoration-color", "text-decoration-style", "text-emphasis-color", "text-emphasis-position",
            "text-overflow", "text-rendering", "text-shadow", "text-transform", "white-space-collapse", "word-spacing",
            "writing-mode", "align-items", "appearance", "background", "border", "flex-direction", "flex-shrink",
            "flex-wrap", "grid-auto-flow", "justify-content", "object-fit", "object-position", "overflow", "padding",
            "text-emphasis", "transform", "transition", "animation", "visibility", "white-space", "-webkit-font-smoothing",
            "-webkit-rtl-ordering", "-webkit-tap-highlight-color"
        ]

        style1 = {k: v for k, v in style1.items() if k in keep_properties}
        style2 = {k: v for k, v in style2.items() if k in keep_properties}

        all_keys = set(style1.keys()) | set(style2.keys())
        common_keys = set(style1.keys()) & set(style2.keys()) # 比较公有key

        # total_common_similarity = sum(1.0 if style1[k] == style2[k] else 0.0 for k in common_keys)
        total_common_similarity = sum(1.0 if style1[k] == style2[k] else 0.0 for k in common_keys) # k v都相同才算
        total_possible = len(all_keys)
        return total_common_similarity / total_possible if total_possible else 0 #total_possible是零的话说明又一个element是注释 

    @staticmethod
    def compare_attributes(tagname1, tagname2, attr1, attr2 ):
        # 忽略class id这种
        # 需要进行强比较和弱比较的属性, attr 是字典，分别为属性和对应的value
        lable = {
                "a": {
                "strong_comparison": ["text_content"],
                "weak_comparison": ["href", "target", "rel", "download", "hreflang", "media", "type"]
                },
                "img": {
                "strong_comparison": ["alt"],
                "weak_comparison": ["src", "srcset", "sizes"]
                },
                "button": {
                "strong_comparison": ["text_content"],
                "weak_comparison": ["type", "onclick", "disabled", "name", "value"]
                },
                "input": {
                "strong_comparison": ["value", "placeholder", "required", "checked", "readonly"],
                "weak_comparison": ["type",  "name", "min", "max", "step", "pattern"]
                },
                "div": {
                "strong_comparison": [],
                "weak_comparison": ["class", "id", "style"]
                },
                "h1": {
                "strong_comparison": ["text_content"],
                "weak_comparison": ["class", "id", "style"]
                },
                "p": {
                "strong_comparison": ["text_content"],
                "weak_comparison": ["class", "id", "style"]
                },
                "ul": {
                "strong_comparison": [],
                "weak_comparison": ["class", "id", "style"]
                },
                "li": {
                "strong_comparison": ["text_content"],
                "weak_comparison": ["class", "id", "style"]
                },
                "span": {
                "strong_comparison": ["text_content"],
                "weak_comparison": ["class", "id", "style"]
                },
                "table": {
                "strong_comparison": [],
                "weak_comparison": ["class", "id", "style"]
                },
                "thead": {
                "strong_comparison": [],
                "weak_comparison": ["class", "id", "style"]
                },
                "tbody": {
                "strong_comparison": [],
                "weak_comparison": ["class", "id", "style"]
                },
                "tr": {
                "strong_comparison": [],
                "weak_comparison": ["class", "id", "style"]
                },
                "td": {
                "strong_comparison": ["text_content"],
                "weak_comparison": ["class", "id", "style", "colspan", "rowspan"]
                },
                "th": {
                "strong_comparison": ["text_content"],
                "weak_comparison": ["class", "id", "style", "colspan", "rowspan", "scope"]
                },
                "label": {
                "strong_comparison": ["text_content", "for"],
                "weak_comparison": ["class", "id", "style"]
                },
                "select": {
                "strong_comparison": [],
                "weak_comparison": ["name", "required", "multiple", "class", "id", "style"]
                },
                "option": {
                "strong_comparison": ["text_content", "value", "selected"],
                "weak_comparison": []
                },
                "textarea": {
                "strong_comparison": ["placeholder", "required", "readonly"],
                "weak_comparison": ["name", "rows", "cols", "class", "id", "style"]
                },
                "footer": {
                "strong_comparison": [],
                "weak_comparison": ["class", "id", "style"]
                },
                "header": {
                "strong_comparison": [],
                "weak_comparison": ["class", "id", "style"]
                },
                "article": {
                "strong_comparison": [],
                "weak_comparison": ["class", "id", "style"]
                },
                "section": {
                "strong_comparison": [],
                "weak_comparison": ["class", "id", "style"]
                },
                "nav": {
                "strong_comparison": [],
                "weak_comparison": ["class", "id", "style"]
                },
                "aside": {
                "strong_comparison": [],
                "weak_comparison": ["class", "id", "style"]
                },
                "figure": {
                "strong_comparison": [],
                "weak_comparison": ["class", "id", "style"]
                },
                "figcaption": {
                "strong_comparison": ["text_content"],
                "weak_comparison": ["class", "id", "style"]
                },
                "main": {
                "strong_comparison": [],
                "weak_comparison": ["class", "id", "style"]
                },
                "hr": {
                "strong_comparison": [],
                "weak_comparison": ["class", "id", "style"]
                },
                "br": {
                "strong_comparison": [],
                "weak_comparison": []
                },
                "link": {
                "strong_comparison": [],
                "weak_comparison": ["href", "rel", "media", "type"]
                },
                "meta": {
                "strong_comparison": ["content"],
                "weak_comparison": ["name", "http-equiv", "charset"]
                },
                "script": {
                "strong_comparison": [],
                "weak_comparison": ["src", "type", "async", "defer"]
                },
        }
        
        total_attr2_key = len(attr2.keys())
        tagattr = lable.get(tagname2, {})
        if tagattr == {}: # 不在需要比较的标签里
            return 0
        
        # 不需要比较的属性 class 和id
        ignoreAttr = ['class', 'id']
        # attr2  是GT
        sorce = 0.0
        for k, v in attr2.items():
            # 强比较是必须kv完全一致的，弱比较是必须要有k的
            if k in ignoreAttr:
                total_attr2_key -= 1
                continue
            if k in tagattr["strong_comparison"]:
                sorce += 1.0 if attr1.get(k, "") == v else 0.0
            if k in tagattr["weak_comparison"]:
                sorce += 1.0 if k in attr1.keys() else 0.0
        return sorce / total_attr2_key if total_attr2_key != 0 else 0.0
    
    @staticmethod
    def simple_similarity(value1, value2):
        """简单的属性值比较"""
        return 1.0 if value1 == value2 else 0.0
    
    @staticmethod
    def compare_children(children1, children2):
        """递归比较两个元素的子元素"""
        if len(children1) != len(children2):
            return 0.0
        if not children1:  # 如果没有子元素
            return 1.0
        return sum(CustomTreeElement.compare(child1, child2) for child1, child2 in zip(children1, children2)) / len(children1)

    @staticmethod
    def compare_onclick(element1, element2):
        onclick1 = element1.attributes.get('onclick', None)
        onclick2 = element2.attributes.get('onclick', None)

        # 如果两个元素都没有onclick属性，返回1.0
        if onclick1 is None and onclick2 is None:
            return 1.0
        # 如果两个元素的onclick属性相同，返回1.0
        elif onclick1 == onclick2:
            return 1.0
        # 否则，返回0.0
        else:
            return 0.0
    
    @staticmethod
    def compare(element1, element2):
        scores = [
            CustomTreeElement.compare_tags(element1.tag, element2.tag),
            CustomTreeElement.compare_text_content(element1.text, element2.text),
            CustomTreeElement.compare_attributes(element1.tag, element2.tag, element1.attributes, element2.attributes),
            CustomTreeElement.compare_styles(element1, element2),
            CustomTreeElement.compare_onclick(element1, element2),
            CustomTreeElement.compare_children(element1.children, element2.children)
        ]
        weight = [
            2, # tag name
            3, # text content
            2, # attributes
            1, # styles
            1, # onclick
            2, # children
        ]
        sw = [a * b for a, b in zip(scores, weight)]
        # print(f'scores={scores}')
        return sum(sw) / sum(weight)

    
    @staticmethod
    def similar(a, b):
        # TODO: a=>gt
        # len(lcs(a,b)) * 2 / (len(a) + len(b))
        return SequenceMatcher(None, a, b).ratio()

class TreeSerializer:
    def __init__(self):
        self.include_styles = False

    def serialize_tree(self, tree):
        elements = []
        for element in tree.iter():
            elements.append(self.serialize_element(element))
        return elements
    
    def serialize_tree_styles(self, tree):
        styles = []
        for element in tree.xpath('//link[@rel="stylesheet"] | //style'):
            if element.tag == "link":
                href = element.get("href", "")
                styles.append(f'<link rel="stylesheet" href="{href}">')
            elif element.tag == "style":
                text = element.text.strip() if element.text else ""
                styles.append(f"<style>{text}</style>")
        return styles

    def serialize_element(self, element):
        return CustomTreeElement(element, self.include_styles)

    def serialize(self, tree, include_styles=False):
        self.include_styles = include_styles
        elements = self.serialize_tree(tree)
        styles = []
        if self.include_styles:
            styles = self.serialize_tree_styles(tree)
        return elements, styles


class VisibleDomTree:
    def __init__(self, tree):
        self.tree = tree

    def build_visible_dom_tree(self, element, depth=0):
        visible_tags = ["div", "span", "a", "ul", "ol", "li", "p", "h1", "h2", "h3", "h4", "h5", "h6", "img",
                        "table", "thead", "tbody", "tfoot", "tr", "td", "th", "button", "input", "textarea", "select", "form",]
        visible_elements = []
        if element.tag.lower() in visible_tags:
            tag = element.tag.lower()
            attributes = {
                k: v
                for k, v in element.attrib.items()
                if k.lower() not in ["onclick", "onload", "onmouseover"]
            }
            attributes_str = " ".join(
                [f'{k}="{v}"' for k, v in attributes.items()])
            text_content = (
                element.text_content().strip() if element.text_content().strip() else ""
            )
            serialized_element = (
                f"{' ' * depth}< {tag} {attributes_str} >{text_content}"
            )
            visible_elements.append(serialized_element)
        for child in element:
            visible_elements.extend(
                self.build_visible_dom_tree(child, depth + 1))
        return visible_elements

    def build(self):
        return self.build_visible_dom_tree(self.tree)


class HTMLComparer:
    def __init__(self):
        self.tree_serialize = TreeSerializer()

    def get_tree(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return html.fromstring(file.read())

    def compare(self, file1, file2):
        print(f"Comparing {file1} and {file2}...")
        tree1 = self.get_tree(file1)
        tree2 = self.get_tree(file2)
        elements1, styles1 = self.tree_serialize.serialize(
            tree1, include_styles=False)
        elements2, styles2 = self.tree_serialize.serialize(
            tree2, include_styles=False)
        
        self.compare_differences("HTML", elements1, elements2)

        self.compare_differences("CSS", styles1, styles2)

        return 1.0, 1.0

    def longest_common_subsequence(self, seq1, seq2, similarity_threshold=0.9):
        m, n = len(seq1), len(seq2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if CustomTreeElement.compare(seq1[i - 1], seq2[j - 1]) > similarity_threshold:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        lcs = []
        i, j = m, n
        while i > 0 and j > 0:
            compute_score = CustomTreeElement.compare(seq1[i - 1], seq2[j - 1])
            if compute_score  > similarity_threshold:
                lcs.append((seq1[i - 1], seq2[j - 1],compute_score))
                i -= 1
                j -= 1
            elif dp[i - 1][j] > dp[i][j - 1]:
                i -= 1
            else:
                j -= 1
        lcs.reverse()
        return lcs
    
    def calculate_common_elements(self, seq1, seq2, similarity_threshold=0.9):
        common_elements = []
        used_indices_seq2 = set()

        for idx1, elem1 in enumerate(seq1):
            for idx2, elem2 in enumerate(seq2):
                if idx2 in used_indices_seq2:
                    continue
                if CustomTreeElement.compare(elem1, elem2) > similarity_threshold:
                    common_elements.append((elem1, elem2, idx1, idx2))
                    used_indices_seq2.add(idx2)
                    break
        return common_elements

    def compare_sequences(self, seq1, seq2):
        diff = difflib.ndiff(seq1, seq2)
        return diff

    def compare_differences(self, label, seq1, seq2):
        # label: HTML, CSS, Visible DOM Tree, Semantic Mapping for role 'header', etc.
        print(f"Differences in {label}:")
        if label == "HTML":
            lcs = self.longest_common_subsequence(seq1, seq2, 0.7)
            print(f"序列1: {[i.tag for i in seq1]}, 长度: {len(seq1)}")
            print(f"序列2: {[i.tag for i in seq2]}, 长度: {len(seq2)}")
            print(f"最长公共子序列: {[(i[0].serialize(), i[1].serialize(), i[2]) for i in lcs]}, 长度: {len(lcs)}")
            print(f"LCS/序列1: {len(lcs)/len(seq1)}, LCS/序列2: {len(lcs)/len(seq2)}")
            common_elements = self.calculate_common_elements(seq1, seq2, 0.7)
            print(f"公共元素: {[(i[0].serialize(), i[1].serialize(), i[2], i[3]) for i in common_elements]}, 长度: {len(common_elements)}")
            print(f"公共元素/序列1: {len(common_elements)/len(seq1)}, 公共元素/序列2: {len(common_elements)/len(seq2)}")
            # seq1 为 groud truth
            # seq2 为 inference result
            result = (len(lcs)/len(seq1), len(common_elements)/len(seq1))
        elif label == "CSS":
            diff = self.compare_sequences(seq1, seq2)
            for line in diff:
                if line.startswith("+ ") or line.startswith("- "):
                    print(line)


def map_semantic_roles(elements):
    roles = {
        # ? 同义词如何获取？如何自动化？
        # ？ 一份文件有多个同义词，如何处理？
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

def main():
    
    global computed_styles1, computed_styles2
    file_pairs = [
        ["/Users/yisuanwang/Desktop/image2html/src/ignoreAttr/data/case3/email.html", 
        "/Users/yisuanwang/Desktop/image2html/src/ignoreAttr/data/case3/modified_simple_email_template.html"],
        # ["/Users/yisuanwang/Desktop/image2html/src/ignoreAttr/data/case3/email.html", "/Users/yisuanwang/Desktop/image2html/src/ignoreAttr/data/case3/simple_email_template.html"],
    ]
    htmlComparer = HTMLComparer()
    for pair in file_pairs:
        # getComputedStyle 直接返回json
        computed_styles1 = getComputedStyle(local_html_file_path='file:///'+pair[0], output_path='./style1.json')
        computed_styles2 = getComputedStyle(local_html_file_path='file:///'+pair[1], output_path='./style2.json')

        # computed_properties1 = getTagProperties(local_html_file_path='file:///'+pair[0], output_path='./prompt1.json')
        # computed_properties2 = getTagProperties(local_html_file_path='file:///'+pair[1], output_path='./prompt2.json')

        htmlComparer.compare(pair[0], pair[1])

if __name__ == "__main__":
    main()

