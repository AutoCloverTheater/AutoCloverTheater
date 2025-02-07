from facades.Constant.Constant import IMG_PATH
from facades.Emulator.Emulator import GetSnapShot
from facades.Img.ImgRead import MyImread
from facades.Img.ImgSearch import imgSearchArea


class BackPack:
    def __init__(self) -> None:
        pass

    def spaceNotEnough(self):
        """
        仓库空间不足
        """
        path = IMG_PATH.joinpath(f"backpack/backPackIsFull__555_156_173_34__505_106_273_134.png")
        img = MyImread(path)
        pot, ok = imgSearchArea(GetSnapShot(), img, [555, 156, 173, 34])
        if ok:
            pot = pot[0]

        return {"name": "仓库空间不足", "pot": pot}, ok


    def cancle(self):
        """
        取消
        """
        path = IMG_PATH.joinpath(f"cancel/cancel__424_463_61_30__374_413_161_130.png")
        img = MyImread(path)
        pot, ok = imgSearchArea(GetSnapShot(), img, [424, 463, 61, 30])
        if ok:
            pot = pot[0]

        return {"name": "取消", "pot": pot}, ok