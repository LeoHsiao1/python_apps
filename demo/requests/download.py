import re

import requests


url = "https:" + "//www.baidu.com"
r = requests.get(url, timeout=1)
if r.status_code != 200:
    raise RuntimeError
r.encoding = "utf-8"
html = r.text

# 从html中筛选png图片的链接
# （html中的目标数据为 src=//www.baidu.com/img/bd_logo1.png）
result = re.findall(r"src=(.*\.png)", html)
print("found: " + result)

# 合成图片的有效链接，下载到本地
for i in result:
    url = "https:" + i
    filename = i.split('/')[-1]
    r = requests.get(url, timeout=1)
    r.raise_for_status()
    with open(filename, 'wb') as f:
        f.write(r.content)
