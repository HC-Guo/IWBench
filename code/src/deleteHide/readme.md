# 清理html中的非可见元素（html预处理）

baseline生成html的统一脚本 todo,步骤：
1. 找到GT的html @GYN
2. clean GThtml：删除注释，替换GT html里的缺失图片资源，删除隐藏元素 (src/deleteHide) @CJH
3. 转GT image并且coco标注  @ZW
4. 标注好的图输入COT进行image2html (3、4合并到了src/i2hBaseline/I2HApi.py) @CJH
6. 删除llm生成的html的隐藏元素 (src/deleteHide) @CJH
5. 比较原始html和生成的html的相似度 (src/compareHtml/html_comparer.py) @CJH


```python
python3 deleteHide/process.py

或者直接调用
def cleanHtml(html_file, clean_html_file):

```
在此之前请先修改process.py中的路径：
```
html_file = './deleteHide/h1.html' # 要清理的html文件
clean_html_file = './deleteHide/h1_clean.html' # 清理后的html文件保存路径
```

和临时文件保存目录, 这里可以不修改，因为会默认运行结束删除tmp文件夹，debug用的
```
# 临时文件保存目录
tmp_dir = './tmp/'
```