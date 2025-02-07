import logging

from src.app.http import app

logging.getLogger("flask").setLevel(logging.ERROR)
logging.getLogger("werkzeug").setLevel(logging.ERROR)
app.run(port=8233, threaded=True)