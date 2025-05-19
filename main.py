import logging
import threading

from act.app import app
from act.facades.App.App import startSseData

logging.getLogger("flask").setLevel(logging.ERROR)
logging.getLogger("werkzeug").setLevel(logging.ERROR)

port = 8233

if __name__ == '__main__':
    threading.Thread(target=startSseData).start()
    app.run(port=port, threaded=True, debug=True)