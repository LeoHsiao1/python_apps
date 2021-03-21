import os
import sys


# 将项目根目录加入 sys.path ，从而允许导入 utils
root_dir = os.path.normpath(os.path.join(os.path.abspath(__file__), '../../'))
sys.path.append(root_dir)

