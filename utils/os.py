""" Used to extend functions of os module. """
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

