import cv2
import numpy
from PIL import Image
from facades.Constant.Constant import IMG_PATH
from facades.Detect.DetectLog import matchResult
import imagehash

from facades.Emulator.Emulator import GetSnapShot
from facades.Img.ImgColor import imgGetColor
from facades.Img.ImgSearch import imgSearch, imgMultipleResultSearch
from facades.Logx.Logx import logx
from facades.Ocr.MyCnocr import MyCnocr

"""
世界树，死境难度。
避战流派只打奇遇而且只会选第一个选项
"""
class WorldTreeDetect:

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
        return {"name":"世界树bata2.0","pot":pot},ok

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
                lv = int(roc["text"].replace('lv.', ''))
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
        :return:
        """

        img = GetSnapShot().img
        y, x, _ = img.shape
        cardxy = img[565:595, :]

        # 将掩码外的像素设置为黑色
        result = imgGetColor(img=cardxy, low="AB9F87", top="F9E9CF")

        cv2.imwrite("result.png", result)
        result1  = result
        result2 = result
        result3 = result
        # 保存图片
        l = result1[0:28,322:406]
        m = result2[0:28,544:704]
        r = result3[0:28,840:928]

        lname = imagehash.average_hash(Image.fromarray(l))
        mname = imagehash.average_hash(Image.fromarray(m))
        rname = imagehash.average_hash(Image.fromarray(r))

        lp = IMG_PATH.joinpath("Main/worldTree/cards").joinpath(f"l/{lname}.png")
        mp = IMG_PATH.joinpath("Main/worldTree/cards").joinpath(f"m/{mname}.png")
        rp = IMG_PATH.joinpath("Main/worldTree/cards").joinpath(f"r/{rname}.png")

        res1 = cv2.imwrite(f"{lp}",l)
        res2 = cv2.imwrite(f"{mp}",m)
        res3 = cv2.imwrite(f"{rp}",r)
        logx.info(f"保存结果 {res1},{res2},{res3}\n")

        # res = MyCnocr.bizarreCardOcr(img=result1)
        return {}, True

    @matchResult
    def isInWorldTreeEndWindow(self) :
        """
        世界树探索结束窗口
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTreeEnd.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
        return {"name":"探索结束","pot":pot},ok

    @matchResult
    def isInWorldTreeBattleReadyWindow(self):
        """
        世界树探索战斗准备窗口
        :return:
        """
        pass

    @matchResult
    def isInAdventureListWindow(self):
        """
        冒险列表窗口
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("adventure").joinpath("adventureList.png")
        mainWindow = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, mainWindow)
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

    def isInStartPerform(self):
        """
        开始表演
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("startPerform_1039_644_133_38__989_594_233_126.png")
        topLever = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, topLever)
        return {"name":"开始表演","pot":pot},ok

    def isInworldTreeCardWindow(self):
        """
        世界树游戏中
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("inGame.png")
        inGame = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, inGame)
        return {"name":"世界树游戏中","pot":pot},ok

    def isLoading(self):
        """
        正在加载
        :return:
        """
        path = IMG_PATH.joinpath("lag").joinpath("loading.png")
        inGame = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, inGame)
        return {"name":"正在加载...","pot":pot},ok

    def selectBlessing(self):
        """
        确认选择祝福
        Returns:

        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("selectBlessing__606_651_68_29__556_601_168_119.png")
        selectBlessing = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, selectBlessing)
        return {"name":"确认选择祝福","pot":pot},ok

    def hasEventConfirmButton(self):
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("selecEvent__968_218_47_24__918_168_147_124.png")
        selectBlessing = cv2.imread(f"{path}")
        pot, ok  = imgMultipleResultSearch(GetSnapShot().img, selectBlessing)
        return {"name":f"遭遇事件选项：{len(pot)} 个","pot":pot},ok

    def hasEndBuyButton(self):
        """
        兔子商店-结束购买
        Returns:

        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("endBuy__905_603_105_24__855_553_205_124.png")
        endBuy = cv2.imread(f"{path}")
        pot, ok  = imgSearch(GetSnapShot().img, endBuy)
        return {"name":"结束购买","pot":pot},ok