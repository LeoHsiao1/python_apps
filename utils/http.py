""" Contains some code related to HTTP """
import multiprocessing
import os
import time


class HttpServer:
    """
    Used to start an HTTP server, equivalent to executing `python3 -m http.server`
    
    Sample:
    >>> HttpServer(bind='127.0.0.1'), port=80)
    """

    def __init__(self, bind='127.0.0.1', port=80, work_dir='.'):
        self.bind = bind
        self.port = int(port)
        self.work_dir = work_dir

    def _start(self):
        from http import server
        os.chdir(self.work_dir)
        server.test(HandlerClass=server.SimpleHTTPRequestHandler, bind=self.bind, port=self.port)
        RuntimeError('The HTTP server exits without calling stop()')

    def start(self):
        from urllib import request
        self.proc = multiprocessing.Process(target=self._start, name=str(self))
        self.proc.start()
        time.sleep(2)
        try:
            with request.urlopen('http://127.0.0.1:{}'.format(self.port), timeout=3) as f:
                if f.status != 200:
                    raise RuntimeError()
        except:
            raise RuntimeError('Failed to run the HTTP server')

    def stop(self):
        self.proc.terminate()

