import time

from airtest.core.api import click, text

from facades.Configs.Config import Config
from facades.Detect.MainWindowDetect import MainWindowDetect
from facades.Emulator.Emulator import UpdateSnapShot, ConnectEmulator
from facades.Logx.Logx import logx


def Login():
    main = MainWindowDetect()

    # 返回runner是否匹配到了页面
    matchResult = True

    times = 0
    while 1 :
        if times >= 3:
            matchResult = False
            logx.warning("跳过登录")
            break
        # 更新截图
        UpdateSnapShot()
        gameUi, ok = main.isInGameUiWindow()
        if ok:
            logx.info("识别到游戏主页面登录流程结束")
            break
        # 登录页面-需要登录
        loginNeedAccountAndPass, isNeedLoginOk = main.isNeedLogin()
        if isNeedLoginOk:
            logx.info(f"识别到页面:{loginNeedAccountAndPass['name']}")
            logx.info(f"输入账号")
            accountInput = (460, 210)
            click(accountInput)
            time.sleep(1)
            text(f'{Config("app").get("account")}')
            logx.info(f"输入账号完毕")
            passwordInput = (460, 280)
            logx.info(f"输入密码")
            click(passwordInput)
            time.sleep(1)
            text(f'{Config("app").get("password")}')
            logx.info(f"输入账号完毕")
            # 等待登录完成
            break
        # 登录页面-不需要登录
        isNotNeedLoginResp, ok = main.isNotNeedLogin()
        if ok and not isNeedLoginOk:
            logx.info(f"点击登录")
            click(isNotNeedLoginResp['pot'])
            continue
        DailySignReward,ok = main.isInDailySignRewardWindow()
        if ok:
            logx.info(f"准备关闭签到页面")
            click(DailySignReward['pot'])
        # 每日签到
        sign, ok = main.isInDailySignWindow()
        if ok:
            # y轴向下偏移200像素点
            pot = (sign['pot'][0], sign['pot'][1] + 400)
            click(pot)
            continue
        # 主页面
        isMainWindowResp, ok = main.isMainWindow()
        if ok:

            logx.info(f"开始登录流程")
            # y坐标增加60
            clickXy = (isMainWindowResp['pot'][0], isMainWindowResp['pot'][1] + 60)
            click(clickXy)
            logx.info(f"预测下一个页面，点击登录")
            continue
        times+=1

    return matchResult

if __name__ == '__main__':
    ConnectEmulator()
    Login()