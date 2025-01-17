import cv2
import imagehash
from PIL import Image

from facades.Constant.Constant import IMG_PATH
from facades.Emulator.Emulator import GetSnapShot, ConnectEmulator, UpdateSnapShot
from facades.Img.ImgColor import imgGetColor
from facades.Logx.Logx import logx


def saveCard():
    """
    翻新世界树卡片资源用
    :return:
    """
    img = GetSnapShot().img
    y, x, _ = img.shape
    cardxy = img[565:595, :]

    # 将掩码外的像素设置为黑色
    result = imgGetColor(img=cardxy, low="AB9F87", top="F9E9CF")

    result1 = result
    result2 = result
    result3 = result
    # 保存图片
    l = result1[0:28, 293:428]  # 293:428
    m = result2[0:28, 556:688]  # 556:688
    r = result3[0:28, 815:950]  # 815:950

    lname = imagehash.average_hash(Image.fromarray(l))
    mname = imagehash.average_hash(Image.fromarray(m))
    rname = imagehash.average_hash(Image.fromarray(r))

    lp = IMG_PATH.joinpath("Main/worldTree/cards").joinpath(f"l/{lname}.png")
    mp = IMG_PATH.joinpath("Main/worldTree/cards").joinpath(f"m/{mname}.png")
    rp = IMG_PATH.joinpath("Main/worldTree/cards").joinpath(f"r/{rname}.png")

    res1 = cv2.imwrite(f"{lp}", l)
    res2 = cv2.imwrite(f"{mp}", m)
    res3 = cv2.imwrite(f"{rp}", r)
    logx.info(f"保存结果 {res1},{res2},{res3}\n")

if __name__ == '__main__':
    ConnectEmulator()
    UpdateSnapShot()
    saveCard()