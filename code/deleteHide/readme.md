# 清理html中的非可见元素

```python
python3 deleteHide/process.py
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