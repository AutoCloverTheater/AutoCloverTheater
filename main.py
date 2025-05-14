import logging

from install import checkAdbutilsBinaries
from src.app import app

logging.getLogger("flask").setLevel(logging.ERROR)
logging.getLogger("werkzeug").setLevel(logging.ERROR)

port = 8233

if __name__ == '__main__':
    checkAdbutilsBinaries()
    app.run(port=port, threaded=True)