from act.facades.Detect.Common.BackDetect import BackDetect
from act.facades.Detect.MainWindowDetect import MainWindowDetect
from act.facades.Emulator.Emulator import UpdateSnapShot, Click, ConnectEmulator
from act.facades.Logx.Logx import logx


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