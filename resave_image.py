# -*- coding: utf-8 -*-
"""
检索指定目录（包括子目录）下的所有图片，将它们另存到当前目录。
"""

import os
import traceback

from PIL import Image

from utils import Inputs, find_file, test_run


# 提示用户输入
print("该程序用于检索指定目录（包括子目录）下的所有.jpg图片，将它们另存到当前目录。")
Inputs.path = Inputs.input_path("请输入要检索的目录：")
Inputs.pattern = ("*.jpg", "*.JPG", "*.jpeg", "*.png")


print("检索所有图片...")
file_list = find_file(Inputs.path, "*.jpg")

# 创建一个保存被修改图片的文件夹
result_dir = os.path.join(os.getcwd(), "result")
os.makedirs(result_dir, exist_ok=True)

print("开始修改...")
for path in file_list:
    try:
        img = Image.open(path)

        # 可能有些图片只是后缀名为jpg，实际上却不是RGB模式，这里把它们都转换成RGB模式
        if img.mode != "RGB":
            img = img.convert("RGB")

        # 创建保存图片的子目录
        result_path = path.replace(Inputs.path, result_dir, 1)
        result_path = result_path[:result_path.rfind('.')] + ".jpg"
        os.makedirs(os.path.dirname(result_path), exist_ok=True)

        # 保存图片
        img.save(result_path, quality=95)
        print("已保存：{}".format(result_path))
        """将其它后缀名的图片转换成jpg图片时，可能会覆盖同名的jpg图片"""

    except:
        print("处理失败：{}".format(path))
        traceback.print_exc()

print("\n全部完成。\n")
