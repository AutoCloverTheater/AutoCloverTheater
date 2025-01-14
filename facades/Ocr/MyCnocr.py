import numpy
from cnocr import CnOcr

from facades.Constant.Constant import RUNTIME_PATH

class Cnocr:
    rec_root = RUNTIME_PATH.joinpath("cnocr")
    det_root = RUNTIME_PATH.joinpath("cnstd")

    def ocr(self, img : numpy.array):
        ocr = CnOcr(det_root=self.rec_root,rec_root=self.det_root, rec_model_name="scene-densenet_lite_136-gru")
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