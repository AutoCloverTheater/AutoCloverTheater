import cv2

from facades.Constant.Constant import ROOT_PATH
from facades.Ocr.MyCnocr import MyCnocr

def TestOcr_for_single_line():
    path = ROOT_PATH.joinpath("img").joinpath("WorldTree")
    出发冒险 = MyImread(f"{path}/chufamaoxian.png")
    ocr = MyCnocr()
    print(ocr.ocr(出发冒险))

def test_ocr(benchmark):
    benchmark(TestOcr_for_single_line)

def test_tmp():
    path = ROOT_PATH.joinpath("img").joinpath("WorldTree").joinpath("tmp.png")
    img = MyImread(path)
    y,x,_ = img.shape

    cardxy = img[300:400,150:x-150]
    cv2.imwrite("cardxy.png",cardxy)
    res = MyCnocr.ocr(img)

    rpc = [item for item in res if item["score"] > 0.4 and item['text'] != '']
    print(rpc)