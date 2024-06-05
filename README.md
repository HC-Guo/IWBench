# IW-Bench: Evaluating Large Multimodal Models for Converting Image-to-Web

----

# ✨Introduction
👋 Welcome, this is a benchmark for evaluating large language models for Converting Images to HTML Code. 😊 We welcome everyone to participate and contribute 🌟. 

# 🛠Environment
We recommend using conda
```
conda create -n iwbench python=3.10
conda activate iwbench
pip install -r requirements.txt

# We use Chrome for HTML to image generation. Please initialize Playwright before use.
# thie will download Chromium version.xxx.xxx.xxx
playwright install
```

# 🚨Dataset
Download the version V1 dataset from [Google Drive(88.1MB)](https://drive.google.com/drive/folders/1zmQHgLvF1591gXSXWponMTBBH_SA-8Pj) and place it in the "./dataset" directory.

# 📈Evaluation
Using your LMM, generate the corresponding HTML code based on the input images. For example, use the PNG files in the 'dataset' directory as input and save the generated results in a folder, in a format like 'code/baseline/dataset-llava-v1.5-13b-html' or 'code/baseline/dataset-websight-html'. The '.html' and '.htmlcoco' files should be generated from the corresponding PNG files in the 'dataset' directory.

```
cd code/
python benchmark.py --input_dir ./baseline/dataset-qwenvlchat-html
```

# 📊Result
Accuracy scores on our IW-bench. Element Accuracy is employed to gauge the comprehensiveness of elements, while Layout Accuracy is utilized to evaluate the effectiveness of webpage layout. These metrics are categorized into three difficulty levels: simple, medium, and complex. Each level is accompanied by corresponding scores and contributes to the final overall average score.
![image](document/result.png)

# 🗓ToDO List
✅ 1. Released version V1 of the dataset with over 317 web pages.

🔘 2. Released version V2 of the dataset, a total of 1000 web pages.



## Licenses

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

This work is licensed under a MIT License.

[![CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](http://creativecommons.org/licenses/by-nc-sa/4.0/)

The dataset is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/).




