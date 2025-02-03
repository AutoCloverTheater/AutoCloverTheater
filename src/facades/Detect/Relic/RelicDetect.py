import cv2

from src.facades.Constant.Constant import IMG_PATH
from src.facades.Detect.DetectLog import matchResult
from src.facades.Emulator.Emulator import GetSnapShot, ConnectEmulator, UpdateSnapShot
from src.facades.Img import find_all_template
from src.facades.Img.ImgColor import imgFindByColor
from src.facades.Img.ImgRead import MyImread
from src.facades.Img.ImgSearch import imgSearchArea
from src.facades.Logx.Logx import logx


class RelicDetect:

    def __init__(self):
        """
        遗迹
        """
        pass

    @matchResult
    def isInRelicEntrance(self):
        """
        遗迹探索准备窗口
        :return:[]roi
        :return:bool
        """
        path = IMG_PATH.joinpath("main/relic/relicEntrance__95_23_91_22__45_0_191_95.png")
        img = MyImread(path)
        rois,ok = imgSearchArea(GetSnapShot(), img, [95, 23, 91, 22])
        if len(rois) > 0:
            pot = rois[0]
        else:
            pot = (0,0)

        return {"name": "遗迹探索", "pot": pot}, ok

    @matchResult
    def hasDesert(self):
        """
        是否处于沙漠星城
        :return:[]roi
        :return:bool
        """
        path = IMG_PATH.joinpath("main/relic/desert__138_205_108_40__88_155_208_140.png")
        img = MyImread(path)
        rois,ok = imgSearchArea(GetSnapShot(), img, [138, 205, 108, 40])
        if len(rois) > 0:
            pot = rois[0]
        else:
            pot = (0,0)

        return {"name": "沙漠星城", "pot": pot}, ok

    @matchResult
    def hasNormal(self):
        """
        普通难度
        :return:[]roi
        :return:bool
        """
        path = IMG_PATH.joinpath("main/relic/normal__352_105_97_25__302_55_197_125.png")
        img = MyImread(path)
        rois,ok = imgSearchArea(GetSnapShot(), img, [138, 205, 108, 40])
        if len(rois) > 0:
            pot = rois[0]
        else:
            pot = (0,0)

        return {"name": "普通难度", "pot": pot}, ok

    @matchResult
    def hasGoExplore(self):
        """
        前往探索
        :return:[]roi
        :return:bool
        """
        path = IMG_PATH.joinpath("main/relic/goExplore__999_612_106_29__949_562_206_129.png")
        img = MyImread(path)
        pot,ok = imgSearchArea(GetSnapShot(), img, [999, 612, 106, 29])
        if ok:
            pot = pot[0]

        return {"name": "前往探索", "pot": pot}, ok

    @matchResult
    def hasConfirmButton(self):
        """
        确认按钮
        :return:[]roi
        :return:bool
        """
        imgs = [
            'main/relic/confirm01__618_558_67_30__568_508_167_130.png',
        ]

        path = IMG_PATH.joinpath("main/relic/confirm01__618_558_67_30__568_508_167_130.png")
        img = MyImread(path)
        pot,ok = imgSearchArea(GetSnapShot(), img, [618,558,67,30])
        if ok :
            pot = pot.pop()

        return {"name": "确认", "pot": pot}, ok

    @matchResult
    def hasConfirmButton03(self):
        """
        确认按钮
        :return:[]roi
        :return:bool
        """

        path = IMG_PATH.joinpath("main/relic/c03__617_556_72_35__567_506_172_135.png")
        img = MyImread(path)
        pot, ok = imgSearchArea(GetSnapShot(), img, [618, 558, 67, 30], 0.95)
        if ok:
            pot = pot.pop()

        return {"name": "确认03", "pot": pot}, ok

    @matchResult
    def hasSelectButton(self):
        """
        选择按钮
        :return:
        """
        rois = [
            [969, 219, 50, 24],  # 第一个选择
            [969,322,51,27],# 第二个选择
        ]

        pot = ()
        ok = False
        for k, roi in enumerate(rois):
            path = IMG_PATH.joinpath("main/relic/select.png")
            img = MyImread(path)
            pot,ok = imgSearchArea(GetSnapShot(), img, roi)
            if ok :
                logx.info(f"选择按钮{k}")
                pot = (int(roi[0] + roi[2] / 2),int(roi[1]+ roi[3] / 2))
                break

        return {"name": "选择", "pot": pot}, ok

    def pointNotEnough(self):
        """
        点数不足
        Returns:
        """

        path = IMG_PATH.joinpath("main/relic/notEnough__520_281_239_25__470_231_339_125.png")
        img = MyImread(path)
        pot, ok = imgSearchArea(GetSnapShot(), img, [516,180,249,177], 0.8)
        if ok:
            cv2.imwrite("im.png", GetSnapShot())
            logx.info("点数不足")
            pot = (969+25,322+12)

        return {"name": "点数不足", "pot": pot}, ok

    @matchResult
    def pressAnyKeyToContinue(self):
        """
        点击弹窗其他区域关闭
        :return:[]roi
        :return:bool
        """

        imgs = [
            'lag/lag__622_345_35_31__572_295_135_131.png',
            'lag/lag__576_400_136_35__526_350_236_135.png',
            'lag/loading__867_579_343_97__817_529_443_191.png',
        ]
        roi = [
            (622, 345, 35, 31),
            (576, 400, 136, 35),
            (867, 579, 343, 97),
        ]
        ok = False
        pot = (0, 0)

        for k, i in enumerate(imgs):
            loading = MyImread(IMG_PATH.joinpath("lag").joinpath(i))
            resp, ok  = imgSearchArea(GetSnapShot(), loading, roi[k])
            if ok:
                pot = resp[0]
                break

        return {"name": "点击弹窗其他区域关闭", "pot": pot}, ok
    @matchResult
    def  eventPoint(self):
        """
        遗迹兴趣点
        :return:res
        :return:bool
        """
        img = GetSnapShot()
        imgG = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        temp = MyImread(IMG_PATH.joinpath("Main/relic/point__975_417_80_23__925_367_180_123.png"))
        tempG = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)

        # 设定亮度阈值（0-255，值越小，亮度要求越低）
        brightness_threshold = 100

        # 创建掩码：亮度低于阈值的区域为黑色，其余为白色
        mask = cv2.threshold(imgG, brightness_threshold, 255, cv2.THRESH_BINARY)[1]

        # 将掩码应用到原图上
        imgG = cv2.bitwise_and(imgG, imgG, mask=mask)

        res = find_all_template(imgG, tempG, threshold=0.75)
        # 筛选出来x，y最小的点
        sorted_data = sorted(res, key=lambda x: x['result'])

        pot = [x['result'] for x in sorted_data]

        # x < 400,y>400的剔除
        for k, item in enumerate(pot):
            x, y = item
            if x < 400 < y:
                del pot[k]

        return {"name": "遗迹兴趣点", "pot": pot}, len(pot) > 0

    @matchResult
    def isInRelicGame(self):
        """
        是否在遗迹探索游戏内
        Returns:
        """
        path = "Main/relic/location__40_231_41_62__0_181_131_162.png"
        path = IMG_PATH.joinpath(path)
        img = MyImread(path)
        rois,ok = imgSearchArea(GetSnapShot(), img, [40, 231, 41, 62])
        if len(rois) > 0:
            pot = rois[0]
        else:
            pot = (0,0)
        return {"name": "遗迹探索中...", "pot": pot}, ok


    @matchResult
    def location(self):
        """
        重制视角
        Returns:

        """
        path = IMG_PATH.joinpath("Main/relic/location__40_231_41_62__0_181_131_162.png")
        img = MyImread(path)
        rois,ok = imgSearchArea(GetSnapShot(), img, [40, 231, 41, 62])
        if len(rois) > 0:
            pot = rois[0]
        else:
            pot = (0,0)

        return {"name": "重制视角", "pot": pot}, ok

    @matchResult
    def killedBoss(self):
        """
        击杀过boss了
        Returns:
        """
        roi = [752,150,13,8]
        pot = (703,210)
        img = GetSnapShot()

        img = img[roi[1]:roi[1]+roi[3],roi[0]:roi[0]+roi[2]]
        ok = imgFindByColor(img, "281e96", 0.6)

        return {"name": "击杀过boss了", "pot": pot}, ok

    @matchResult
    def reLocation(self):
        path = IMG_PATH.joinpath("Main/relic/reLocation__701_266_120_26__651_216_220_126.png")
        img = MyImread(path)
        rois,ok = imgSearchArea(GetSnapShot(), img, [690,251,150,126])

        pot = ()
        if ok > 0:
            pot = rois.pop()

        return {"name": "当前路径不能直接跳转请重新选择", "pot": pot}, ok

    @matchResult
    def explorationEnds(self):
        """
        探索结束
        :return:
        """
        path = IMG_PATH.joinpath("Main/relic/explorationEnds__451_122_376_53__401_72_476_153.png")
        img = MyImread(path)
        rois,ok = imgSearchArea(GetSnapShot(), img, [451, 122, 376, 53])
        if len(rois) > 0:
            pot = (0.5, 0)
        else:
            pot = (0,0)

        return {"name": "探索结束", "pot": pot}, ok

    @matchResult
    def hasSettingMap(self):
        """
        选择地图
        Returns:

        """
        maps = [
            {
                "name":"热砂",
                "url":"hot.png",
            }
        ]

        path = IMG_PATH.joinpath("main/relic/hot.png")
        img = MyImread(path)
        pot,ok = imgSearchArea(GetSnapShot(), img, [124,63,161,645])
        if ok:
            pot = pot[0]

        return {"name": f"选择地图 {maps[0]}", "pot": pot}, ok

    @matchResult
    def hasSettingRank(self):
        """
        选择难度
        :return:
        """
        ranks = [
            "噩梦"
        ]

        path = IMG_PATH.joinpath("main/relic/nightmare__350_233_96_24__300_183_196_124.png")
        img = MyImread(path)
        pot,ok = imgSearchArea(GetSnapShot(), img, [350, 233, 96, 24])
        if ok:
            pot = pot[0]

        return {"name": f"选择难度 {ranks[0]}", "pot": pot}, ok

    @matchResult
    def getItems(self):
        """
        获取道具
        :return:
        """
        path = IMG_PATH.joinpath("main/relic/getItems__497_78_282_72__447_28_382_172.png")
        img = MyImread(path)
        pot,ok = imgSearchArea(GetSnapShot(), img, [497, 78, 282, 72])
        if ok > 0:
            pot = (0.5, 0.0)

        return {"name": "获取道具", "pot": pot}, ok

if __name__ == '__main__':
    ConnectEmulator()

    relic = RelicDetect()
    # [699, 193, 120, 66]
    while True:
        UpdateSnapShot()
        img = GetSnapShot()
        _,ok = relic.killedBoss()
        if ok :
            left = (699,193)
            bottom = (699+120,193+66)
            cv2.rectangle(img, left, bottom, (0, 255, 0), 2)

        cv2.imshow("png", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # 按 'q' 退出
            cv2.destroyAllWindows()
            break
        # while True: