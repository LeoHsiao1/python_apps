# -*- coding: utf-8 -*-
import os
import shutil
import traceback

from PIL import Image

from utils import Inputs, find_file


print("""该脚本的用途：找出目标目录（包括子目录）下的所有图片（后缀名为jpg、png），筛选出符合条件的图片，将它们拷贝到当前目录下。""")
Inputs.path = Inputs.input_path('请输入目标目录：')

print('检索所有文件...')
file_list = find_file(Inputs.path)

# 创建一个保存结果的文件夹
result_dir = os.path.join(os.getcwd(), 'results')
os.makedirs(result_dir, exist_ok=True)

print('开始处理...')
for path in file_list:
    suffix = path[path.rfind('.'):].lower()
    if suffix not in ['.jpg', '.png']:
        continue
    
    try:
        img = Image.open(path)

        img_selected = False   # 一个标志位，代表是否筛选出该图片

        # 筛选出高度小于1080的图片
        if img.size[1] < 1080:
            img_selected = True
        
        # # 筛选出文件大小超过10M的图片
        # _10MB = 15*1024*1024
        # if os.path.getsize(path) > _10MB:
        #     img_selected = True

        if img_selected:
            result_path = path.replace(Inputs.path, result_dir, 1)  # 生成保存图片的路径
            os.makedirs(os.path.dirname(result_path), exist_ok=True)  # 创建保存图片的子目录
            shutil.copy(path, result_path)  # 保存图片
            print('已保存：{}'.format(result_path))
        
    except:
        print('处理失败：{}'.format(path))
        traceback.print_exc()

print('\n全部完成。\n')
