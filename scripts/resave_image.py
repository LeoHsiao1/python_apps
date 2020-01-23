# -*- coding: utf-8 -*-
"""
检索指定目录（包括子目录）下的所有图片，将它们保存到当前目录下，从而刷新它们的哈希值。
并且，将png、jpeg后缀名的图片都转换成jpg后缀名，方便统一管理。
"""

import os
import traceback

from PIL import Image

from utils import Inputs, find_file


print("""该脚本用于检索指定目录（包括子目录）下的所有图片（后缀名为jpg、jpeg、png），将它们另存到当前目录下（后缀名改为jpg）。""")

Inputs.path = Inputs.input_path('请输入要检索的目录：')

print('检索所有文件...')
file_list = find_file(Inputs.path)

# 创建一个保存结果的文件夹
result_dir = os.path.join(os.getcwd(), 'results')
os.makedirs(result_dir, exist_ok=True)

print('开始修改...')
for path in file_list:
    original_suffix = path[path.rfind('.'):].lower()
    if original_suffix == '.jpg':
        new_suffix = '.jpg'
    elif original_suffix in ['.jpeg', '.png']:
        new_suffix = original_suffix + '.jpg'
    else:
        continue

    try:
        img = Image.open(path)

        # 可能有些图片只是后缀名为jpg，实际上却不是RGB模式，这里把它们都转换成RGB模式
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # 创建保存图片的子目录
        result_path = path.replace(Inputs.path, result_dir, 1)
        result_path = result_path[:result_path.rfind('.')] + new_suffix
        os.makedirs(os.path.dirname(result_path), exist_ok=True)

        # 保存图片
        img.save(result_path, quality=100)
        print('已保存：{}'.format(result_path))

    except:
        print('处理失败：{}'.format(path))
        traceback.print_exc()

print('\n全部完成。\n')
