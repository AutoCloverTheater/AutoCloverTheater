import cv2
from paddlex import create_pipeline

from act.facades.Emulator.Emulator import ConnectEmulator, GetSnapShot, UpdateSnapShot
from act.facades.tool import cutImgByRoi

if __name__ == "__main__":
    ConnectEmulator()
    pipeline = create_pipeline(pipeline="OCR")

    while True:
        UpdateSnapShot()
        img = GetSnapShot()
        img = cutImgByRoi(img, [109,663,910,70])
        cv2.imshow("img", img)
        if cv2.waitKey(2) & 0xFF == ord('q'):
            break
        else:
            output = pipeline.predict(
                input=img,
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
                use_textline_orientation=False,
            )
            for res in output:
                print(res["rec_texts"])
                # print(res["dt_polys"])
            continue

    cv2.destroyAllWindows()