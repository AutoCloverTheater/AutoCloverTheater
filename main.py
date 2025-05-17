import logging

from act.app import app

logging.getLogger("flask").setLevel(logging.ERROR)
logging.getLogger("werkzeug").setLevel(logging.ERROR)

port = 8233

if __name__ == '__main__':
    app.run(port=port, threaded=True, debug=True)