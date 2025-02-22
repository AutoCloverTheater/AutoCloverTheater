import threading

IS_STOP_LOCK = threading.Lock()
TASK_THREAD = None
IS_STOP = False