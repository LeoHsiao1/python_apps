""" Used to extend functions of re module. """
import re


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
    >>> replace('Hello World', 'Hello', '$1')
    ValueError: group id out of range : $1
    >>> replace('你好World', '([\\u4e00-\\u9fa5])(\w)', '$1 $2')
    '你好 World'
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
