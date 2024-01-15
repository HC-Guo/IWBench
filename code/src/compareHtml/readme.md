# GPT4 ,few-shot compare html
使用GPT4评测，few-shot方式,返回相似度
```python
python3 gpt4_comp_baseline/comp.py
```

# ours 测评方式，根目录的html_comparer.py
LCS比较最大相似元素@zhangwei
```python
def comp_html(file1, file2)
这里直接返回两html的相似度
```