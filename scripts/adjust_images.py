# -*- coding: utf-8 -*-
"""
需要安装：  pip install pillow==7.0.0 pyexiv2==2.0.0
"""
import os
import traceback

from PIL import Image
import pyexiv2

from utils import Inputs, find_file


print("""该脚本的用途：检查目标目录（包括子目录）下的所有图片，如果它们不符合以下特征则自动修改：
- 后缀名为jpg
- 只保留图片元数据中的标签""")

Inputs.path = Inputs.input_path('请输入目标目录：')

print('检索所有文件...')
file_list = find_file(Inputs.path)

print('开始处理...')
for path in file_list:
    suffix = path[path.rfind('.'):]
    # 只处理这些后缀名的图片文件
    if suffix.lower() not in ['.jpg', '.jpeg', '.webp', '.png', '.jfif']:
        continue
    new_suffix = '.jpg'

    try:
        img = Image.open(path)

        # 如果原图片已满足条件，则不修改
        if suffix == '.jpg' and img.mode == 'RGB' and img.size[1] >= 1080:
            continue
        
        # 通过pillow生成新图片并保存
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # # 如果原图片的高度小于1080，则放大至1080（这样放大会产生锯齿）
        # if img.size[1] < 1080:
        #     width, height = img.size
        #     times = 1080 / height
        #     new_size = round(width * times), round(height * times)
        #     img = img.resize(new_size)

        # 生成新图片的保存路径
        new_path = path[:path.rfind('.')] + new_suffix
        # 如果新路径已被其它文件占用，则在文件名末尾再添加一个.jpg（此后需要手动改名）
        if new_path != path:
            while 1:
                if os.path.isfile(new_path):
                    new_path += '.jpg'
                else:
                    break

        # 读取原图片的标签
        with pyexiv2.Image(path, 'gbk') as metadata:
            subject = metadata.read_xmp().get('Xmp.dc.subject')

        # 保存新图片
        img.save(new_path, format='JPEG', quality=95)

        # 删除原图片
        img.close()
        if new_path != path:
            os.remove(path)
        
        # 写入原图片的标签
        if subject:
            with pyexiv2.Image(new_path, 'gbk') as new_metadata:
                new_metadata.modify_xmp({'Xmp.dc.subject': subject})

        # # 清除图片的元数据
        # with pyexiv2.Image(new_path) as img:
        #     img.clear_exif()
        #     img.clear_iptc()
        #     img.clear_xmp()

        print('已保存：{}'.format(new_path))

    except:
        print('处理失败：{}'.format(path))
        traceback.print_exc()

print('\n全部完成。\n')
