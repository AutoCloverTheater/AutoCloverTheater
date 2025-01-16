import cv2
import numpy as np


def hex_to_bgr(hex_color):
    """
    将十六进制颜色代码转换为 BGR 格式。

    参数:
        hex_color (str): 十六进制颜色代码，例如 "#F9E9CF"。

    返回:
        tuple: BGR 值，例如 (207, 233, 249)。
    """
    # 去除 # 号
    hex_color = hex_color.lstrip('#')

    # 将十六进制转换为 RGB
    rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    # 将 RGB 转换为 BGR
    bgr = (rgb[2], rgb[1], rgb[0])

    return bgr


def bgr_to_hex(bgr):
    """
    将 BGR 格式转换为十六进制颜色代码。

    参数:
        bgr (tuple): BGR 值，例如 (207, 233, 249)。

    返回:
        str: 十六进制颜色代码，例如 "#F9E9CF"。
    """
    # 将 BGR 转换为 RGB
    rgb = (bgr[2], bgr[1], bgr[0])

    # 将 RGB 转换为十六进制
    hex_color = "#{:02X}{:02X}{:02X}".format(*rgb)

    return hex_color

def imgGetColor(img, low, top):
    # 定义目标颜色 (BGR 格式)
    # low = [151, 179, 189]
    low = hex_to_bgr(low)
    # top = [207, 233, 249]
    top = hex_to_bgr(top)

    # 读取图片
    image = img

    # 创建一个掩码，找到颜色值为 target_color 的像素
    # 这里允许一定的颜色容差
    # lower_bound = np.array([175, 200, 220], dtype=np.uint8)  # 下限
    # upper_bound = np.array([190, 220, 230], dtype=np.uint8)  # 上限
    lower_bound = np.array(low, dtype=np.uint8)  # 下限
    upper_bound = np.array(top, dtype=np.uint8)  # 上限
    mask = cv2.inRange(image, lower_bound, upper_bound)

    # 将掩码外的像素设置为黑色
    result = cv2.bitwise_and(image, image, mask=mask)

    return result
