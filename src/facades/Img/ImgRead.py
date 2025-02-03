import cv2

from src.facades.Constant.Constant import IMG_PATH
from src.facades.Logx.Logx import logx

IMG_POOL = {}

def MyImread(path):
    p = f"{path}"

    if p in IMG_POOL:
        return IMG_POOL[p]
    else:
        IMG_POOL[p] = cv2.imread(p)
        if IMG_POOL[p] is None:
            logx.exception(f"{p} not found")
        return  IMG_POOL[p]


if __name__ == "__main__":
    img = IMG_PATH.joinpath("WorldTree").joinpath("quit.png")
    MyImread(img)
    print(f"{len(IMG_POOL)}\n")
    MyImread(img)
    print(f"{len(IMG_POOL)}\n")