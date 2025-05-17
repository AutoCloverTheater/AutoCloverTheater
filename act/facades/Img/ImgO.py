from collections import Counter

import cv2
import numpy as np

from act.facades.Emulator.Emulator import UpdateSnapShot, ConnectEmulator, GetSnapShot
from act.facades.Logx.Logx import logx


def calculate_slope(x1, y1, x2, y2):
    if x1 == x2:
        return None  # 斜率不存在
    return (y2 - y1) / (x2 - x1)

def imo(image):
    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 边缘检测
    edges = cv2.Canny(gray, 50, 150)

    # 概率霍夫变换检测直线
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

    ks = []
    k1 = 50
    k2 = -50
    # 绘制直线
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            k = calculate_slope(x1,y1,x2,y2)
            if k is None:
                continue
            k = int(k * 100)
            if k is 0:
                continue

            if k > 0 and abs(k - k1) > 4:
                continue
            if k < 0 and abs(k - k2) > 4:
                continue
            ks.append(k)
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 绘制绿色直线
    r = Counter(ks)
    logx.info(f"斜率分组{r}")

    return image
    # 显示结果
    cv2.imshow("Detected Lines (Probabilistic Hough)", image)
    cv2.waitKey(1)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    ConnectEmulator()
    while True:
        UpdateSnapShot()
        img = GetSnapShot()

        res = imo(img)
        cv2.imshow("png", res)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # 按 'q' 退出
            break