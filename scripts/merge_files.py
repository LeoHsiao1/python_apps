import os
import traceback

import _load_utils
from utils.io import Inputs
from utils.shell import find


# 提示用户输入
print("该脚本的用途：找出目标目录（包括子目录）下某种名字的文件，将它们合并成一个文件。")
Inputs.path = Inputs.input_path("请输入目标目录：")
Inputs.pattern = input("请输入文件名格式（比如'*.txt'）：")

# 设置保存检索结果的文件路径
result_file_name = "merge_result"

# 获得符合条件的文件列表
file_list = find(Inputs.path, pattern=Inputs.pattern)

# 读取每个文件的内容并合并
print("开始处理...")
with open(result_file_name, 'wb') as f:  # 以二进制模式打开，这样就不用考虑编码格式
    for path in file_list:
        try:
            with open(path, 'rb') as raw_file:
                f.write(raw_file.read())
                print("已处理：{}".format(path))
        except:
            print("处理失败：{}".format(path))
            traceback.print_exc()

print("\n全部完成！\n数据保存为文件：{} ".format(result_file_name))
