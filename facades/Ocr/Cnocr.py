import numpy
from cnocr import CnOcr

class Cnocr:
    rec_root = "runtime/cnocr"

    def ocr(self, img : numpy.array):
        ocr = CnOcr(model_name='naive_det', root=self.rec_root)
        out = ocr.ocr(img)

        print(out)

    def ocr_for_single_line(self, img : numpy.array):
        """
        识别单行文字
        :param img:
        :return:
        """
        ocr = CnOcr(model_name='naive_det', root=self.rec_root)
        out = ocr.ocr_for_single_line(img)

        print(out)