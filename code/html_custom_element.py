from difflib import SequenceMatcher

# class HtmlCustomElement:
#     def __init__(self, data):
#         self.outerHTML = data.get("outerHTML", "")
#         self.tag = data["tag"]
#         self.textContent = data.get("textContent", "")
#         self.attributes = data.get("attributes", {})
#         self.style = data.get("style", {})
#         self.jsBindings = data.get("jsBindings", {})
#         self.children = " ".join(data.get("children", []))

#     def serialize(self):
#         # Since outerHTML is already provided, simply return it
#         return self.outerHTML


def compare_element(element1, element2):
    scores = [
        compare_tag(element1["tag"], element2["tag"]),
        compare_text_content(element1["textContent"], element2["textContent"]),
        compare_attributes(element1["tag"], element1["attributes"], element2["attributes"]),
        compare_styles(element1["style"], element2["style"]),
        compare_js_bindings(element1["jsBindings"], element2["jsBindings"]),
        compare_children(element1["children"], element2["children"]),
    ]
    return scores

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
    
def compare_tag(tag1, tag2):
    return 1.0 if tag1 == tag2 else 0.0

def compare_text_content(text1, text2):
    return similar(text1, text2)

def compare_attributes(tag, attr1, attr2):
    # 忽略class id这种
    # 需要进行强比较和弱比较的属性, attr 是字典，分别为属性和对应的value
    label = {
        "a": {
            "text_content": "strong_comparison",
            "href": "weak_comparison",
            "target": "weak_comparison",
            "rel": "weak_comparison",
            "download": "weak_comparison",
            "hreflang": "weak_comparison",
            "media": "weak_comparison",
            "type": "weak_comparison"
        },
        "img": {
            "alt": "strong_comparison",
            "src": "weak_comparison",
            "srcset": "weak_comparison",
            "sizes": "weak_comparison"
        },
        "button": {
            "text_content": "strong_comparison",
            "type": "weak_comparison",
            "onclick": "weak_comparison",
            "disabled": "weak_comparison",
            "name": "weak_comparison",
            "value": "weak_comparison"
        },
        "input": {
            "value": "strong_comparison",
            "placeholder": "strong_comparison",
            "required": "strong_comparison",
            "checked": "strong_comparison",
            "readonly": "strong_comparison",
            "type": "weak_comparison",
            "name": "weak_comparison",
            "min": "weak_comparison",
            "max": "weak_comparison",
            "step": "weak_comparison",
            "pattern": "weak_comparison"
        },
        "div": {
            "class": "weak_comparison",
            "id": "weak_comparison",
            "style": "weak_comparison"
        },
        "h1": {
            "text_content": "strong_comparison",
            "class": "weak_comparison",
            "id": "weak_comparison",
            "style": "weak_comparison"
        },
        "p": {
            "text_content": "strong_comparison",
            "class": "weak_comparison",
            "id": "weak_comparison",
            "style": "weak_comparison"
        },
        "ul": {
            "class": "weak_comparison",
            "id": "weak_comparison",
            "style": "weak_comparison"
        },
        "li": {
            "text_content": "strong_comparison",
            "class": "weak_comparison",
            "id": "weak_comparison",
            "style": "weak_comparison"
        },
        "span": {
            "text_content": "strong_comparison",
            "class": "weak_comparison",
            "id": "weak_comparison",
            "style": "weak_comparison"
        },
        "table": {
            "class": "weak_comparison",
            "id": "weak_comparison",
            "style": "weak_comparison"
        },
        "thead": {
            "class": "weak_comparison",
            "id": "weak_comparison",
            "style": "weak_comparison"
        },
        "tbody": {
            "class": "weak_comparison",
            "id": "weak_comparison",
            "style": "weak_comparison"
        },
        "tr": {
            "class": "weak_comparison",
            "id": "weak_comparison",
            "style": "weak_comparison"
        },
        "td": {
            "text_content": "strong_comparison",
            "class": "weak_comparison",
            "id": "weak_comparison",
            "style": "weak_comparison",
            "colspan": "weak_comparison",
            "rowspan": "weak_comparison"
        },
        "th": {
            "text_content": "strong_comparison",
            "class": "weak_comparison",
            "id": "weak_comparison",
            "style": "weak_comparison",
            "colspan": "weak_comparison",
            "rowspan": "weak_comparison",
            "scope": "weak_comparison"
        },
        "label": {
            "text_content": "strong_comparison",
            "for": "strong_comparison",
            "class": "weak_comparison",
            "id": "weak_comparison",
            "style": "weak_comparison"
        },
        "select": {
            "name": "weak_comparison",
            "required": "weak_comparison",
            "multiple": "weak_comparison",
            "class": "weak_comparison",
            "id": "weak_comparison",
            "style": "weak_comparison"
        },
        "option": {
            "text_content": "strong_comparison",
            "value": "strong_comparison",
            "selected": "strong_comparison"
        },
        "textarea": {
            "placeholder": "strong_comparison",
            "required": "strong_comparison",
            "readonly": "strong_comparison",
            "name": "weak_comparison",
            "rows": "weak_comparison",
            "cols": "weak_comparison",
            "class": "weak_comparison",
            "id": "weak_comparison",
            "style": "weak_comparison"
        },
        "footer": {
            "class": "weak_comparison",
            "id": "weak_comparison",
            "style": "weak_comparison"
        },
        "header": {
            "class": "weak_comparison",
            "id": "weak_comparison",
            "style": "weak_comparison"
        },
        "article": {
            "class": "weak_comparison",
            "id": "weak_comparison",
            "style": "weak_comparison"
        },
        "section": {
            "class": "weak_comparison",
            "id": "weak_comparison",
            "style": "weak_comparison"
        },
        "nav": {
            "class": "weak_comparison",
            "id": "weak_comparison",
            "style": "weak_comparison"
        },
        "aside": {
            "class": "weak_comparison",
            "id": "weak_comparison",
            "style": "weak_comparison"
        },
        "figure": {
            "class": "weak_comparison",
            "id": "weak_comparison",
            "style": "weak_comparison"
        },
        "figcaption": {
            "text_content": "strong_comparison",
            "class": "weak_comparison",
            "id": "weak_comparison",
            "style": "weak_comparison"
        },
        "main": {
            "class": "weak_comparison",
            "id": "weak_comparison",
            "style": "weak_comparison"
        },
        "hr": {
            "class": "weak_comparison",
            "id": "weak_comparison",
            "style": "weak_comparison"
        },
        "br": {},
        "link": {
            "href": "weak_comparison",
            "rel": "weak_comparison",
            "media": "weak_comparison",
            "type": "weak_comparison"
        },
        "meta": {
            "content": "strong_comparison",
            "name": "weak_comparison",
            "http-equiv": "weak_comparison",
            "charset": "weak_comparison"
        },
        "script": {
            "src": "weak_comparison",
            "type": "weak_comparison",
            "async": "weak_comparison",
            "defer": "weak_comparison"
        },
        "html": {},
        "head": {},
        "title": {},
        "style": {},
        "body": {},
        "svg": {},
        "path": {},
    }

    compare_label = label.get(tag, {})
    ignoreAttr = ['class', 'id']
    attribute_scores = []
    for k, v in compare_label.items():
        if k in ignoreAttr:
            continue
        if k in attr1.keys() and k in attr2.keys():
            if v == "strong_comparison":
                if attr1[k] != attr2[k]:
                    attribute_scores.append(0.0)
            elif v == "weak_comparison":
                if attr1[k] != attr2[k]:
                    attribute_scores.append(0.5)
        elif k in attr1.keys() or k in attr2.keys():
            # TODO: 一个有值，一个没有，则有值与默认值比较
            attribute_scores.append(0.0)
    return sum(attribute_scores) / len(attribute_scores) if len(attribute_scores) else 1.0
            

def compare_styles(style1, style2):
    # 过滤掉默认值
    default_values = ["none", "0", "normal", "0px",
                        "auto", "rgba(0, 0, 0, 0)", "rgb(0, 0, 0)"]
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
    style1 = {k: v for k, v in style1.items() if k in keep_properties and v not in default_values}
    style2 = {k: v for k, v in style2.items() if k in keep_properties and v not in default_values}
    common_keys = set(style1.keys()) & set(style2.keys())
    total_common_similarity = sum(
        1.0 if style1[k] == style2[k] else 0.0 for k in common_keys)
    total_possible = len(set(style1.keys()) | set(style2.keys()))
    return total_common_similarity / total_possible if total_possible else 1.0

def compare_js_bindings(js_bindings1, js_bindings2, events=['onclick', 'onload', 'onmouseover', 'onmouseout', 'onchange', 'onsubmit']): 
    total_events = 0
    match_events = 0
    for event in events:
        event_js_bindings1 = js_bindings1.get(event)
        event_js_bindings2 = js_bindings2.get(event)
        if event_js_bindings1 is not None:
            total_events += 1
            if event_js_bindings2 is not None:
                match_events += 1.0
            elif event_js_bindings2 is None:
                match_events += 0.0
        else:
            pass
    confidence_score = (match_events / total_events) if total_events != 0 else 1.0
    return confidence_score

def compare_children(children1, children2):
    return similar(children1, children2)


