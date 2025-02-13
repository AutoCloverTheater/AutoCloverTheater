import logging
import threading
import time

from src.app import app, data_queue, clients_lock, send_event
from src.app.webui.webui import mainWindow
from src.facades.Logx.Logx import logx

logging.getLogger("flask").setLevel(logging.ERROR)
logging.getLogger("werkzeug").setLevel(logging.ERROR)

for rule in app.url_map.iter_rules():
    logx.info(rule)

port = 8233

threading.Thread(target=app.run, kwargs={'port': port, 'threaded': True}, daemon=True).start()
logx.info(f"listing port at {port}")
while True:
    data = time.strftime("%Y-%m-%d %H:%M:%S")
    logx.info(data)
    time.sleep(1)
# mainWindow(port)