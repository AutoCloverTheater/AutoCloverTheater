import cv2
import numpy
from cnocr import CnOcr

from facades.Constant.Constant import RUNTIME_PATH, IMG_PATH


class Cnocr:
    rec_root = RUNTIME_PATH.joinpath("cnocr")
    det_root = RUNTIME_PATH.joinpath("cnstd")

    def ocr(self, img : numpy.array):
        ocr = CnOcr(det_root=self.rec_root,rec_root=self.det_root, rec_model_name="scene-densenet_lite_136-gru")
        out = ocr.ocr(img)
        return out



    def bizarreCardOcr(self, img : numpy.array):
        ocr = CnOcr(det_root=self.rec_root,rec_root=self.det_root, rec_model_name="scene-densenet_lite_136-gru")
        out = ocr.ocr(img)
        return out

    def ocrNum(self,img : numpy.array):
        ocr = CnOcr(det_root=self.rec_root,rec_root=self.det_root, rec_model_name="scene-densenet_lite_136-gru", cand_alphabet=[
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
        ])
        out = ocr.ocr(img)
        return out

    def ocr_for_single_line(self, img : numpy.array):
        """
        识别单行文字
        :param img:
        :return:
        """
        ocr = CnOcr(det_root=self.rec_root,rec_root=self.det_root)
        out = ocr.ocr_for_single_line(img)

        print(out)

MyCnocr = Cnocr()

if __name__ == '__main__':
    i = IMG_PATH.joinpath("WorldTree").joinpath("tmp.png")
    img = MyImread(f"{i}")
    print(MyCnocr.ocr(img))