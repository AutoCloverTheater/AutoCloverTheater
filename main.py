import logging

from src.app.http import app
from src.facades.Logx.Logx import logx

logging.getLogger("flask").setLevel(logging.ERROR)
logging.getLogger("werkzeug").setLevel(logging.ERROR)

for rule in app.url_map.iter_rules():
    logx.info(rule)
app.run(port=8233, threaded=True)