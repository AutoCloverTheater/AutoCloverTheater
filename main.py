import logging
import threading
import time

from src.app import app
from src.app.webui.webui import mainWindow
from src.facades.Logx.Logx import logx
from src.facades.QueueSchedule.QueueSchedule import QueueSchedule

logging.getLogger("flask").setLevel(logging.ERROR)
logging.getLogger("werkzeug").setLevel(logging.ERROR)

for rule in app.url_map.iter_rules():
    logx.info(rule)

port = 8233

threading.Thread(target=app.run, kwargs={'port': port, 'threaded': True}, daemon=True).start()
logx.info(f"listing port at {port}")

mainWindow(port)