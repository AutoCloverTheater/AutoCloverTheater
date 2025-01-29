from facades.Constant.Constant import IMG_PATH
from facades.Detect.DetectLog import matchResult
from facades.Emulator.Emulator import GetSnapShot
from facades.Img.ImgRead import MyImread
from facades.Img.ImgSearch import imgSearchArea


class GuildDetect:
    @matchResult
    def hasGuildButton(self):
        """
        判断是否有公会按钮
        """

        path = IMG_PATH.joinpath(f"guild/guild__594_544_64_22__544_494_164_122.png")
        img = MyImread(path)
        pot, ok = imgSearchArea(GetSnapShot(), img, [594, 544, 64, 22], 0.95)
        if ok:
            pot = pot[0]

        return {"name":"工会", "pot":pot},ok

    @matchResult
    def hasGuildHallButton(self):
        """
        判断是否有工会大厅
        """
        path = IMG_PATH.joinpath(f"guild/guildHall__72_117_109_29__22_67_209_129.png")
        img = MyImread(path)
        pot, ok = imgSearchArea(GetSnapShot(), img, [72, 117, 109, 29], 0.95)
        if ok:
            pot = pot[0]

        return {"name":"工会大厅", "pot":pot},ok

    @matchResult
    def hasDonate(self):
        """
        判断是否有捐献按钮
        """
        path = IMG_PATH.joinpath(f"guild/donate__1174_618_64_80__1124_568_156_152.png")
        img = MyImread(path)
        pot, ok = imgSearchArea(GetSnapShot(), img, [1174, 618, 64, 80], 0.95)
        if ok:
            pot = pot[0]

        return {"name":"捐献", "pot":pot},ok

    @matchResult
    def canDonate(self):
        """
        捐献次数
        """
        path = IMG_PATH.joinpath(f"guild/outOfDonateNum__653_517_42_23__603_467_142_123.png")
        img = MyImread(path)
        pot, ok = imgSearchArea(GetSnapShot(), img, [653, 517, 42, 23], 0.98)
        if ok:
            pot = pot[0]

        return {"name":"捐献次数达到上限", "pot":pot},ok

    @matchResult
    def donate(self):
        """
        捐献
        """
        path = IMG_PATH.joinpath(f"guild/donateButton__478_443_56_28__428_393_156_128.png")
        img = MyImread(path)
        pot, ok = imgSearchArea(GetSnapShot(), img, [478, 443, 56, 28], 0.95)
        if ok:
            pot = pot[0]

        return {"name":"捐献", "pot":pot},ok

    @matchResult
    def hasGuildRequestion(self):
        """
        工会任务
        """
        path = IMG_PATH.joinpath(f"guild/guildRequestion__947_334_114_30__897_284_214_130.png")
        img = MyImread(path)
        pot, ok = imgSearchArea(GetSnapShot(), img, [947, 334, 114, 30], 0.95)
        if ok:
            pot = pot[0]

        return {"name":"工会任务", "pot":pot},ok

    @matchResult
    def canGetReward(self):
        path = IMG_PATH.joinpath(f"guild/canGetReward__605_96_35_24__555_46_135_124.png")
        img = MyImread(path)
        pot, ok = imgSearchArea(GetSnapShot(), img, [605, 96, 35, 24], 0.95)
        if ok:
            pot = pot[0]

        return {"name":"可以领取奖励", "pot":pot},ok

    @matchResult
    def getReward(self):
        """
        领取全部奖励
        """
        path = IMG_PATH.joinpath(f"guild/getAllReward__585_595_107_28__535_545_207_128.png")
        img = MyImread(path)
        pot, ok = imgSearchArea(GetSnapShot(), img, [585, 595, 107, 28], 0.95)
        if ok:
            pot = pot[0]

        return {"name":"领取全部奖励", "pot":pot},ok

    @matchResult
    def hasMeettingRoom(self):
        """
        议事厅
        """
        path = IMG_PATH.joinpath(f"guild/meettingRoom__71_193_81_26__21_143_181_126.png")
        img = MyImread(path)
        pot, ok = imgSearchArea(GetSnapShot(), img, [71, 193, 81, 26], 0.95)
        if ok:
            pot = pot[0]
        return {"name":"议事厅", "pot":pot},ok