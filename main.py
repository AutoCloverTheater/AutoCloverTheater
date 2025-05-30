import logging
import threading

from act.app import app
from act.facades.App.App import startSseData

logging.getLogger("flask").setLevel(logging.ERROR)
logging.getLogger("werkzeug").setLevel(logging.ERROR)
logging.getLogger('paddlex').setLevel(logging.ERROR)
logging.getLogger('paddle').setLevel(logging.ERROR)
logging.getLogger('paddleocr').setLevel(logging.ERROR)

port = 8233

if __name__ == '__main__':
    threading.Thread(target=startSseData).start()
    app.run(host="0.0.0.0",port=port, threaded=True, debug=True)