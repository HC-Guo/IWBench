import requests
import base64
import json
import os
from utils.setting import GITHUB_USERNAME, GITHUB_REPO, GITHUB_PATH, GITHUB_TOKEN
import uuid

def read_dir(dir):
    files = os.listdir(dir)
    fdata_tmps = []
    for file in files:
        if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".gif"):
            # ext = os.path.splitext(file)[1]
            with open(dir + "/" + file, 'rb') as f: # rb 二进制 读取
                fdata_tmp = file_base64(f.read())
                f.close()
                fdata_tmps.append((file, fdata_tmp))
    return fdata_tmps

def read_file(file_name):
    with open(file_name, 'rb') as f:
        fdata_tmp = file_base64(f.read())
        f.close()
    file_name_back = file_name.split("/")[-1]
    return (file_name_back, fdata_tmp)

# file need be encoded by base64 before uploading to github
def file_base64(data):
    data_b64 = base64.b64encode(data).decode('utf-8')
    return data_b64

def upload_file_by_file_content(file_content):
    file_name = str(uuid.uuid4()) + ".png"
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/" + GITHUB_PATH + "/" + file_name
    headers = {"Authorization": "token " + GITHUB_TOKEN}
    content = file_content
    data = {
        "message": "upload pictures",
        "content": content
    }
    data = json.dumps(data)
    req = requests.put(url=url, data=data, headers=headers)
    req.encoding = "utf-8"
    re_data = json.loads(req.text)
    # print(re_data)
    result = url.replace("https://api.github.com/repos/", "https://cdn.jsdelivr.net/gh/").replace("contents/", "")
    # print(result)
    return result

def upload_file_by_file_name(file_name):
    file_data = read_file(file_name)
    file_name = file_data[0]
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/" + GITHUB_PATH + "/" + file_name
    headers = {"Authorization": "token " + GITHUB_TOKEN}
    content = file_data[1]
    data = {
        "message": "upload pictures",
        "content": content
    }
    data = json.dumps(data)
    req = requests.put(url=url, data=data, headers=headers)
    req.encoding = "utf-8"
    re_data = json.loads(req.text)
    # print(re_data)
    result = url.replace("https://api.github.com/repos/", "https://cdn.jsdelivr.net/gh/").replace("contents/", "")
    # print(result)
    return result

if __name__ == '__main__':
    file_name = "data/easy_1.html"
    upload_file_by_file_name(file_name)

