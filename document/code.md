# html_process.py

## 代码功能：

1. URL => 本地HTML => 渲染后的HTML => 屏幕截图：
   - 首先，通过`fetch_and_save_html`函数从URL获取HTML并保存到本地，返回本地HTML文件的路径列表`local_html_paths`。
   - 接下来，使用`get_rendered_html`函数加载本地HTML文件，将其渲染为HTML，并返回渲染后的HTML文件的路径列表`rendered_html_paths`。
   - 最后，使用`get_screenshot`函数获取渲染后的HTML的屏幕截图，并返回截图列表`screenshots`。
2. URL => 渲染后的HTML => 屏幕截图：
   - 使用`get_rendered_html`函数加载URL，将其渲染为HTML，并返回渲染后的HTML文件的路径列表`rendered_html_paths`。
   - 使用`get_screenshot`函数获取渲染后的HTML的屏幕截图，并返回截图列表`screenshots`。
3. 本地HTML => 屏幕截图：
   - 使用`get_screenshot`函数直接从本地HTML文件路径列表`local_htmls`获取屏幕截图，并返回截图列表`screenshots`。
4. 本地HTML => 渲染后的HTML => 屏幕截图：
   - 使用`get_rendered_html`函数加载本地HTML文件，将其渲染为HTML，并返回渲染后的HTML文件的路径列表`rendered_html_paths`。
   - 使用`get_screenshot`函数获取渲染后的HTML的屏幕截图，并返回截图列表`screenshots`。

## 使用方法：

1. 库依赖：Selenium、requests
2. 环境依赖：Google Chrome浏览器以及对应版本的Chrome WebDriver
3. 数据依赖： 代码中的`urls`列表中添加您要渲染和截图的网址，或将本地HTML文件的路径添加到`local_htmls`列表中。
4. 运行代码，它将执行不同的操作来渲染和截图指定的网址或本地HTML文件。

## 代码中每个函数的功能和实现方法：

- `WebDriverManager`类：
  - 功能：用于管理和控制Selenium WebDriver。可以启动特定的浏览器驱动程序，并提供设置设备类型（移动设备或桌面设备）的功能。
  - 实现方法：该类包含了驱动程序的启动和设备类型的设置方法，使用Selenium提供的相关功能实现。
- `ensure_directory_exists`函数：
  - 功能：确保目录存在的辅助函数。
  - 实现方法：通过检查目标目录是否存在，若不存在则创建该目录。
- `generate_file_path`函数：
  - 功能：根据基本目录、文件名、扩展名和设备类型生成文件路径的辅助函数。
  - 实现方法：根据提供的参数，生成文件路径字符串，其中包括基本目录、文件名、扩展名和设备类型。
- `get_base_filename`函数：
  - 功能：根据URL或文件路径获取基本文件名的辅助函数。
  - 实现方法：使用Python的字符串操作方法从URL或文件路径中提取基本文件名，即不包含目录路径和扩展名的部分。
- `rendering_html`函数：
  - 功能：根据提供的URL或本地HTML文件路径，使用Selenium WebDriver加载页面或HTML文件，并将渲染后的HTML保存到指定位置。
  - 实现方法：该函数使用Selenium库中的WebDriver来加载页面或本地HTML文件，并等待页面完全加载完成。然后，它将获取到的HTML内容保存到指定的文件路径中。
- `get_rendered_html`函数：
  - 功能：接收URL列表或本地HTML文件路径列表，并使用`rendering_html`函数获取每个源的渲染后HTML。
  - 实现方法：该函数循环遍历提供的URL列表或本地HTML文件路径列表，并对每个源调用`rendering_html`函数以获取渲染后的HTML内容。它返回渲染后HTML文件的路径列表。
- `convert_html_to_screenshot`函数：
  - 功能：将提供的HTML文件路径使用Selenium WebDriver转换为屏幕截图，并将截图保存到指定位置。
  - 实现方法：该函数使用Selenium库中的WebDriver来加载HTML文件，并将其转换为屏幕截图。最后，它将截图保存到指定的文件路径中。
- `get_screenshot`函数：
  - 功能：接收渲染后HTML文件路径列表，并使用`convert_html_to_screenshot`函数为每个文件获取屏幕截图。
  - 实现方法：该函数循环遍历提供的渲染后HTML文件路径列表，并对每个文件调用`convert_html_to_screenshot`函数以获取屏幕截图。它返回截图文件的路径列表。
- `fetch_and_save_html`函数：
  - 功能：接收URL列表，并使用Requests库获取每个URL的HTML内容，并将每个HTML保存到指定位置。
  - 实现方法：该函数使用Requests库向给定的URL发出请求，获取每个URL的HTML内容。然后，它将每个HTML内容保存到指定的文件路径中，并返回HTML文件的路径列表。

# html_compare.py

## 代码功能：

输入两份HTML文件，进行以下操作：

1. 序列化HTML标签，数据形式为：`标签、属性和文本内容`，比较命中率
2. 序列化CSS样式，字符串形式逐个比较（尝试）
3. 基于语义的HTML标签归类，类内计算命中率（尝试）
4. 重建可见元素的DOM Tree，在原来的基础上删去不可见元素（ing）

## 使用方法：

1. 库依赖：lxml、difflib
2. 数据依赖： 两份本地HTML文件的路径。
3. 运行代码，它将比较本地HTML文件的差异。

## 代码中每个函数的功能和实现方法：

- `read_html_file(file_path)`:
  - 功能：读取HTML文件的内容并返回。
  - 实现方法：使用Python的内置文件操作函数，打开指定路径的HTML文件，并使用`read`方法读取文件内容，然后将内容作为字符串返回。
- `serialize_html_elements(tree, include_styles=False)`:
  - 功能：将给定树形结构中的HTML元素序列化为字符串列表。可以选择是否包含样式。
  - 实现方法：遍历树形结构中的每个元素，将元素的标签、属性和文本内容序列化为字符串，并添加到一个列表中。如果`include_styles`参数为True，则还会包含样式信息。最后，返回包含所有序列化元素的列表。
- `map_semantic_roles(elements)`:
  - 功能：将序列化的HTML元素映射到语义角色，并返回一个字典，其中键是语义角色，值是属于该角色的元素列表。
  - 实现方法：定义一个包含不同语义角色和对应关键字的字典。遍历序列化的HTML元素列表，根据元素的标签或属性匹配关键字，并将元素添加到对应语义角色的列表中。最后返回包含语义角色和元素列表的字典。
- `build_visible_dom_tree(element, depth=0)`:
  - 功能：根据给定的元素构建可见DOM树的字符串列表。该函数递归地遍历树形结构，将可见元素添加到列表中。
  - 实现方法：递归地遍历给定元素的子元素。对于每个子元素，判断其是否可见（例如，不包含注释节点或空白文本节点），如果可见，则将其标签和属性添加到字符串列表中。然后，对子元素的子元素进行相同的操作。最后返回构建的可见DOM树的字符串列表。
- `serialize_styles(tree)`:
  - 功能：从树形结构中提取样式表，并将其序列化为字符串列表。
  - 实现方法：遍历树形结构中的每个元素，检查是否有样式表信息。如果有样式表，则将其序列化为字符串，并添加到列表中。最后，返回包含序列化样式表的列表。
- `compare_sequences(seq1, seq2)`:
  - 功能：比较两个序列并返回差异列表。
  - 实现方法：使用`difflib`模块中的`Differ`类，将两个序列作为参数传递给`compare`方法，获得一个差异比较结果对象。然后，使用`Differ`对象的`get_opcodes`方法获取差异的操作码，并将其转换为差异列表。
- `compare_and_print_differences(label, seq1, seq2)`:
  - 功能：比较两个序列并打印差异。该函数使用`compare_sequences`函数获取差异列表，并按行打印差异信息，以"+"或"-"开头的行表示差异内容。
  - 实现方法：调用`compare_sequences`函数比较两个序列，并通过遍历差异列表，根据差异类型打印相应的差异信息。使用"+"表示在第二个序列中添加的内容，使用"-"表示在第一个序列中删除的内容。