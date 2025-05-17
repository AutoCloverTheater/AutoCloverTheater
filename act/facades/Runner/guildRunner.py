from act.facades.Configs.Config import Config
from act.facades.Detect.Guild.GuildDetect import GuildDetect
from act.facades.Emulator.Emulator import ConnectEmulator, UpdateSnapShot, Click
from act.facades.Logx.Logx import logx
from act.facades.Runner.layout.Back import backMain


def beforeInGuild():
    guild = GuildDetect()
    times = 12
    while True:
        if times <= 0:
            break
        UpdateSnapShot()
        resp,ok = guild.hasGuildButton()
        if ok:
            Click(resp['pot'], 0.3)
            break

        times -=1
    return

def donate():
    guild = GuildDetect()
    times = 12

    while True:
        if times <= 0:
            logx.info("退出捐献")
            break
        UpdateSnapShot()
        resp,ok = guild.hasDonate()
        if ok:
            Click(resp['pot'], 0.3)
            continue
        resp, ok2 = guild.donate()
        _, ok1 = guild.canDonate()
        if ok1:
            logx.info("达到捐献上限")
            if ok1 and ok2:
                # 退出回到工会大厅
                Click((0.9,0.5), 0.3)
            break
        ocrDonatedTimes = guild.ocrDonatedTimes()
        if ocrDonatedTimes >= Config("app.guildDonateLimit"):
            logx.info("达到捐献次数")
            break
        if not ok1 and ok2:
            Click(resp['pot'], 2)
            logx.info("捐献一次")
            continue
        times -= 1
    return

def getReward():
    guild = GuildDetect()
    times = 12
    while True:
        if times <= 0:
            logx.info("退出领取奖励")
            break
        UpdateSnapShot()
        resp, ok = guild.getItem()
        if ok:
            Click(resp['pot'], 0.3)
            continue
        resp, ok = guild.hasMeettingRoom()
        if ok:
            Click(resp['pot'], 0.3)
            continue
        resp,ok = guild.hasGuildRequestion()
        if ok:
            Click(resp['pot'], 0.3)
            continue
        _, inGetRewardWindow = guild.getReward()
        resp, ok1 = guild.canGetReward()
        if not ok1 and inGetRewardWindow:
            Click((0.9,0.5), 0.3)
            break
        if ok1:
            Click(resp['pot'], 0.3)
        resp, ok = guild.getReward()
        if ok1 and ok:
            Click(resp['pot'], 0.3)
            continue

        times -= 1
    return


if __name__ == '__main__':
    ConnectEmulator()
    beforeInGuild()
    donate()
    getReward()
    backMain()