import logging
import threading

from src.facades.Runner.WorldTreeRunner import WorldTreeRunner


class App:
    def __init__(self):
        # 配置日志
        self.threads = []
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - 「Clover」%(levelname)s - %(message)s')
    def searchDevice(self) -> list:
        """
        根据选中的模拟器类型搜索设备
        :return:
        """
        return []
    def connectDevice(self):
        """
        连接设备
        :return:
        """
        pass

    def runWorldTree(self):
        """
        运行世界树
        :return:
        """
        run = WorldTreeRunner()
        thread = threading.Thread(run.run(), name=run.__class__.__name__)
        self.threads.append({"thread":thread, "runnerInstance": run})
        pass

    def runAll(self):
        self.runWorldTree()


    def stopAll(self, t):
        for item in self.threads:
            if item.thread.is_alive():
                item.runnerInstance.stop()
                item.thread.join(timeout=t)  # 等待线程结束，最多等待1秒
                if item.thread.is_alive():
                    logging.warning(f"Thread {item.runnerInstance.__class__.__name__} did not terminate in time")
        self.threads.clear()  # 清空线程列表