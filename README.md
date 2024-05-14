# IW-Bench: Evaluating Large Multimodal Models for Converting Image-to-Web

----

## [🗂Project Page](https://iw-bench-page.vercel.app/) 
<!-- | [![GitHub Repo Stars](https://img.shields.io/github/stars/HC-Guo/Image2HTML-Benchmark?label=stars&logo=github&color=brightgreen)](https://github.com/HC-Guo/Image2HTML-Benchmark) | [![arXiv](https://img.shields.io/badge/arXiv-xxxx-b31b1b.svg?style=flat-square)](https://arxiv.org/abs/xxxx) -->

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
Download the complete dataset from [Google Drive(88.1MB)](https://drive.google.com/drive/folders/1zmQHgLvF1591gXSXWponMTBBH_SA-8Pj) and place it in the "./dataset" directory.

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



# Updates

[12.17] Readme files for HTML_process.py, html_compare.py and Dom_Tree construction are updated [Document](./document)

[12.17] better HTML preprocess script and HTML compare script is updated [code](./code), production of partial datasets is uploaded.[benchmark](https://drive.google.com/drive/folders/18qOha7IqmMUSYo-UvJmnB-9R0bCo7yrI?usp=drive_link)

[12.16] prompts for designing webs are uploaded [prompts](./prompts). 

[12.14] Third meetup on code implement and data collection.[Meetup_3](./Meetup).

[12.11] Code for HTML-DOM tree, Patch comparison, HTML preprocessing is updated [code](./code)

[12.06] GPT4 test cases. [GPT4_case](./Meetup)

[12.03] Second meetup on detailed Todo and GPT4 test.[Meetup_2](./Meetup).

[11.26] Our first meetup on HTML structure and dataset collection.[Meetup_1](./Meetup).



## 📜Citation

Feel free to cite us if you like our work.
```
xxx
```

## Contact



