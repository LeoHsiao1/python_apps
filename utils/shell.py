""" Used to execute shell commands, or simulate commands """
import difflib
import fnmatch
import os
import re
import shlex
import shutil
import subprocess
import sys


# Determine which platform is running on
platform    = sys.platform.lower() or 'unknown'    # It could be linux, win32, msys, cygwin, darwin, etc.
if os.name == 'nt' and 'GCC' in sys.version:
    platform = 'mingw'


class Exec:
    """
    Execute a command in the shell, return a `Exec` object.
    - Compatible with Windows, Linux, MacOS and other platforms.
    - `compatible_output=True`: filter out path delimiters, whitespace characters in output.
    - `decode_output=True`: decode output from bytes to str.

    Sample:
    >>> Exec('echo Hello')
    Hello
    >>> Exec('echo Hello').returncode
    0
    """

    def __init__(self,
                 cmd: str,
                 cwd=None,
                 extra_env=dict(),
                 encoding='utf-8',
                 stdin: (str, bytes) = None,
                 redirect_stderr_to_stdout=True,
                 assert_returncode=[0],
                 compatible_output=True,
                 decode_output=True):
        self.cmd            = cmd                   # command to be executed
        self.cwd            = cwd or os.getcwd()    # current work dir

        # set environment variables
        self.env            = os.environ.copy()
        self.env.update(extra_env)

        self.encoding       = encoding
        self.stdin          = stdin
        # self.stdout       = None
        # self.stderr       = None
        self.redirect_stderr_to_stdout  = redirect_stderr_to_stdout
        self.assert_returncode          = assert_returncode
        # self.returncode   = 0
        self.compatible_output  = compatible_output
        self.decode_output      = decode_output

        # Generate the args for subprocess.Popen
        if platform in ['win32', 'mingw']:
            # 'cmd /c' means to execute commands in the shell in case the executable file is not found
            self.args = 'cmd /c ' + self.cmd.replace('\'', '\"')
        else:
            self.args = shlex.split(self.cmd, posix=os.name == 'posix')

        # Check stdin
        if self.stdin:
            if not isinstance(stdin, bytes):
                self.stdin = str(stdin).encode(self.encoding)

        self.run()

    def __str__(self):
        return self.stdout

    def __repr__(self):
        return self.__str__()

    def run(self):
        # Check stdout
        if self.redirect_stderr_to_stdout:
            stderr   = subprocess.STDOUT
        else:
            stderr   = subprocess.PIPE

        # Execute the command in subprocess
        try:
            with subprocess.Popen(self.args,
                                  cwd=self.cwd,
                                  env=self.env,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  stderr=stderr
                                  ) as self.subprocess:
                try:
                    output  = self.subprocess.communicate(self.stdin, timeout=10)  # Assign (stdout, stderr) to output
                except subprocess.TimeoutExpired:
                    self.subprocess.kill()
                    output  = self.subprocess.communicate()
        except:
            raise RuntimeError('Failed to execute: {}'.format(self.args))
        output          = [i or b'' for i in output]
        output          = [i.rstrip(b'\r\n').rstrip(b'\n') for i in output] # Remove the last line break of the output

        # Extract stdout and stderr
        if self.compatible_output:
            output      = [i.replace(b'\r\n', b'\n')    for i in output]   # Fix dos line-endings
            output      = [i.replace(b'\\', rb'/')      for i in output]   # Fix dos path separators
        if self.decode_output:
            output      = [i.decode(self.encoding)      for i in output]
        self.stdout, self.stderr = [i or None           for i in output]

        # Check return code
        self.returncode = self.subprocess.returncode
        if self.assert_returncode and self.returncode not in self.assert_returncode:
            tips = '\n'
            tips += '  Failed to execute: {}\n'.format(self.args)
            tips += '  The asserted return code is {}, but got {}\n'.format(str(self.assert_returncode), self.subprocess.returncode)
            tips += 'OUTPUT:\n{}\n'.format(output[0] + output[1])
            raise RuntimeError(tips)


class Output:
    """
    Simulate the stdout buffer.
    You can use `out += x` to simulate `print(x)`.

    Sample:
    >>> out = Output()
    >>> out
    <__main__.Output object at 0x00000201D51F78B0>
    >>> str(out)            # The initial content of Output() is empty
    ''
    >>> out += 'Hello'
    >>> out += 1
    >>> out += ['Hi' , 2]
    >>> out += None         # Adding None has no effect
    >>> str(out)
    "Hello\n1\n['Hi', 2]"
    """
    def __init__(self):
        self.lines = []
        self.newline = '\n'

    def __str__(self):
        return self.newline.join(self.lines)

    # Comment it so that log does not automatically convert to str type
    # def __repr__(self):
    #     return str(self)

    def __add__(self, other):
        if other != None and other.__str__() != None:
            self.lines.append(str(other))
        return self

    def __radd__(self, other):
        return self.__add__(other)


def find(directory='.', pattern=None, re_pattern=None, depth=-1, onerror=print) -> list:
    """
    Find files and directories that match the pattern in the specified directory and return their paths.
    Work in recursive mode. If there are thousands of files, the runtime may be several seconds.
    - `directory`   : Find files in this directory and its subdirectories
    - `pattern`     : Filter filename based on shell-style wildcards.
    - `re_pattern`  : Filter filename based on regular expressions.
    - `depth`       : Depth of subdirectories. If its value is negative, the depth is infinite.
    - `onerror`     : A callable parameter. it will be called if an exception occurs.

    Sample:
    find(pattern='*.py')
    find(re_pattern='.*.py')
    """
    if not os.path.isdir(directory):
        raise ValueError('{} is not an existing directory.'.format(directory))

    try:
        file_list = os.listdir(directory)
    except PermissionError as e:    # Sometimes it does not have access to the directory
        onerror('PermissionError: {}'.format(e))
        return []

    def match(name, pattern=None, re_pattern=None):
        if pattern and not fnmatch.fnmatch(name, pattern):
            return False
        if re_pattern and not re.findall(re_pattern, name):
            return False
        return True

    path_list = []
    if match(os.path.basename(directory), pattern, re_pattern):
        path_list.append(directory)
    if depth != 0:
        for filename in file_list:
            path = os.path.join(directory, filename)
            if os.path.isdir(path):
                path_list.extend(find(path, pattern, re_pattern, depth-1, onerror))
                continue
            if match(filename, pattern, re_pattern):
                path_list.append(path)

    return path_list


def cp(src, dst):
    """ Copy one or more files or directories. It simulates `cp -rf src dst`. """
    if os.path.isfile(src):
        shutil.copy(src, dst)
    elif os.path.isdir(src):
        if os.path.isdir(dst):
            dst_dir = os.path.join(dst, os.path.basename(src))
        else:
            dst_dir = dst
        for src_path in find(src):
            relpath = os.path.relpath(src_path, src)
            dst_path = os.path.join(dst_dir, relpath)
            if os.path.isdir(src_path):
                os.makedirs(dst_path, exist_ok=True)
            else:
                shutil.copy(src_path, dst_path)
    else:
        raise ValueError('src is not a valid path to a file or directory.')


def rm(*paths):
    """ Remove one or more files or directories. It simulates `rm -rf paths`. """
    for path in paths:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            for sub_path in find(path, depth=1)[1:]:
                if os.path.isdir(sub_path):
                    rm(sub_path)
                else:
                    os.remove(sub_path)
            os.rmdir(path)  # Remove the directory only when it is empty
        else:
            continue


def mv(src, dst):
    """ Move one or more files or directories. """
    cp(src, dst)
    rm(src)


def cat(*files, encoding='utf-8', return_bytes=False):
    if return_bytes:
        result = b''
        for i in files:
            with open(i, 'rb') as f:
                result += f.read()
    else:
        result = ''
        for i in files:
            with open(i, 'r', encoding=encoding) as f:
                result += f.read()
    return result


def grep(pattern, *files, encoding='utf-8'):
    result  = ''
    pattern = '.*{}.*'.format(pattern)
    for i in files:
        content = cat(i, encoding=encoding)
        result += '\n'.join(re.findall(pattern, content))
    return result


def save(content: (bytes, str, tuple, list), filename, encoding='utf-8'):
    if isinstance(content, bytes):
        with open(filename, 'wb') as f:
            f.write(content)
        return
    if isinstance(content, (tuple, list)):
        content = '\n'.join(content)
    if isinstance(content, str):
        with open(filename, 'w', encoding=encoding) as f:
            f.write(content)
    else:
        raise ValueError('Expect content of type (bytes, str, tuple, list), but get {}'.format(type(content).__name__))


def diff(file1, file2, encoding='utf-8'):
    """
    Simulates the output of GNU diff.
    You can use `diff(f1, f2)` to simulate `diff -w f1 f2`
    """
    encoding     = encoding
    texts        = []
    for f in [file1, file2]:
        with open(f, encoding=encoding) as f:
            text = f.read()
        text     = text.replace('\r\n', '\n') # Ignore line breaks for Windows
        texts   += [text.split('\n')]
    text1, text2 = texts

    output       = []
    new_part     = True
    num          = 0
    for line in difflib.unified_diff(text1, text2, fromfile=file1, tofile=file2, n=0, lineterm=''):
        num     += 1
        if num   < 3:
            # line         = line.replace('--- ', '<<< ')
            # line         = line.replace('+++ ', '>>> ')
            # output      += [line]
            continue

        flag             = line[0]
        if flag         == '-':   # line unique to sequence 1
            new_flag     = '< '
        elif flag       == '+':   # line unique to sequence 2
            new_flag     = '> '
            if new_part:
                new_part = False
                output  += ['---']
        elif flag       == ' ':   # line common to both sequences
            # new_flag   = '  '
            continue
        elif flag       == '?':   # line not present in either input sequence
            new_flag     = '? '
        elif flag       == '@':
            output      += [re.sub(r'@@ -([^ ]+) \+([^ ]+) @@', r'\1c\2', line)]
            new_part     = True
            continue
        else:
            new_flag     = flag
        output          += [new_flag + line[1:]]

    return '\n'.join(output)


def diff_bytes(file1, file2, return_str=False):
    """
    Compare the bytes of two files.
    Simulates the output of GNU diff.
    """
    texts        = []
    for f in [file1, file2]:
        with open(f, 'rb') as f:
            text = f.read()
        text     = text.replace(b'\r\n', b'\n') # Ignore line breaks for Windows
        texts   += [text.split(b'\n')]
    text1, text2 = texts

    output       = []
    new_part     = True
    num          = 0
    for line in difflib.diff_bytes(difflib.unified_diff, text1, text2,
                                   fromfile=file1.encode(), tofile=file2.encode(), n=0, lineterm=b''):
        num     += 1
        if num   < 3:
            line         = line.decode()
            line         = line.replace('--- ', '<<< ')
            line         = line.replace('+++ ', '>>> ')
            output      += [line.encode()]
            continue

        flag             = line[0:1]
        if flag         == b'-':   # line unique to sequence 1
            new_flag     = b'< '
        elif flag       == b'+':   # line unique to sequence 2
            new_flag     = b'> '
            if new_part:
                new_part = False
                output  += [b'---']
        elif flag       == b' ':   # line common to both sequences
            # new_flag   = b'  '
            continue
        elif flag       == b'?':   # line not present in either input sequence
            new_flag     = b'? '
        elif flag       == b'@':
            output      += [re.sub(rb'@@ -([^ ]+) \+([^ ]+) @@', rb'\1c\2', line)]
            new_part     = True
            continue
        else:
            new_flag     = flag
        output          += [new_flag + line[1:]]

    if return_str:
        return '\n'.join([repr(line)[2:-1] for line in output])
    else:
        return b'\n'.join(output)


def md5sum(filename):
    """ Calculate the MD5 value of the file """
    import hashlib
    with open(filename, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

