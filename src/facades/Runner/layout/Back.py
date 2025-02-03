from src.facades.Detect.Common.BackDetect import BackDetect
from src.facades.Detect.MainWindowDetect import MainWindowDetect
from src.facades.Emulator.Emulator import UpdateSnapShot, Click, ConnectEmulator
from src.facades.Logx.Logx import logx


def backMain():
    back = BackDetect()
    main = MainWindowDetect()

    times = 12
    while True:
        if times <= 0:
            logx.info("返回上一页失败")
            break

        UpdateSnapShot()
        resp, ok = main.isInGameUiWindow()
        if ok:
            break

        resp, ok = back.findLastPageButton()
        if ok:
            Click(resp['pot'], 0.3)
            continue

        times-= 1
    return

if __name__ == '__main__':
    ConnectEmulator()
    backMain()