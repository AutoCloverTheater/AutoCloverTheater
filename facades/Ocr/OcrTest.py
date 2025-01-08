import cv2

from facades.Constant.Constant import ROOT_PATH
from facades.Ocr.MyCnocr import MyCnocr

def TestOcr_for_single_line():
    path = ROOT_PATH.joinpath("img").joinpath("WorldTree")
    出发冒险 = cv2.imread(f"{path}/chufamaoxian.png")
    ocr = MyCnocr()
    print(ocr.ocr(出发冒险))

def test_ocr(benchmark):
    benchmark(TestOcr_for_single_line)