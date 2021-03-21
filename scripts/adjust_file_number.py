# -*- coding: utf-8 -*-
import os
import re
import traceback

import _load_utils
from utils.io import Inputs
from utils.os import find_file


print("""该脚本的用途：检查目标目录（包括子目录）下所有文件的文件名，将编号 (1) - (9) 改为 (01) - (09) 。""")
Inputs.path = Inputs.input_path('请输入要检索的目录：')

print('检索所有文件...')
file_list = find_file(Inputs.path)

for path in file_list:
    dirname, basename = os.path.split(path)
    pattern = r' \(([1-9])\)'
    number = re.findall(pattern, basename)
    if number:
        number = number[0]
    else:
        continue
    new_basename = re.sub(pattern, ' (0{})'.format(number), basename)
    new_path = os.path.join(dirname, new_basename)

    try:
        os.rename(path, new_path)
        print('已改名：{}'.format(new_path))

    except:
        print('处理失败：{}'.format(path))
        traceback.print_exc()

print('\n全部完成。\n')
