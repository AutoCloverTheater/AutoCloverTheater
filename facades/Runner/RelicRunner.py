import time

import imagehash
from PIL import Image
from collections import Counter

from facades.Detect.Common.ErrorDetect import ErrorDetect
from facades.Detect.Common.FlashBattleDetect import FlashBattleDetect
from facades.Detect.Relic.RelicDetect import RelicDetect
from facades.Emulator.Emulator import UpdateSnapShot, ConnectEmulator, GetSnapShot, Click, Swipe
from facades.Logx.Logx import logx
from facades.Ocr.MyCnocr import MyCnocr
from facades.Runner.layout.AdventureRunner import FindAdventure
from facades.Runner.layout.LoginRunner import Login


TearCrystal = 0
def beforeRelic():
    relic = RelicDetect()
    fastBattle = FlashBattleDetect()
    times = 0
    while True:
        if times >= 12:
            logx.warning("跳过遗迹准备阶段")
            break
        UpdateSnapShot()
        _, ok = relic.isInRelicGame()
        if ok:
            break

        go,ok = fastBattle.startPerform()
        if ok:
            Click(go['pot'])
            times = 0
            continue
        settingMap, ok = relic.hasSettingMap()
        if ok:
            Click(settingMap['pot'])
            times = 0
        settingRank, ok = relic.hasSettingRank()
        if ok:
            Click(settingRank['pot'])
            times = 0
        start,ok = relic.hasGoExplore()
        if ok:
            Click(start['pot'])
            times = 0
            continue
        # 加载
        _,ok = fastBattle.isLoading()
        if ok:
            time.sleep(0.1)
            times = 0
            continue
        times += 1

def _findNextNode():
    relic  = RelicDetect()
    UpdateSnapShot()
    # 在遗迹内
    _, inGame = relic.isInRelicGame()
    # 探索点
    resp, ok = relic.eventPoint()
    if ok and inGame:
        Click(resp['pot'])
        time.sleep(5)
        return resp
    maps = [
        {
            "name":"右上角",
            "point":[(0.5,0.5),(0.1,0.9)],
        },{
            "name": "左上角",
            "point": [(0.5,0.5),(0.9,0.9)],
        },{
            "name": "右下角",
            "point": [(0.5,0.5),(0.1,0.1)],
        },{
            "name": "左下角",
            "point": [(0.5,0.5),(0.9,0.1)],
        }
    ]
    stop = False
    for item in maps:
        if stop:
            break
        name = item['name']
        point = item['point']
        # 在遗迹探索中
        _, ok = relic.isInRelicGame()
        if not ok:
            break

        # 视角复位
        UpdateSnapShot()
        resp, ok = relic.location()
        if ok:
            Click(resp['pot'])
            time.sleep(0.2)
        else:
            logx.warning("没有找到复位按钮")
            return resp

        _, inBoss = relic.killedBoss()
        if inBoss:
            break

        for i in range(6):
            Swipe(point[0], point[1])
            UpdateSnapShot()
            # 在遗迹内
            _, inGame = relic.isInRelicGame()
            if not inGame:
                break
            logx.info(f"{name}寻找第 {i + 1} 次")

            # 探索点
            resp, ok = relic.eventPoint()
            if ok:
                Click(resp['pot'])
                UpdateSnapShot()
                # 在遗迹内
                _, inGame = relic.isInRelicGame()
                if not inGame:
                    break
                # 已经在boss点位
                _, inBoss = relic.killedBoss()
                if inBoss:
                    break
                _,ok = relic.reLocation()
                if ok :
                    stop = False
                    break
                else:
                    time.sleep(5)
                    stop = True
                    break

    # 视角复位
    UpdateSnapShot()
    resp, ok = relic.location()
    if ok:
        Click(resp['pot'])
        time.sleep(0.5)
    else:
        logx.warning("没有找到复位按钮")
        return resp

    return resp

def ErikaMoving():
    """
    艾丽卡移动中
    连续三帧相同，则艾丽卡移动结束
    :return:
    """
    # [41,6,159,146]
    fpsLimit = 2

    fps = []
    while True:
        UpdateSnapShot()
        img = GetSnapShot()
        Erika = img[6:6+146,41:41+159]

        hk = imagehash.average_hash(Image.fromarray(Erika))
        hk = f"{hk}"
        fps.append(hk)

        if len(fps) > fpsLimit:
            fps.pop(0)

        counts  = Counter(fps)
        if len(fps) == fpsLimit and len(counts) <= 1:
            logx.info("艾丽卡停止移动")
            break
        logx.info("艾丽卡移动中")


    return

def inRelic():
    global TearCrystal
    relic = RelicDetect()
    fastBattle = FlashBattleDetect()

    times = 0
    while True:
        if times >= 5:
            logx.warning("跳过遗迹冒险")
            break
        UpdateSnapShot()
        # 加载
        _,ok = fastBattle.isLoading()
        if ok:
            time.sleep(0.1)
            times = 0
            continue
        # 战斗
        resp, ok = fastBattle.exeFlashBattle()
        if ok:
            Click(resp['pot'])
            times = 0
            time.sleep(0.2)
            continue
        getItems, ok = relic.getItems()
        if ok:
            Click(getItems['pot'])
            times = 0
            continue
        # 在遗迹内
        _, inGame = relic.isInRelicGame()
        # 确认按钮
        confirmButton,ok = relic.hasConfirmButton()
        if ok and inGame:
            Click(confirmButton['pot'])
            time.sleep(0.2)
            times = 0
            continue
        hasSelectButton,ok =  relic.hasSelectButton()
        if ok:
            need = beforeClickSelect()
            logx.info(f"所需 {need}, 拥有 {TearCrystal}")
            if need > TearCrystal:
                Click((969 + 25, 322 + 12))
            else:
                Click(hasSelectButton['pot'])
            times = 0
            continue
        # 击杀boss了
        killedBoss, ok = relic.killedBoss()
        if ok:
            Click(killedBoss['pot'])
            time.sleep(0.2)
            times = 0
            continue
        explorationEnds,ok = relic.explorationEnds()
        if ok:
            Click(explorationEnds['pot'])
            time.sleep(1)
            break
        # 探索点
        resp, ok = relic.eventPoint()
        if ok and inGame:
            TearCrystal = beforeClickEventPoint()
            Click(resp['pot'])
            ErikaMoving()
            times = 0
            continue
        # 没有找到探索点，开始寻找下一个探索点
        if not ok and inGame:
            _findNextNode()
            ErikaMoving()
            times = 0
            continue
        times+= 1

def beforeClickEventPoint():
    """
    更新泪精数量
    Returns:
    [826,9,63,80]
    """
    roc = [825,28,61,44]

    img = GetSnapShot()
    img = img[roc[1]:roc[1]+roc[3],roc[0]:roc[0]+roc[2]]
    ocr = MyCnocr.ocrNum(img)

    num = 0
    if len(ocr):
        if ocr[0]['text'] != '':
         num = int(ocr[0]['text'])
    logx.info(f"更新泪精数量 {num}")
    return num

def beforeClickSelect():
    """
    识别所需泪精
    Returns:
    """
    roc = [761,227,35,35]

    img = GetSnapShot()
    img = img[roc[1]:roc[1]+roc[3],roc[0]:roc[0]+roc[2]]
    ocr = MyCnocr.ocrNum(img)

    num = 0
    if len(ocr):
        if ocr[0]['text'] != '':
         num = int(ocr[0]['text'])

    logx.info(f"所需泪精数量 {num}")
    return num


if __name__ == '__main__':
    ConnectEmulator()
    # relic = RelicDetect()
    # while True:
    #     UpdateSnapShot()
    #     res,r = relic.killedBoss()
    #     logx.info(r)

    #     TearCrystal = beforeClickEventPoint()
    #     logx.info(TearCrystal)


    def run():
        ConnectEmulator()
        Login()
        FindAdventure("hasRelicButton")
        beforeRelic()
        inRelic()

    for i in range(1):
        run()
        resp,ok = ErrorDetect().error()
        if ok :
            Click(resp['pot'])
            run()