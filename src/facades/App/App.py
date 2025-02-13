from threading import Lock,Event

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

def sseOutPut(message):
    with clients_lock:
        data_queue.append(message)
        send_event.set()
    pass