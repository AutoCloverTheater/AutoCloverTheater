import queue
import time

from act.facades.Emulator.Emulator import ConnectEmulator
from act.facades.Exceptions.HumanHandleException import HumanHandleException
from act.facades.Logx.Logx import logx
from act.facades.Runner.layout.LoginRunner import Login
from act.runtime.runtime import IS_STOP


class QueueSchedule:
    def __init__(self):
        self.queue = queue.Queue()  # 创建一个线程安全的队列

    def push(self, func, *args, **kwargs):
        self.queue.put((func, args, kwargs))

    def clear(self):
        """清空队列"""
        self.queue.queue.clear()

    def run(self):
        """工作线程函数，从队列中取出函数并执行"""
        if IS_STOP is False:
            while True:
                if not self.queue.empty():
                    func, args, kwargs = self.queue.get()
                    try:
                        logx.debug(f"Executing function: {func.__name__}")
                        func(*args, **kwargs)  # 执行函数
                    except HumanHandleException as e:
                        logx.warning(e)
                    except Exception as e:
                        logx.warning(f"Error executing function: {e}")
                        raise Exception(f"Error executing function: {e}")
                    finally:
                        self.queue.task_done()  # 标记任务完成
                else:
                    time.sleep(0.1)  # 队列为空时稍作等待，避免过度占用CPU
        else:
            logx.warning("任务队列已停止")

taskQueue = QueueSchedule()

if __name__ == '__main__':
    q = QueueSchedule()
    q.push(ConnectEmulator)
    q.push(Login)
    q.run()