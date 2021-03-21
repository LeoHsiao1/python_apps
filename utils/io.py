# -*- coding: utf-8 -*-
"""
与终端交互
"""

import os
import sys
import time


class Inputs:
    """
    提供一些从终端获取用户输入的静态方法。
      - 可在外部创建该类的变量，暂存一些输入的数据。
    """

    @staticmethod
    def input_int(tip_str='', retry=True):
        while retry:
            try:
                return int(input(tip_str))
            except:
                print("输入的不是整数！")

    @staticmethod
    def input_positive_int(tip_str='', retry=True):
        while retry:
            num = Inputs.input_int(tip_str, retry)
            if num > 0:
                return num
            else:
                print("输入的不是正整数！")

    @staticmethod
    def input_real_num(tip_str='', retry=True):
        while retry:
            try:
                return float(input(tip_str))
            except:
                print("输入的不是整数或浮点数！")

    @staticmethod
    def input_path(tip_str='', retry=True):
        while retry:
            path = input(tip_str)
            if os.path.isdir(path):
                # 如果该path存在，则转换成正常格式的绝对地址
                return os.path.abspath(os.path.normpath(path))
            else:
                print("输入的不是有效目录！")


def print_text(text, delay=0):
    """ 在DOS窗口中显示文本text，显示每个字符的间隔时长为delay """
    for line in text:
        for word in line:
            print(word, end='')  # 逐个字显示
            time.sleep(delay)
            # 每打印一个字符就刷新一次stdout，否则缓存区累积了一行才会显示
            sys.stdout.flush()
