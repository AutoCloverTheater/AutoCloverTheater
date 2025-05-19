import time
from threading import Lock,Event

from act.facades.sqlite.logs import LogsModel

# 用于存储 SSE 客户端的连接
clients = {}
clients_lock = Lock()

# 用于触发发送数据的事件
send_event = Event()
data_queue = []

# 定义一个标志变量，用于跟踪定时器是否已经执行
timer_executed = False

def getExecuted():
    return timer_executed

def setExecuted(value):
    timer_executed = value
    return timer_executed

def startSseData():
    LogsModel.update_log()
    # 创建一个线程，用于定时取数据
    offset = 0
    while True:
        raw = LogsModel.getLastestLogs(offset, 30)
        if len(raw) >0:
            offset = raw[0]['id']
        for item in raw:
            data_queue.append(item['info'])
        time.sleep(1)