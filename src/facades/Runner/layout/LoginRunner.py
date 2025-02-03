
from src.facades.Configs.Config import Config
from src.facades.Detect.Common.ErrorDetect import ErrorDetect
from src.facades.Detect.MainWindowDetect import MainWindowDetect
from src.facades.Emulator.Emulator import UpdateSnapShot, ConnectEmulator, Click, Text, AppCurrent, AppStart
from src.facades.Logx.Logx import logx
from src.facades.Runner.core.Limit import error_function


def BeforeLogin():
    if not AppCurrent():
        AppStart()
        logx.info(f"启动应用")

@error_function
def Login():
    BeforeLogin()

    main = MainWindowDetect()
    errors = ErrorDetect()

    # 返回runner是否匹配到了页面
    matchResult = True

    times = 0
    while 1 :
        if times >= 7:
            matchResult = False
            logx.warning("跳过登录")
            break
        # 更新截图
        UpdateSnapShot()
        # app启动中
        _,ok = main.appStart()
        if ok:
            times = 0
            continue
        # 加载中
        resp, ok = errors.loading()
        if ok:
            times = 0
            continue
        # 更新内容
        resp,ok = main.dlc()
        if ok:
            Click(resp['pot'])
            times = 0
            continue
        # 服务器维护中
        _,ok = errors.gameUpdating()
        if ok:
            break
        # 勾选隐私协议
        resp,ok = main.userAgreementBotSelected()
        if ok:
            Click(resp['pot'])
            times = 0
            continue
        gameUi, ok = main.isInGameUiWindow()
        if ok:
            logx.info("识别到游戏主页面登录流程结束")
            break
        # 登录页面-需要输入账号密码
        pleaseInputAccount, pleaseInput = main.pleaseInputAccount()
        if pleaseInput:
            logx.info(f"输入账号")
            accountInput = (460, 210)
            Click(accountInput)
            Text(f'{Config("app").get("account")}')
            logx.info(f"输入账号完毕")
            passwordInput = (460, 280)
            logx.info(f"输入密码")
            Click(passwordInput)
            Text(f'{Config("app").get("password")}')
            logx.info(f"输入账号完毕")
            # 等待登录完成
            times = 0
            continue
        # 不需要输入账号密码或者已经输入了
        login, ok = main.hasLoginButton()
        if ok and not pleaseInput:
            logx.info(f"点击登录{login}")
            Click(login['pot'])
        DailySignReward,ok = main.isInDailySignRewardWindow()
        if ok:
            logx.info(f"准备关闭签到页面")
            Click(DailySignReward['pot'])
        # 每日签到
        sign, ok = main.isInDailySignWindow()
        if ok:
            # y轴向下偏移200像素点
            pot = (sign['pot'][0], sign['pot'][1] + 400)
            Click(pot)
            times = 0
            continue
        # 登录主页面
        isMainWindowResp, ok = main.needLogin()
        if ok:
            # y坐标增加60
            clickXy = (isMainWindowResp['pot'][0], isMainWindowResp['pot'][1] + 60)
            Click(clickXy)
            times = 0
            continue
        times+=1
        logx.info("未知页面")

    return matchResult

if __name__ == '__main__':
    ConnectEmulator()
    Login()