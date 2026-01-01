"""
该脚本调用 edge-tts 来朗读英文 text ，生成 mp3 文件。
需要先安装 pip install edge-tts
"""

import os
import re
import subprocess


def replace(string, src: str, dst: str) -> str:
    """
    Replace `src` with `dst` in `string`, based on regular expressions.

    Sample:
    >>> replace('Hello World', 'Hello', 'hi')
    'hi World'
    >>> replace('Hello World', '(Hello).', 'hi')
    'hiWorld'
    >>> replace('Hello World', '(Hello).', '$1,')
    'Hello,World'
    """
    # Check the element group
    src_group_num = min(len(re.findall(r'\(', src, re.A)), len(re.findall(r'\)', src, re.A)))
    dst_group_ids = re.findall(r'\$(\d)', dst, re.A)
    if dst_group_ids:
        dst_group_ids = list(set(dst_group_ids))  # Remove duplicate id
        dst_group_ids.sort()
        max_group_id = int(dst_group_ids[-1])
        if max_group_id > src_group_num:
            raise ValueError('group id out of range : ${}'.format(max_group_id))

    # replace
    if dst_group_ids:
        pattern = re.compile('({})'.format(src), re.A)
        result = string[:]
        for match in pattern.findall(string):
            _dst = dst[:]
            for i in dst_group_ids:
                i = int(i)
                _dst = _dst.replace('${}'.format(i), match[i])
            result = result.replace(match[0], _dst)
    else:
        pattern = re.compile(src, re.A)
        result = pattern.sub(dst, string)

    return result


try:
    # 读取原文本
    with open('text.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    # 在文本中插入 \n ，使得朗读时停顿
    text = replace(text, '```yml', '```')
    text = replace(text, ' # .*', '') # 忽略 # 开头的注释，从而简化朗读内容
    text = replace(text, '#', '\nhashtag\n')
    text = replace(text, '- ', '\nnext paragraph\n')
    text = replace(text, '/', ' or ')
    # text = replace(text, ' +([\\u4e00-\\u9fa5])', '\n$1')
    # text = replace(text, '  +', '\n')

    # 保存修改后的文本
    with open('text_modified.txt', 'w', encoding='utf-8') as f:
        f.write(text)

    # 用 edge-tts 朗读文本，生成 mp3 文件
    command='edge-tts --voice en-US-AvaMultilingualNeural --file text_modified.txt --write-media text.mp3'
    with os.popen(command) as p:
        print(p.read())

    print('done')
    # with os.popen('pause') as p:
    #     print(p.read())

except Exception as e:
    print('Error: {}'.format(str(e)))
