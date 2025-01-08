import datetime

from loguru import logger
import os
from facades.Constant.Constant import RUNTIME_PATH


class Logx:
    def __init__(self, log_level) -> None:
        # 自定义格式化器
        def custom_format(level):

            # 绿色：32，红色：31，黄色：33，蓝色：34，淡蓝色：36，清除：0
            if level == 'INFO':
                return '\x1b[32m{{time:yyyy-MM-dd HH:mm:s}} \x1b[36 Clover \x1b[32m{level:^7}\x1b[0m| {message} file:{file} line:{line}\n'
            if level == 'ERROR':
                return '\x1b[32m{{time:yyyy-MM-dd HH:mm:s}} \x1b[36 Clover \x1b[31m{level:^7}\x1b[0m| {message} file:{file} line:{line}\n'
            if level == 'DEBUG':
                return '\x1b[32m{{time:yyyy-MM-dd HH:mm:s}} \x1b[36 Clover \x1b[0m{level:^7}| {message}\n'
            if level == 'WARNING':
                return '\x1b[32m{{time:yyyy-MM-dd HH:mm:s}} \x1b[36 Clover \x1b[33m{level:^7}\x1b[0m| {message} file:{file} line:{line}\n'
            return     '\x1b[32m{{time:yyyy-MM-dd HH:mm:s}} \x1b[36 Clover \x1b[31m{level:^7}| {message} file:{file} line:{line}\n'

        logger.remove()
        def fileRecord(record):
            return f"{record['time']:YYYY-MM-DD HH:mm:ss} | {record['level']} | {record['file'].path}:{record['line']} - {record['message']}\n"

        def consoleRecord(record):
            tagStart = ("<green>", "</green>")
            if record['level'].name == "ERROR":
                tagStart = ("<red>", "</red>")
            timeToStr = record['time'].strftime("%Y-%m-%d %H:%M:%S")
            return f"{tagStart[0]}{timeToStr} | {record['level']} | {record['file'].path}:{record['line']} - {record['message']}\n{tagStart[1]}"

        # 添加文件日志记录器
        logger.add(
            os.path.join(RUNTIME_PATH.joinpath("logs"), 'log_{time:YYYY-MM-dd}.log'),
            level=log_level,
            colorize=True,
            format=fileRecord,
            catch=True,
            retention='1 week',
        )


        # 添加控制台日志记录器
        logger.add(
            lambda msg: print(msg, end=''),
            level=log_level,
            colorize=True,
            format=consoleRecord,
            catch=True,
        )

def info(msg):
    Logx("INFO")
    logger.info(msg)

def error(msg):
    Logx("ERROR")
    logger.error(msg)

# 示例使用
if __name__ == "__main__":
    info("消息")
    error("错误")
