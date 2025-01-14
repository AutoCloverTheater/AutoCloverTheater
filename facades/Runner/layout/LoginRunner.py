import time

from airtest.core.api import click, text

from facades.Configs.Config import Config
from facades.Detect.MainWindowDetect import MainWindowDetect
from facades.Emulator.Emulator import UpdateSnapShot, ConnectEmulator
from facades.Logx import Logx


def Login():
    main = MainWindowDetect()

    # 返回runner是否匹配到了页面
    matchResult = True

    times = 0
    while 1 :
        if times >= 3:
            matchResult = False
            break
        # 更新截图
        UpdateSnapShot()
        gameUi, ok = main.isInGameUiWindow()
        if ok:
            Logx.info("识别到游戏主页面登录流程结束")
            break
        # 登录页面-需要登录
        loginNeedAccountAndPass, isNeedLoginOk = main.isNeedLogin()
        if isNeedLoginOk:
            Logx.info(f"识别到页面:{loginNeedAccountAndPass['name']}")
            Logx.info(f"输入账号")
            accountInput = (460, 210)
            click(accountInput)
            time.sleep(1)
            text(Config("app").get("account"))
            Logx.info(f"输入账号完毕")
            passwordInput = (460, 280)
            Logx.info(f"输入密码")
            click(passwordInput)
            time.sleep(1)
            text(Config("app").get("password"))
            Logx.info(f"输入账号完毕")
            # 等待登录完成
            break
        # 登录页面-不需要登录
        isNotNeedLoginResp, ok = main.isNotNeedLogin()
        if ok and not isNeedLoginOk:
            Logx.info(f"识别到页面:{isNotNeedLoginResp['name']}")
            main.click(isNotNeedLoginResp['pot'])
            Logx.info(f"点击登录")
            continue
        # 每日签到
        sign, ok = main.isInDailySignWindow()
        if ok:
            Logx.info(f"识别到页面:{sign['name']}")
            click(sign['pot'])
            continue
        # 主页面
        isMainWindowResp, ok = main.isMainWindow()
        if ok:
            Logx.info(f"开始登录流程")
            # y坐标增加60
            clickXy = (isMainWindowResp['pot'][0], isMainWindowResp['pot'][1] + 60)
            click(clickXy)
            Logx.info(f"预测下一个页面，点击登录")
            continue
        times+=1

    return matchResult

if __name__ == '__main__':
    ConnectEmulator()
    Login()