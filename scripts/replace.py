# -*- coding: utf-8 -*-
'''
该脚本的用途：替换文件中的字符串，基于正则语法。

Sample：
python3 replace.py --file 1.py --src '([\u4e00-\u9fa5])(\w)' --dst '$1 $2'
'''
from utils import replace
import argparse


parser = argparse.ArgumentParser(description=r"""This script is use to replace string in a file. Sample: python3 replace.py --file 1.py --src '([\u4e00-\u9fa5])(\w)' --dst '$1 $2' """)
parser.add_argument('--file', help='a valid file path', type=str, required=True)
parser.add_argument('--src', help='the source string, which is a regular expression.', type=str, required=True)
parser.add_argument('--dst', help='the destination string', type=str, required=True)
parser.add_argument('--encoding', help='the encoding of the original file, which is utf-8 by default.', type=str, default='utf-8')
args = parser.parse_args()


try:
    with open(args.file, 'r', encoding=args.encoding) as f:
        raw_text = f.read()
        print('Handling file: {} ...'.format(args.file), end='\t')

    result = replace(raw_text, args.src, args.dst)

    if raw_text == result:
        print('skip')
    else:
        with open(args.file, 'w', encoding=args.encoding) as f:
            f.write(result)
            print('done')

except Exception as e:
    print('Error: {}'.format(str(e)))
