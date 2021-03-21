"""
用于记录日志
"""

import time
import logging


class Log:
    """
    A simple log class for caching log text.

    Sample:
    >>> log = Log()
    >>> log.info('test...')
    >>> log.warn('test...')
    >>> log.dump()
    '[INFO] test...\n[WARN] test...'
    """

    def __init__(self):
        self.buffer = []

    def clear(self):
        self.buffer = []

    def to_str(self):
        return '\n'.join(self.buffer)

    def dump(self):
        _dump = self.to_str()
        self.clear()  # clear the buffer to avoid duplicate output
        return _dump

    def add(self, msg):
        self.buffer.append(str(msg))

    def info(self, msg, index=None):
        self.add('[INFO] {}'.format(msg))

    def warn(self, msg):
        self.add('[WARN] {}'.format(msg))

    def error(self, msg):
        self.add('[ERROR] {}'.format(msg))


class Logger:
    """
    基于logging模块定义一个日志器。
      - 外部调用该类即可记录日志，不需要再导入logging模块。
      - 统一使用logger.log("INFO", "bbb")的格式记录日志，这样通用性强。
    """

    def __init__(self, name, level="INFO"):
        self.logger = logging.getLogger(name)   # 创建一个日志器
        self.logger.setLevel(self._checkLevel(level))  # 设置日志级别，进行过滤
        self.formatter = logging.Formatter(
            fmt="{asctime}  {levelname:5}  {threadName:15} : {message}", style='{')

    def _checkLevel(self, level):
        """
        检查日志级别level的取值是否合法。
          - 这里调用logging模块，取值范围为：{'CRITICAL': 50, 'FATAL': 50, 'ERROR': 40,
          'WARN': 30, 'WARNING': 30, 'INFO': 20, 'DEBUG': 10, 'NOTSET': 0}
        """
        return logging._checkLevel(level)

    def to_file(self, filename, level="DEBUG"):
        """ 添加一个日志处理器，将日志输出到一个文件（写入为追加模式）。 """
        handler = logging.FileHandler(filename)
        handler.setLevel(self._checkLevel(level))
        handler.setFormatter(self.formatter)  # 设置该handler的格式
        self.logger.addHandler(handler)  # 将该handler添加到日志器

    def to_console(self, level="INFO"):
        """ 添加一个日志处理器，将日志输出到终端。 """
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self._checkLevel(level))
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)

    def log(self, level, msg, *args, **kwargs):
        self.logger.log(self._checkLevel(level), msg, *args, **kwargs)


# sample
if __name__ == "__main__":
    logger = Logger(__file__, "DEBUG")

    filename = __file__ + time.strftime("_%Y%m%d", time.localtime()) + ".log"
    logger.to_file(filename, "DEBUG")

    logger.to_console("INFO")

    logger.log("DEBUG", "aaa")
    logger.log("INFO", "bbb")
