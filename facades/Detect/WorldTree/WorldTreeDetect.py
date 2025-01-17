import glob
import os
import time
from collections import Counter

import cv2
from airtest.core.api import click

from facades.Constant.Constant import IMG_PATH
from facades.Detect.DetectLog import matchResult

from facades.Emulator.Emulator import GetSnapShot
from facades.Img.ImgSearch import imgSearch, imgMultipleResultSearch, imgSearchArea
from facades.Logx.Logx import logx
from facades.Ocr.MyCnocr import MyCnocr

"""
世界树，死境难度。
避战流派只打奇遇而且只会选第一个选项
"""
class WorldTreeDetect:
    memeryOf = []
    def __init__(self):
        # 探索等级
        self.lv = 0
        # 露水数量
        self.dew = 0

    @matchResult
    def isInWorldTreeMainWindow(self):
        """
        在世界树探索bata2.0页面
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("worldTreeBata.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"世界树bata2.0","pot":pot},ok

    @matchResult
    def isInWorldTreeDifficultySelectWindow(self):
        """
        选择难度
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("difficulty.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"选择难度","pot":pot},ok

    def getLever(self):
        """
        获取当前世界树等级
        :return:
        """
        # 截取指定位置
        dewXY = GetSnapShot().img
        dewXY = dewXY[490:545, 824:1195]
        res = MyCnocr.ocrNum(img=dewXY)
        lv = 0
        for roc in res:
            if "lv" in roc["text"]:
                roc["text"] = roc["text"].replace('lv.', '')
                roc["text"] = roc["text"].replace('l', '1')

                lv = int(roc["text"])
        self.lv = lv
        return lv

    def updateDew(self):
        """
        更新露水数量
        :return:
        """
        dewXY = GetSnapShot().img
        # 截取指定位置
        dewXY = dewXY[43:80, 960:1150]
        res = MyCnocr.ocrNum(img=dewXY)

        text = [item["text"] for item in res]
        text = ''.join(text)

        self.dew = text.replace("露水数量", "")

        return self.dew
    def hasBizarreCard(self) :
        """
        是否存在奇遇卡片可选
        一共三个位置，同时匹配
        :return:
        """

        def matchCards():
            cardRoi = [[293, 565, 200, 40], [555, 565, 200, 40], [800, 565, 200, 40]]
            path = ['l', 'm', 'r']

            result = []
            # 第一个位置要是一个都没有就直接返回 False
            for i, roi in enumerate(cardRoi):
                # 定义目录路径
                directory = f"{IMG_PATH.joinpath(f'Main/worldTree/cards/{path[i]}')}"

                # 使用 glob 读取目录下的 .png 文件
                png_files = glob.glob(os.path.join(directory, "*.png"))
                for file in png_files:
                    tempImg = cv2.imread(file)

                    pots, ok = imgSearchArea(GetSnapShot().img, tempImg, roi, 0.8)
                    if ok:
                        fName = file.split('/')[-1].split('.')[0]
                        result.append({"pot": (roi[0], roi[1]), "name": fName})
                        # 找到了就直接返回
                        break

            return result

        imgWithRoi = matchCards()
        # 没有匹配结果直接返回
        if len(imgWithRoi) == 0:
            return {}, False

        logx.info("原始识别结果")
        logx.info([item['name'] for item in imgWithRoi])

        cards = []

        nb = []
        eb = []
        # 开始组装卡片, 战斗类的排到最后面
        for img in imgWithRoi:
            # 创建映射表，删除所有数字
            translation_table = str.maketrans("", "", "0123456789")
            # 使用 translate 删除数字
            name = img['name'].translate(translation_table)

            if name == '普通战斗':
                nb.append(img)
            elif name == '精英战斗':
                eb.append(img)
            else:
                cards.append(img)

        cards = cards+ nb + eb
        logx.info("排序点击后的结果")
        logx.info([item['name'] for item in cards])

        self.memeryOf.append(''.join([item['name'] for item in cards]))

        if len(self.memeryOf) > 3:
            self.memeryOf.pop(-1)

        # 加入选择卡片的时候卡住了连续都是一样的卡片，则把三个坐标都点一遍
        counter = Counter(self.memeryOf)
        if counter[''.join([item['name'] for item in cards])] >=3:
            logx.info("选择卡片卡住了，正在处理")
            for roi in cards:
                click(roi['pot'])
                time.sleep(0.3)
            # 处理完接下来就不用返回给上面了
            return cards[0], False

        return cards[0], True

    @matchResult
    def isInWorldTreeEndWindow(self) :
        """
        探索结束
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("worldTreeEnd__556_55_164_40__506_5_264_140.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"探索结束","pot":pot},ok

    @matchResult
    def isInAdventureListWindow(self):
        """
        冒险之旅窗口
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("adventure").joinpath("adventureList__96_23_93_22__46_0_193_95.png")
        mainWindow = cv2.imread(f"{path}")
        pots, ok  = imgSearchArea(GetSnapShot().img, mainWindow, [96, 23, 93, 22])
        if ok:
            pot = pots[0]
        else:
            pot = (0,0)
        return {"name":"冒险之旅","pot":pot},ok
    @matchResult
    def hasWorldTreeButton(self):
        """
        是否有世界树按钮
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("adventure").joinpath("worldTree.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"世界树","pot":pot},ok
    @matchResult
    def searchStartWorldTreeAdvButton(self):
        """
        搜索是世界树开始冒险按钮
        :return:
        """
        startWorldTree = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("startWorldTreeAdventure.png")
        startWorldTree = cv2.imread(f"{startWorldTree}")
        pot, ok  = imgSearch(GetSnapShot().img, startWorldTree)
        return {"name":"世界树「开始冒险」","pot":pot},ok

    @matchResult
    def isInMainWindow(self):
        """
        游戏主页面
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("adventure").joinpath("adventure.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"游戏主界面ui","pot":pot},ok

    @matchResult
    def isInSelectYourBlessing(self):
        """
        选择你的祝福
        1 提升4点速度降低5%防御
        2 获得50点露水
        3 回复6%生命2会合降低10%暴伤
        4 提升1.5%攻防生命
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("WorldTree").joinpath("blessing__1036_239_45_89__986_189_145_189.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"选择你的祝福","pot":pot},ok

    @matchResult
    def canSeeDew(self):
        """
        露水
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("dewNum_939_49_16_20_889_0_116_119.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"露水数量","pot":pot},ok
    @matchResult
    def hasTopLeverButton(self):
        """
        绝境难度按钮
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("go__1122_503_54_23__1072_453_154_123.png")
        path = f"{path}"
        path = path.encode('utf-8').decode('utf-8')
        topLever = cv2.imread(f"{path}")
        pots,ok = imgMultipleResultSearch(GetSnapShot().img, topLever)
        # 去除相差小于10的

        if ok :
            pot = pots[-1]
        else:
            pot = (0,0)
        # pot, ok  = 1imgSearch(GetSnapShot().img, topLever)
        return {"name":"死境难度","pot":pot},ok
    @matchResult
    def isInStartPerform(self):
        """
        开始表演
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("startPerform__1047_647_119_29__997_597_219_123.png")
        topLever = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, topLever)
        return {"name":"开始表演","pot":pot},ok
    @matchResult
    def isInworldTreeCardWindow(self):
        """
        世界树游戏中
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("inGame.png")
        inGame = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, inGame)
        return {"name":"世界树探索中","pot":pot},ok

    @matchResult
    def isLoading(self):
        """
        正在加载
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("loading__867_579_343_97__817_529_443_191.png")
        inGame = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, inGame)
        return {"name":"正在加载...","pot":pot},ok
    @matchResult
    def selectConfirm2(self):
        """
        确认选择
        Returns:

        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("selectConfirm2__606_650_69_31__556_600_169_120.png")
        selectBlessing = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, selectBlessing)
        return {"name":"确认选择2","pot":pot},ok
    @matchResult
    def selectConfirm1(self):
        """
        确认选择
        Returns:

        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("selectConfirm1__606_651_68_29__556_601_168_119.png")
        selectBlessing = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, selectBlessing)
        return {"name":"确认选择1","pot":pot},ok

    @matchResult
    def hasEventConfirmButton(self):
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("selectEvent__968_218_47_24__918_168_147_124.png")
        selectBlessing = cv2.imread(f"{path}")
        pot, ok  = imgMultipleResultSearch(GetSnapShot().img, selectBlessing)
        return {"name":f"遭遇事件选项：{len(pot)} 个","pot":pot},ok

    @matchResult
    def hasEndBuyButton(self):
        """
        兔子商店-结束购买
        Returns:

        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("endBuy__905_603_105_24__855_553_205_124.png")
        endBuy = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, endBuy)
        return {"name":"结束购买","pot":pot},ok

    @matchResult
    def getItems(self):
        """
        获得道具
        Returns:
        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("getItems__497_78_284_69__447_28_384_169.png")
        items = cv2.imread(f"{path}")
        pots,ok = imgSearch(GetSnapShot().img, items)
        return {"name":"获得道具","pot":pots},ok

    @matchResult
    def giveUpItem(self):
        """
        放弃奖励
        Returns:
        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("giveUpItem__586_580_109_27__536_530_209_127.png")
        items = cv2.imread(f"{path}")
        pots,ok = imgSearch(GetSnapShot().img, items)
        return {"name":"放弃奖励","pot":pots},ok

    @matchResult
    def wealthCard(self):
        """
        赠礼
        Returns:
        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("wealth__613_194_55_27__563_144_155_127.png")
        items = cv2.imread(f"{path}")
        pots,ok = imgSearch(GetSnapShot().img, items)
        return {"name":"选择赠礼-财富","pot":pots},ok

    @matchResult
    def survivalCard(self):
        """
        赠礼
        Returns:

        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("survival__1034_195_56_25__984_145_156_125.png")
        items = cv2.imread(f"{path}")
        pots,ok = imgSearch(GetSnapShot().img, items)
        return {"name":"选择赠礼-生存","pot":pots},ok
    @matchResult
    def lvPlusCard(self):
        """
        选择赠礼
        Returns:

        """

        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("lvplus__194_193_55_28__144_143_155_128.png")
        items = cv2.imread(f"{path}")
        pots,ok = imgSearch(GetSnapShot().img, items)
        return {"name":"选择赠礼-远见","pot":pots},ok

    def hasExit(self):
        """
        点击空白区域退出
        Returns:
        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("exit__530_652_234_23__480_602_334_118.png")
        items = cv2.imread(f"{path}")
        pots,ok = imgSearchArea(GetSnapShot().img, items, [530,652,234,23])
        if ok:
            pot = pots[-1]
        else:
            pot = (0,0)
        return {"name":"点击空白区域退出","pot":pot},ok