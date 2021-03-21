""" Used for recording and managing logs """
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
    Record logs based on the logging module.
    """

    def __init__(self, name, level='INFO'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self._checkLevel(level))
        self.formatter = logging.Formatter(
            fmt='{asctime}  {levelname:5}  {threadName:15} : {message}', style='{')

    def _checkLevel(self, level):
        """
        Check if the log level is valid.
        - Valid values include: {'CRITICAL': 50, 'FATAL': 50, 'ERROR': 40,
          'WARN': 30, 'WARNING': 30, 'INFO': 20, 'DEBUG': 10, 'NOTSET': 0}
        """
        return logging._checkLevel(level)

    def to_file(self, filename, level='DEBUG'):
        """ Add a log handler to output the log to a file. """
        handler = logging.FileHandler(filename)
        handler.setLevel(self._checkLevel(level))
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)

    def to_console(self, level='INFO'):
        """ Add a log handler to output the log to the console. """
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self._checkLevel(level))
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)

    def log(self, level, msg, *args, **kwargs):
        self.logger.log(self._checkLevel(level), msg, *args, **kwargs)


if __name__ == '__main__':
    logger = Logger(__file__, 'DEBUG')

    filename = __file__ + time.strftime('_%Y%m%d', time.localtime()) + '.log'
    logger.to_file(filename, 'DEBUG')

    logger.to_console('INFO')

    logger.log('DEBUG', 'aaa')
    logger.log('INFO', 'bbb')
