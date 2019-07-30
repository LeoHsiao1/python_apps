# -*- coding: utf-8 -*-
"""
该程序用于检索指定目录（包括子目录）下某种后缀名的文件，将它们合并成一个文件。
"""

import os
import traceback

from utils import Inputs, searchFile, test_run


def main():
    # 提示用户输入
    print("该程序用于检索指定目录（包括子目录）下某种后缀名的文件，将它们合并成一个文件。")
    Inputs.path = Inputs.input_path("请输入要检索的目录：")
    Inputs.suffix = input("请输入要合并的这类文件的后缀名（例如'.txt'）：")

    # 设置保存检索结果的文件路径
    result_file_name = "merge_result" + Inputs.suffix

    # 获得符合条件的文件列表
    file_list = searchFile(Inputs.path, Inputs.suffix)

    # 读取每个文件的内容并合并
    print("开始检索...")
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


if __name__ == "__main__":
    test_run(main)
