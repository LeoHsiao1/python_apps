"""
For drawing.
Installation required: pip install matplotlib
"""

import threading

import matplotlib.pyplot as plt

from .time import Timer


class DynamicPlot(threading.Thread):
    """
    用于显示一个图表并实时刷新。
      - 横轴为启动时间，从0开始计时。
      - 每次调用add()时输入一个值，会绘制出一个新点，其横坐标为当前时间、纵坐标为y。
      - 绘制一个新点之后，会用一条线段连接上一个点与新点。也可不显示线段，改为散点图。
    """
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance == None:  # 单例模式
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, title='', ylabel='', *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self._title = title
        self.name = title
        self._xlabel = "Run Time (s)"
        self._ylabel = ylabel
        self._askToStop = False
        self._dots = []
        self.t = Timer("Run Time")

    def add(self, y):
        """ 在图上加入一个点，传入其y轴坐标。 """
        if isinstance(y, (int, float)):
            self._dots.append([self.t.count, y])
        else:
            raise TypeError("y must be a int or float")

    def run(self):
        """ 线程的主循环 """
        plt.title(self._title)
        plt.xlabel(self._xlabel)
        plt.ylabel(self._ylabel)
        plt.ion()  # 打开交互模式

        while not self._askToStop:
            # 如果没有输入新点，就保持显示，否则显示所有新点
            if len(self._dots) == 0:
                plt.pause(0.1)
            else:
                dots = self._dots
                self._dots = []
                _dots = list(zip(*dots))
                plt.plot(_dots[0], _dots[1], color="blue",
                         linestyle="", marker=".")
                # 每次循环绘制的是一条新线段，颜色随机，这里给它们设置统一的颜色
                plt.pause(0.1)

        # TODO：鼠标拖动图像窗口时，plot线程会暂停运行，待考虑这个问题

    def show(self):
        self.start()

    def stop(self):
        self._askToStop = True


# sample
if __name__ == "__main__":
    p1 = DynamicPlot("Communication Delay", "delay")
    p1.show()
    import time
    for i in range(10, 20):
        p1.add(i)
        time.sleep(1)
