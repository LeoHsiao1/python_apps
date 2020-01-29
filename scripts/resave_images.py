# -*- coding: utf-8 -*-
import os
import shutil
import traceback

from PIL import Image
import pyexiv2

from utils import Inputs, find_file


print("""该脚本的用途：找出目标目录（包括子目录）下的所有图片，另存到当前目录下。
- 新图片的后缀名统一为jpg
- 新图片会拷贝原图片的标签
- 原图片尺寸过小时会自动放大，使高度至少为1080""")

Inputs.path = Inputs.input_path('请输入目标目录：')

print('检索所有文件...')
file_list = find_file(Inputs.path)

# 创建一个保存结果的文件夹
result_dir = os.path.join(os.getcwd(), 'results')
os.makedirs(result_dir, exist_ok=True)

print('开始处理...')
for path in file_list:
    suffix = path[path.rfind('.'):].lower()
    # 只处理这些后缀名的图片文件
    if suffix not in ['.jpg', '.jpeg', '.png']:
        continue
    new_suffix = '.jpg'

    try:
        img = Image.open(path)

        # 生成新图片的保存路径
        result_path = path.replace(Inputs.path, result_dir, 1)
        result_path = result_path[:result_path.rfind('.')] + new_suffix
        os.makedirs(os.path.dirname(result_path), exist_ok=True)  # 创建相应的目录
        # 如果目标文件已存在，则在文件名末尾再添加一个.jpg（此后需要手动改名）
        while 1:
            if os.path.isfile(result_path):
                result_path += '.jpg'
            else:
                break

        # 如果原图片已满足条件，则不修改，直接拷贝
        if suffix == '.jpg' and img.mode == 'RGB' and img.size[1] >= 1080:
            shutil.copy(path, result_path)

        # 此时需要通过pillow保存新图片
        else:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 如果原图片的高度小于1080，则放大至1080
            if img.size[1] < 1080:
                width, height = img.size
                times = 1080 / height
                new_size = round(width * times), round(height * times)
                img = img.resize(new_size)

            # 保存新图片
            img.save(result_path, quality=95)

            # 拷贝原图片的标签
            metadata = pyexiv2.Image(path)
            subject = metadata.read_xmp().get('Xmp.dc.subject', '')
            new_metadata = pyexiv2.Image(result_path)
            new_metadata.modify_xmp({'Xmp.dc.subject': subject})

        print('已保存：{}'.format(result_path))

    except:
        print('处理失败：{}'.format(path))
        traceback.print_exc()

print('\n全部完成。\n')
