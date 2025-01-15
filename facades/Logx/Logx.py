import datetime
import logging
import os
from facades.Constant.Constant import RUNTIME_PATH

# 这是设置airtest日志等级
logging.getLogger('airtest').setLevel(logging.ERROR)

# 定义颜色代码
COLORS = {
    'DEBUG': '\033[94m',    # 蓝色
    'INFO': '\033[92m',     # 绿色
    'WARNING': '\033[93m',  # 黄色
    'ERROR': '\033[91m',    # 红色
    'CRITICAL': '\033[91m', # 红色
    'RESET': '\033[0m'      # 重置颜色
}

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        # 获取日志等级名称
        levelname = record.levelname
        # 根据日志等级添加颜色
        if levelname in COLORS:
            record.levelname = f"{COLORS[levelname]}{levelname}{COLORS['RESET']}"
            record.msg = f"{COLORS[levelname]}{record.msg}{COLORS['RESET']}"
            record.pathname = f"{COLORS[levelname]}{record.pathname}{COLORS['RESET']}"
            record.asctime = f"{COLORS[levelname]}{record.asctime}{COLORS['RESET']}"
        return super().format(record)
def setup_logger():
    # 创建日志记录器
    logger = logging.getLogger("clover")
    logger.setLevel(logging.INFO)
    # 禁用传播
    logger.propagate = False
    # 定义时间格式
    date_format = '%Y-%m-%d %H:%M:%S'
    # 创建日志格式
    formatter = ColoredFormatter('%(asctime)s - %(levelname)s - %(message)s [%(pathname)s:%(lineno)d]', datefmt=date_format)

    # 创建控制台处理器并设置格式
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 创建文件处理器并设置格式
    t = datetime.datetime.now()

    file_handler = logging.FileHandler(os.path.join(RUNTIME_PATH.joinpath("logs"), f"log_{t.strftime('%Y-%m-%d-%H')}.log"))

    # 创建文件处理器并设置格式（文件日志不需要颜色）
    file_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s [%(pathname)s:%(lineno)d]',
        datefmt=date_format
    )
    file_handler.setFormatter(file_formatter)

    # 将处理器添加到日志记录器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

logx = setup_logger()

# 示例使用
if __name__ == "__main__":
    logx.info("消息")
    logx.error("错误")
    logx.warning("警告")
