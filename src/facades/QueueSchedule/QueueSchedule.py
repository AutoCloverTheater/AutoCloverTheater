
import time

import queue

from src.facades.Emulator.Emulator import ConnectEmulator
from src.facades.Logx.Logx import logx
from src.facades.Runner.layout.LoginRunner import Login


class QueueSchedule:
    def __init__(self):
        self.queue = queue.Queue()  # 创建一个线程安全的队列

    def push(self, func, *args, **kwargs):
        self.queue.put((func, args, kwargs))

    def run(self):
        """工作线程函数，从队列中取出函数并执行"""
        while True:
            if not self.queue.empty():
                func, args, kwargs = self.queue.get()
                try:
                    logx.info(f"Executing function: {func.__name__}")
                    func(*args, **kwargs)  # 执行函数
                except Exception as e:
                    logx.exception(f"Error executing function: {e}")
                    raise Exception(f"Error executing function: {e}")
                finally:
                    self.queue.task_done()  # 标记任务完成
            else:
                time.sleep(0.1)  # 队列为空时稍作等待，避免过度占用CPU

if __name__ == '__main__':
    q = QueueSchedule()
    q.push(ConnectEmulator)
    q.push(Login)
    q.run()