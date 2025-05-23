import glob
import os
import string
import time
from ftplib import print_line

import cv2
from paddlex import create_pipeline
from act.facades.Constant.Constant import IMG_PATH
from act.facades.Detect.DetectLog import matchResult
from act.facades.Emulator.Emulator import GetSnapShot, UpdateSnapShot, ConnectEmulator, Pipe
from act.facades.Img.ImgRead import MyImread
from act.facades.Img.ImgSearch import imgSearch, imgMultipleResultSearch, imgSearchArea
from act.facades.Logx.Logx import logx
from act.facades.tool import cutImgByRoi

"""
世界树，死境难度。
避战流派只打奇遇而且只会选第一个选项
"""
class WorldTreeDetect:
    memeryOf = []
    pipeline = create_pipeline(pipeline="OCR")
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
        mainWindow = MyImread(path)
        pot, ok  = imgSearch(GetSnapShot(), mainWindow)
        return {"name":"世界树bata2.0","pot":pot},ok

    @matchResult
    def isInWorldTreeDifficultySelectWindow(self):
        """
        选择难度
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("difficulty.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearch(GetSnapShot(), mainWindow)
        return {"name":"选择难度","pot":pot},ok

    def getLever(self):
        """
        获取当前世界树等级
        :return:
        """
        # 截取指定位置
        # dewXY = GetSnapShot()
        # dewXY = dewXY[490:545, 824:1195]
        # res = MyCnocr.ocrNum(img=dewXY)
        lv = 0
        # for roc in res:
        #     if "lv" in roc["text"]:
        #         roc["text"] = roc["text"].replace('lv.', '')
        #         roc["text"] = roc["text"].replace('l', '1')
        #
        #         lv = int(roc["text"])
        # self.lv = lv
        return lv

    def updateDew(self):
        """
        更新露水数量
        :return:
        """
        # dewXY = GetSnapShot()
        # 截取指定位置
        # dewXY = dewXY[43:80, 960:1150]
        # res = MyCnocr.ocrNum(img=dewXY)

        # self.dew = text.replace("露水数量", "")

        return self.dew
    def hasBizarreCardV2(self):
        """
        是否存在奇遇卡片可选
        一共三个位置，同时匹配
        :return:
        """
        def  matchCards():
            roi = (257, 560, 800, 40)
            img = cutImgByRoi(GetSnapShot(), roi)
            output = self.pipeline.predict(
                input=img,
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
                use_textline_orientation=False,
                text_rec_score_thresh=0.8
            )
            x,y,_,_ = roi
            iCards = []

            def is_chinese(char) -> bool:
                return '\u4e00' <= char <= '\u9fff'

            reRoc = False
            for res in output:
                if reRoc:
                    break

                for  poly in res["rec_texts"]:
                    for s in poly:
                        if is_chinese(s):
                            continue
                        else:
                            reRoc = True
                            break
                for k,poly in enumerate(res["rec_polys"]):
                        x1, y1, *rest = poly[0]
                        # 小图上的四点坐标我们只要取第一个坐标就好
                        card = {
                            "name": res["rec_texts"][k],
                            "pot": (float(x + x1), float(y + y1)),
                        }
                        iCards.append(card)

            return  iCards, reRoc

        cards,ok = matchCards()

        # 排序所有跟战斗有关的卡都排到最后面
        nameP = [i["name"] for i in cards]
        logx.info("卡牌排序前："+ ".".join(nameP))

        tCards = []
        for k,i in enumerate(cards):
            if "战" in i["name"]:
                tCards = tCards + [i]
            else:
                tCards = [i] + tCards
        nameAf = [i["name"] for i in tCards]
        logx.info("卡牌排序后：" + ".".join(nameAf))

        return tCards, len(cards) == 3


    def hasBizarreCard(self) :
        """
        是否存在奇遇卡片可选
        一共三个位置，同时匹配
        :return:
        """

        def matchCards():
            cardRoi = [[257,560,214,34], [475,512,300,130], [800, 565, 200, 40]]
            path = ['l', 'm', 'r']

            result = []
            # 第一个位置要是一个都没有就直接返回 False
            for i, roi in enumerate(cardRoi):
                # 定义目录路径
                directory = f"{IMG_PATH.joinpath(f'Main/worldTree/cards/{path[i]}')}"

                # 使用 glob 读取目录下的 .png 文件
                png_files = glob.glob(os.path.join(directory, "*.png"))
                for file in png_files:
                    tempImg = MyImread(file)

                    pots, ok = imgSearchArea(GetSnapShot(), tempImg, roi, 0.8)
                    if ok:
                        fName = file.split('/')[-1].split('.')[0]
                        result.append({"pot": (roi[0], roi[1]), "name": fName})
                        logx.debug(f"{fName} path{path[i]} 匹配成功")
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
        logx.debug(cards)

        if 3 > len(cards) > 1:
            logx.exception("卡片长度异常")
            raise Exception("卡片长度异常")

        # logx.info([item['name'] for item in cards])
        #
        # self.memeryOf.append(''.join([item['name'] for item in cards]))
        #
        # if len(self.memeryOf) > 3:
        #     self.memeryOf.pop(-1)
        #
        # # 假如选择卡片的时候卡住了连续都是一样的卡片，则把三个坐标都点一遍
        # counter = Counter(self.memeryOf)
        #
        # logx.info(f"{self.memeryOf}")
        #
        # if counter[''.join([item['name'] for item in cards])] >=3:
        #     logx.info("选择卡片卡住了，正在处理")
        #     for roi in cards:
        #         time.sleep(1)
        #         Click(roi['pot'], 1)
        #     # 处理完接下来就不用返回给上面了
        #     return cards[0], False

        return cards, len(cards) > 0

    @matchResult
    def isInWorldTreeEndWindow(self) :
        """
        探索结束
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("worldTreeEnd__556_55_164_40__506_5_264_140.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearch(GetSnapShot(), mainWindow)
        return {"name":"探索结束","pot":pot},ok

    @matchResult
    def searchStartWorldTreeAdvButton(self):
        """
        搜索是世界树开始冒险按钮
        :return:
        """
        startWorldTree = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("startWorldTreeAdventure.png")
        startWorldTree = MyImread(f"{startWorldTree}")
        pot, ok  = imgSearch(GetSnapShot(), startWorldTree)
        return {"name":"世界树「开始冒险」","pot":pot},ok

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
        mainWindow = MyImread(path)
        pot, ok  = imgSearch(GetSnapShot(), mainWindow)
        return {"name":"选择你的祝福","pot":pot},ok

    @matchResult
    def canSeeDew(self):
        """
        露水
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("dewNum_939_49_16_20_889_0_116_119.png")
        mainWindow = MyImread(path)
        pot, ok  = imgSearch(GetSnapShot(), mainWindow)
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
        topLever = MyImread(path)
        pots,ok = imgMultipleResultSearch(GetSnapShot(), topLever)
        # 去除相差小于10的

        if ok :
            pot = pots[-1]
        else:
            pot = (0,0)
        # pot, ok  = 1imgSearch(GetSnapShot(), topLever)
        return {"name":"死境难度","pot":pot},ok
    @matchResult
    def isInStartPerform(self):
        """
        开始表演
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("startPerform__1047_647_119_29__997_597_219_123.png")
        topLever = MyImread(path)
        pot, ok  = imgSearch(GetSnapShot(), topLever)
        return {"name":"开始表演","pot":pot},ok
    @matchResult
    def isInworldTreeCardWindow(self):
        """
        世界树游戏中
        :return:
        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("inGame.png")
        inGame = MyImread(path)
        pot, ok  = imgSearch(GetSnapShot(), inGame)
        return {"name":"世界树探索中","pot":pot},ok

    @matchResult
    def hasOffset(self):
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("offset").joinpath("re__462_301_358_22__412_251_458_122.png")
        topLever = MyImread(path)
        pot, ok  = imgSearch(GetSnapShot(), topLever)
        return {"name":"偏移","pot":pot},ok

    @matchResult
    def selectConfirm2(self):
        """
        确认选择
        Returns:

        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("selectConfirm2__606_650_69_31__556_600_169_120.png")
        selectBlessing = MyImread(path)
        pot, ok  = imgSearch(GetSnapShot(), selectBlessing, 0.98)
        return {"name":"确认选择2","pot":pot},ok
    @matchResult
    def selectConfirm1(self):
        """
        确认选择
        Returns:

        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("selectConfirm1__606_651_68_29__556_601_168_119.png")
        selectBlessing = MyImread(path)
        pot, ok  = imgSearch(GetSnapShot(), selectBlessing, 0.98)
        return {"name":"确认选择1","pot":pot},ok

    @matchResult
    def hasEventConfirmButton(self):
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("selectEvent__968_218_47_24__918_168_147_124.png")
        selectBlessing = MyImread(path)
        pot, ok  = imgMultipleResultSearch(GetSnapShot(), selectBlessing)
        return {"name":f"遭遇事件选项：{len(pot)} 个","pot":pot},ok

    @matchResult
    def hasEndBuyButton(self):
        """
        兔子商店-结束购买
        Returns:

        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("endBuy__905_603_105_24__855_553_205_124.png")
        endBuy = MyImread(path)
        pot, ok  = imgSearch(GetSnapShot(), endBuy)
        return {"name":"结束购买","pot":pot},ok

    @matchResult
    def getItems(self):
        """
        获得道具
        Returns:
        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("getItems__497_78_284_69__447_28_384_169.png")
        items = MyImread(path)
        pots,ok = imgSearch(GetSnapShot(), items)
        return {"name":"获得道具","pot":pots},ok

    @matchResult
    def giveUpItem(self):
        """
        放弃奖励
        Returns:
        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("giveUpItem__586_580_109_27__536_530_209_127.png")
        items = MyImread(path)
        pots,ok = imgSearch(GetSnapShot(), items)
        return {"name":"放弃奖励","pot":pots},ok

    @matchResult
    def wealthCard(self):
        """
        赠礼
        Returns:
        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("wealth__613_194_55_27__563_144_155_127.png")
        items = MyImread(path)
        pots,ok = imgSearch(GetSnapShot(), items)
        return {"name":"选择赠礼-财富","pot":pots},ok

    @matchResult
    def survivalCard(self):
        """
        赠礼
        Returns:

        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("survival__1034_195_56_25__984_145_156_125.png")
        items = MyImread(path)
        pots,ok = imgSearch(GetSnapShot(), items)
        return {"name":"选择赠礼-生存","pot":pots},ok
    @matchResult
    def lvPlusCard(self):
        """
        选择赠礼
        Returns:

        """

        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("lvplus__194_193_55_28__144_143_155_128.png")
        items = MyImread(path)
        pots,ok = imgSearch(GetSnapShot(), items)
        return {"name":"选择赠礼-远见","pot":pots},ok

    def hasExit(self):
        """
        点击空白区域退出
        Returns:
        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("exit__530_652_234_23__480_602_334_118.png")
        items = MyImread(path)
        pots,ok = imgSearchArea(GetSnapShot(), items, [530,652,234,23])
        if ok:
            pot = pots[-1]
        else:
            pot = (0,0)
        return {"name":"点击空白区域退出","pot":pot},ok

    def isLeverMax(self):
        """
        本期探索等级是否已满
        Returns:

        """
        path = IMG_PATH.joinpath("Main/worldTree/max__830_491_53_26__780_441_153_126.png")
        items = MyImread(path)
        pots,ok = imgSearchArea(GetSnapShot(), items, [830,491,53,26])
        if ok:
            pot = pots[-1]
        else:
            pot = (0,0)
        return {"name":"点击空白区域退出","pot":pot},ok

    def reSelect(self):
        """
        当前路径不可用请重新选择
        """
        path = IMG_PATH.joinpath("Main/worldTree/reSelect__458_301_370_29__408_251_470_129.png")
        items = MyImread(path)
        pots,ok = imgSearchArea(GetSnapShot(), items, [458,289,364,70])
        pot = (0, 0)
        if ok:
            pot = pots[-1]
        return {"name":"当前路径不可用请重新选择","pot":pot},ok

    @matchResult
    def isLeverMaxInGame(self):
        """
        探索中的时候等级是否已经满了
        Returns:
        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("maxInGame__450_19_46_20__400_0_146_89.png")
        items = MyImread(path)
        pots,ok = imgSearchArea(GetSnapShot(), items, [450,19,46,20])
        if ok:
            pot = pots[-1]
        else:
            pot = (0,0)
        return {"name":"探索中的时候等级是否已经满了","pot":pot},ok

    @matchResult
    def hasExitBtn(self):
        """
        退出
        Returns:
        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("exitBtn__1191_40_50_41__1141_0_139_131.png")
        items = MyImread(path)
        pots,ok = imgSearchArea(GetSnapShot(), items, [1191,40,50,41])
        if ok:
            pot = pots[-1]
        else:
            pot = (0,0)
        return {"name":"退出世界树探索","pot":pot},ok

    @matchResult
    def hasCnfExitBtn(self):
        """
        直接退出
        Returns:
        """
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("cnfExit__469_472_106_28__419_422_206_128.png")
        items = MyImread(path)
        pots,ok = imgSearchArea(GetSnapShot(), items, [469,472,106,28])
        if ok:
            pot = pots[-1]
        else:
            pot = (0,0)
        return {"name":"直接退出","pot":pot},ok

    @matchResult
    def hasCnfExitBtnDia(self):
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("confExit2__582_155_114_29__532_105_214_129.png")
        items = MyImread(path)
        pots,ok = imgSearchArea(GetSnapShot(), items, [582,155,114,29])
        if ok:
            pot = pots[-1]
        else:
            pot = (0,0)
        return {"name":"确认退出确认框","pot":pot},ok
    @matchResult
    def hasCnfExitBtnDiaCnf(self):
        path = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("cnfExit3__728_471_61_29__678_421_161_129.png")
        items = MyImread(path)
        pots,ok = imgSearchArea(GetSnapShot(), items, [728,471,61,29])
        if ok:
            pot = pots[-1]
        else:
            pot = (0,0)
        return {"name":"确认退出确认框-[确认]","pot":pot},ok

if __name__ == '__main__':
    ConnectEmulator()
    c = WorldTreeDetect()

    while True:
        UpdateSnapShot()
        time.sleep(1)
        # imc = GetSnapShot()
        # imc = cutImgByRoi(imc, [450,19,46,20])
        # cv2.imshow("imc", imc)
        # cv2.waitKey(0)