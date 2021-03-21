"""
扩展os模块的功能
"""
import os
import fnmatch
import re


def list_all_files(directory='.', onerror=print):
    """
    Lists all files under the specified directory and its subdirectories. 
    - `directory`: An existing directory.
    - `onerror`: A callable param. it will be called if an exception occurs.

    Work in generator mode. Process one directory at each iteration.
    
    Sample:
    >>> for paths in list_all_files('.'):
    >>>     print(paths)
    """
    for basepath, dirnames, filenames in os.walk(directory, onerror=onerror):
        path_list = []
        for name in dirnames + filenames:
            path_list.append(os.path.join(basepath, name))
        yield path_list


def find_file(directory='.', depth=-1, pattern=None, re_pattern=None, onerror=print) -> list:
    """
    Find some files and return their paths.
    - `directory`: An existing directory.
    - `depth`: The max depth for finding files. If its value is negative, the depth is infinite.
    - `pattern`: Filter filename based on shell-style wildcards.
    - `re_pattern`: Filter filename based on regular expressions.
    - `onerror`: A callable param. it will be called if an exception occurs.
    
    Work in recursive mode. If there are thousands of files, the runtime may be several seconds.

    Sample:
    >>> find_file('.', pattern='*.py')
    >>> find_file('.', re_pattern='.*.py')
    """
    if not os.path.isdir(directory):
        raise ValueError("{} is not an existing directory.".format(directory))

    try:
        file_list = os.listdir(directory)
    except PermissionError as e:    # Sometimes it does not have access to the directory
        onerror("PermissionError: {}".format(e))
        return -1

    path_list = []
    for filename in file_list:
        path = os.path.join(directory, filename)
        if depth != 0 and os.path.isdir(path):
            sub_list = find_file(path, depth-1, pattern, re_pattern, onerror)
            if sub_list != -1:
                path_list.extend(sub_list)
            continue
        if pattern and not fnmatch.fnmatch(filename, pattern):
            continue
        if re_pattern and not re.findall(re_pattern, filename):
            continue
        path_list.append(path)

    return path_list


def locate_path(basedir: str, path: str) -> str:
    """
    Locate the relative `path` to the `basedir`.

    Sample:
    >>> locate_path('/root/', './1.py')
    '/root/1.py'
    >>> locate_path('/root/', '../1.py')
    '/1.py'
    """
    # Return the path if it is not a relative path
    splited_path = path.replace('\\', '/').split('/')
    if not splited_path[0] in ['.', '..']:
        return path
    # Return the located path
    return os.path.abspath(os.path.join(basedir, path))

