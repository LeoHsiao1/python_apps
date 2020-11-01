""" 爬取古风漫画网上的图片 """
import os
import re
import time

import requests


def scrape_page(page_url):
    # 访问漫画页面
    headers = {'Upgrade-Insecure-Requests': '1',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
               'Referer': 'https://m.gufengmh8.com/manhua/xiaoyaoqixia/',
               }
    print('GET', page_url, end=' ... ')
    r = requests.get(page_url, headers=headers)
    if r.status_code == 200:
        print(200)
    else:
        print(r.status_code, r.reason)

    # 解析出图片链接并访问
    next_page_url, image_url = re.findall(
        r'<div class="chapter-content">.{0,200}<div><a href="([^"]*)">\W*<img src="([^"]*)"', r.text, flags=re.S)[0]
    print('GET', image_url, end=' ... ')
    image_html = requests.get(image_url, headers=headers)
    if r.status_code == 200:
        print(200)
    else:
        print(r.status_code, r.reason)

    # 保存图片
    page_index = re.findall(r'\d*-?(\d*).html', page_url)[0] or 0
    image_path = os.path.join(chapter_dir, '{}.jpg'.format(page_index))
    with open(image_path, 'wb') as f:
        f.write(image_html.content)
    print('Saved', image_path)

    if next_page_url.endswith('.html'):
        scrape_page('https://m.gufengmh8.com' + next_page_url)


for chapter_id in range(1329069, 1329291):
    chapter_dir = os.path.join('逍遥奇侠', str(chapter_id))
    os.makedirs(chapter_dir, exist_ok=True)

    chapter_url = 'https://m.gufengmh8.com/manhua/xiaoyaoqixia/{}.html'.format(chapter_id)
    print('\n\n爬取章节：', chapter_id)
    scrape_page(chapter_url)

    time.sleep(3)
    # break



# len(r.text)
# r.status_code

# with open('1.html', 'w', encoding='utf-8') as f:
#     f.write(r.text)

