import cv2

from act.facades.Configs.Config import Config
from act.facades.Constant.Constant import IMG_PATH
from act.facades.Detect.DetectLog import matchResult
from act.facades.Emulator.Emulator import GetSnapShot
from act.facades.Img.ImgRead import MyImread
from act.facades.Img.ImgSearch import imgSearchArea


class ItemsDetect:
    @matchResult
    def checkSkipFormat(self):
        """
        检查是否跳过编队
        :return:
        """
        img = {
            "url":"Main/normalBattle/skip__899_533_34_29__849_483_134_129.png",
            "roi": [899, 533, 34, 29]
        }

        template = MyImread(IMG_PATH.joinpath(img['url']))
        pot, ok = imgSearchArea(GetSnapShot(), template, img["roi"])
        if ok:
            pot = pot[0]

        return {"name":"勾选了跳过编队", "pot":pot},ok

    @matchResult
    def nowLoading(self):
        """
        正在加载
        :return:
        """
        img = {
            "url":"lag/loading__867_579_343_97__817_529_443_191.png",
            "roi": [867, 579, 343, 97]
        }
        template = MyImread(IMG_PATH.joinpath(img['url']))
        pot, ok = imgSearchArea(GetSnapShot(), template, img["roi"])
        if ok:
            pot = pot[0]

        return {"name":"正在加载", "pot":pot},ok

    @matchResult
    def goFormation(self):
        """
        前往编队
        :return:
        """
        img = {
            "url":"Main/normalBattle/go_formation__1065_536_106_26__1015_486_206_126.png",
            "roi": [1065, 536, 106, 26]
        }
        template = MyImread(IMG_PATH.joinpath(img['url']))
        pot, ok = imgSearchArea(GetSnapShot(), template, img["roi"])
        if ok:
            pot = pot[0]

        return {"name":"前往编队", "pot":pot},ok

    @matchResult
    def openRepeatBattleWindow(self):
        """
        进入重复战斗设置窗口
        :return:
        """
        img = {
            "url":"Main/normalBattle/repeatBattle__1135_25_41_32__1085_0_141_107.png",
            "roi": [1135, 25, 41, 32]
        }
        template =MyImread(IMG_PATH.joinpath(img['url']))
        pot, ok = imgSearchArea(GetSnapShot(), template, img["roi"])
        if ok:
            pot = pot[0]

        return {"name":"进入重复战斗设置窗口", "pot":pot},ok

    @matchResult
    def setLimit(self):
        """
        设置重复次数
        :return:
        """
        img = {
            "url":"Main/normalBattle/setLimit__265_421_213_38__215_371_313_138.png",
            "roi": [265,421,213,38]
        }
        template =MyImread(IMG_PATH.joinpath(img['url']))
        pot, ok = imgSearchArea(GetSnapShot(), template, img["roi"])
        if ok:
            pot = pot[0]

        return {"name":"设置重复次数", "pot":pot},ok

    @matchResult
    def setLimitInput(self):
        """
        设置重复次数-输入框
        :return:
        """
        img = {
            "url":"Main/normalBattle/setLimitInput__785_424_207_41__735_374_307_141.png",
            "roi": [785,424,207,41]
        }
        template =MyImread(IMG_PATH.joinpath(img['url']))
        pot, ok = imgSearchArea(GetSnapShot(), template, img["roi"])
        if ok:
            pot = pot[0]

        return {"name":"设置重复次数-输入框", "pot":pot},ok

    @matchResult
    def checkRepeatBattle(self):
        """
        开始重复战斗
        :return:
        """
        img = {
            "url":"Main/normalBattle/startRepeatBattle__562_531_156_20__512_481_256_120.png",
            "roi": [562,531,156,20]
        }
        template =MyImread(IMG_PATH.joinpath(img['url']))
        pot, ok = imgSearchArea(GetSnapShot(), template, img["roi"])
        if ok:
            pot = pot[0]

        return {"name":"开始重复战斗", "pot":pot},ok
    @matchResult
    def startBattle(self):
        """
        开始表演
        :return:
        """
        img = {
            "url":"",
            "roi": [1059, 655, 81, 45]
        }
        template, ok =MyImread(img['url'])
        pot, ok = imgSearchArea(GetSnapShot(), template, img["roi"])
        if ok:
            pot = pot[0]

        return {"name":"开始表演", "pot":pot},ok

    @matchResult
    def hasTopLeverButton(self):
        """
        高难副本
        :return:
        """
        img = [
            {
                "url":"topLever__1066_666_50_29__1016_616_150_104.png",
                "roi":[1059,655,81,45]
            },
            {
                "url": "topLever__1069_666_47_27__1019_616_147_104.png",
                "roi": [1059,655,81,45]
            }
        ]
        pot = ()
        ok = False
        for item in img:
            path = IMG_PATH.joinpath(f"Main/itemCollection/{item['url']}")
            img = MyImread(path)
            pot, ok = imgSearchArea(GetSnapShot(), img, item["roi"], 0.95)
            if ok:
                pot = pot[0]
                break
        return {"name":"发现高难副本","pot":pot},ok

    @matchResult
    def zeroNum(self):
        """
        次数用尽
        :return:
        """
        pot = ()

        roc = [1098,419,60,32]

        img = GetSnapShot()
        img = img[roc[1]:roc[1] + roc[3], roc[0]:roc[0] + roc[2]]
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # ocr = MyCnocr.ocrNum(img)

        num = 0
        # if len(ocr):
        #     if ocr[0]['text'] != '':
        #         num = int(ocr[0]['text'].replace("/3", ""))
        str = f"挑战次数 {num}"
        return {"name":str,"pot":pot},num<=0

    @matchResult
    def coinMap(self):
        """
        晶币副本
        :return:
        """
        img = {
            "url":"Main/normalBattle/coin__329_666_93_24__279_616_193_104.png",
            "roi": [329, 666, 93, 24]
        }
        template =MyImread(IMG_PATH.joinpath(img['url']))
        pot, ok = imgSearchArea(GetSnapShot(), template, img["roi"])
        if ok:
            pot = pot[0]

        return {"name":"晶币副本", "pot":pot},ok

    @matchResult
    def eqMap(self):
        """
        装备副本
        :return:
        """
        img = {
            "url":"Main/normalBattle/eq__140_667_97_25__90_617_197_103.png",
            "roi": [140, 667, 97, 25]
        }
        template =MyImread(IMG_PATH.joinpath(img['url']))
        pot, ok = imgSearchArea(GetSnapShot(), template, img["roi"])
        if ok:
            pot = pot[0]

        return {"name":"装备副本", "pot":pot},ok

    @matchResult
    def exclusiveMap(self):
        """
        专属副本
        :return:
        """
        img = {
            "url":"Main/normalBattle/exclusive__699_665_93_28__649_615_193_105.png",
            "roi": [699, 665, 93, 28]
        }
        template =MyImread(IMG_PATH.joinpath(img['url']))
        pot, ok = imgSearchArea(GetSnapShot(), template, img["roi"])
        if ok:
            pot = pot[0]

        return {"name":"专属副本", "pot":pot},ok

    @matchResult
    def expMap(self):
        """
        经验副本
        :return:
        """
        img = {
            "url":"Main/normalBattle/exp__884_666_92_28__834_616_192_104.png",
            "roi": [884, 666, 92, 28]
        }
        template =MyImread(IMG_PATH.joinpath(img['url']))
        pot, ok = imgSearchArea(GetSnapShot(), template, img["roi"])
        if ok:
            pot = pot[0]

        return {"name":"经验副本", "pot":pot},ok

    @matchResult
    def skillMap(self):
        """
        技能副本
        :return:
        """
        img = {
            "url":"Main/normalBattle/skill__512_665_94_29__462_615_194_105.png",
            "roi":[512,665,94,29]
        }
        template =MyImread(IMG_PATH.joinpath(img['url']))
        pot, ok = imgSearchArea(GetSnapShot(), template, img["roi"])
        if ok:
            pot = pot[0]

        return {"name":"技能副本", "pot":pot},ok

    def selectMap(self):
        """
        选择副本
        :return:
        """
        setting = Config("app.itemCollection.map")
        maps = {
            "技能副本":  self.skillMap,
            "经验副本":  self.expMap,
            "专属副本":  self.exclusiveMap,
            "装备副本":  self.eqMap,
            "晶币副本":  self.coinMap,
        }
        if setting not in maps:
            raise Exception("输入了不存在的副本："+setting)

        return maps[setting]
    @matchResult
    def inBattle(self):
        """
        重复战斗中
        :return:
        """
        img = {
            "url":"Main/normalBattle/inBattle__985_63_280_38__935_13_345_138.png",
            "roi":[985,63,280,38]
        }
        template =MyImread(IMG_PATH.joinpath(img['url']))
        pot, ok = imgSearchArea(GetSnapShot(), template, img["roi"])
        if ok:
            pot = pot[0]

        return {"name":"重复战斗中", "pot":pot},ok

    @matchResult
    def battleResult(self):
        """
        战斗收益
        :return:
        """
        img = {
            "url":"Main/normalBattle/battleResult__581_63_118_33__531_13_218_133.png",
            "roi":[581,63,118,33]
        }
        template =MyImread(IMG_PATH.joinpath(img['url']))
        pot, ok = imgSearchArea(GetSnapShot(), template, img["roi"])
        if ok:
            pot = pot[0]

        return {"name":"战斗收益", "pot":pot},ok
    @matchResult
    def resultIncome(self):
        """
        演出结算
        :return:
        """
        img = {
            "url":"Main/normalBattle/resultIncome__499_31_283_75__449_0_383_156.png",
            "roi":[499,31,283,75]
        }
        template =MyImread(IMG_PATH.joinpath(img['url']))
        pot, ok = imgSearchArea(GetSnapShot(), template, img["roi"])
        if ok:
            pot = pot[0]

        return {"name":"演出结算", "pot":pot},ok

    @matchResult
    def battleSuccess(self):
        """
        战斗胜利
        :return:
        """
        img = {
            "url":"Main/normalBattle/battleSuccess__468_425_355_91__418_375_455_191.png",
            "roi":[468,425,355,91]
        }
        template =MyImread(IMG_PATH.joinpath(img['url']))
        pot, ok = imgSearchArea(GetSnapShot(), template, img["roi"])
        if ok:
            pot = pot[0]

        return {"name":"战斗胜利", "pot":pot},ok
    @matchResult
    def settlementOfBattle(self):
        """
        演出结算
        :return:
        """
        img = {
            "url":"Main/normalBattle/settlementOfBattle__502_34_281_70__452_0_381_154.png",
            "roi":[502,34,281,70]
        }
        template =MyImread(IMG_PATH.joinpath(img['url']))
        pot, ok = imgSearchArea(GetSnapShot(), template, img["roi"])
        if ok:
            pot = pot[0]

        return {"name":"演出结算", "pot":pot},ok