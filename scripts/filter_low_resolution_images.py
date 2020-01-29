# -*- coding: utf-8 -*-
import os
import shutil
import traceback

from PIL import Image

from utils import Inputs, find_file


print("""该脚本的用途：找出目标目录（包括子目录）下的所有图片（后缀名为jpg、png），筛选出分辨率过低的图片，将它们拷贝到当前目录下，以便被PS修改。""")
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
        # 检查图片的高度是否大于1080
        img = Image.open(path)
        if img.size[1] >= 1080:
            continue

        # 创建保存图片的子目录
        result_path = path.replace(Inputs.path, result_dir, 1)
        os.makedirs(os.path.dirname(result_path), exist_ok=True)

        # 保存图片
        shutil.copy(path, result_path)
        print('已保存：{}'.format(result_path))

    except:
        print('处理失败：{}'.format(path))
        traceback.print_exc()

print('\n全部完成。\n')
