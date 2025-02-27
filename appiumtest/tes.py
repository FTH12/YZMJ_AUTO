import re

import easyocr
import cv2
path = 'Screenshot6.png'


# 初始化 EasyOCR
reader = easyocr.Reader(['ch_sim', 'en'], gpu=True)  # 设置语言（中文简体和英文）
# 使用 EasyOCR 识别文字
result = reader.readtext(path)
for detection in result:
    # text = detection[1]
    match = re.search(r"(?<=长度:  )\d+\.\d+(?=厘米)", detection[1])
    if match:
        number = match.group()  # 获取匹配的数字
        print(type(number))

# import json
#
# with open('fishInfo.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)
#     print(data['鲸鲨'])