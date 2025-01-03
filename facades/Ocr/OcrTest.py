import cv2

from facades.Constant.Constant import ROOT_PATH
from facades.Ocr.MyCnocr import MyCnocr


def TestOcr():
    path = ROOT_PATH.joinpath("img").joinpath("WorldTree")

    出发冒险 = cv2.imread(f"{path}/chufamaoxian.png")
    选择 = cv2.imread(f"{path}/xuanze.png")
    exit = cv2.imread(f"{path}/exit.png")

    list = [出发冒险, 选择, exit]

    ocr = MyCnocr()
    for img in list:
        print(ocr.ocr(img))


if __name__ == "__main__":
    TestOcr()