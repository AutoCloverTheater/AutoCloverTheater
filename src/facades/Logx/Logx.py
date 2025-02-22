import datetime
import logging
import sys
import time

from loguru import logger

from src.facades.App.App import sseOutPut
from src.facades.Constant.Constant import RUNTIME_PATH

# 自定义日志格式和颜色
def custom_format(record):
    color_map = {
        "INFO": "green>",
        "WARNING": "yellow>",
        "ERROR": "red>",
    }
    color = color_map.get(record["level"].name, "white>")  # 默认白色
    return f"<{color}{{time:HH:mm:ss}} | {{level}} | {{message}}</{color}\n"


def setup_logger():
    logger.remove()

    now = datetime.datetime.now().strftime("%Y-%m-%d-%H")

    # logger.add(f"{RUNTIME_PATH.joinpath('logs')}/{now}/info.log",format="<green>{time:YYYY-MM-DD HH:mm:ss} - {message}</green>",
    #            rotation="1 week", enqueue=True,backtrace=True, diagnose=True,level=logging.INFO)

    logger.add(f"{RUNTIME_PATH.joinpath('logs')}/{now}/error.log",format="<red>{time:YYYY-MM-DD HH:mm:ss} - {message} File:{file.path}, Line {line}, function {function}</red>",
               rotation="1 week", enqueue=True,backtrace=True, diagnose=True,level=logging.ERROR)

    logger.add(sys.stdout,format=custom_format,
               level=logging.DEBUG)

    logger.add(sseOutPut,format=custom_format,
               level=logging.INFO)

setup_logger()
logx = logger

# 示例使用
if __name__ == "__main__":
    while 1:
        logx.info("消息")
        logx.debug("调试")
        logx.error("错误")
        logx.warning("警告")
        time.sleep(1)
