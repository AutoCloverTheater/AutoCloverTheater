import cv2
import numpy as np

from src.facades.Logx.Logx import logx


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

def imgFindByColor(image, hex_color = '', threshold=0.9):
    """
    在图片中寻找符合的颜色
    :param image: cv2 格式的图片
    :param hex_color: 16进制rgb
    :param threshold: 符合的颜色在输入图片中的所占比例，高于返回true，低于返回false
    :return:
    """
    # 定义目标颜色 (#2F218F)
    hex_color = f"#{hex_color.replace('#', '')}"
    rgb_color = tuple(int(hex_color[i:i + 2], 16) for i in (1, 3, 5))  # 转换为 RGB
    bgr_color = (rgb_color[2], rgb_color[1], rgb_color[0])  # 转换为 BGR

    # 将 BGR 颜色转换为 HSV
    bgr_color_np = np.uint8([[list(bgr_color)]])  # 转换为 NumPy 数组
    hsv_color = cv2.cvtColor(bgr_color_np, cv2.COLOR_BGR2HSV)[0][0]

    # 定义 HSV 范围
    lower_bound = np.array([hsv_color[0] - 10, 50, 50])  # HSV 下限
    upper_bound = np.array([hsv_color[0] + 10, 255, 255])  # HSV 上限

    # 读取图像
    x,y = image.shape[:2]
    total = x*y

    # 将图像转换为 HSV 颜色空间
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 创建掩码
    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

    # 统计符合标准的像素数量
    pixel_count = cv2.countNonZero(mask)

    return  (pixel_count / total) > threshold

    # # 查找轮廓
    # contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #
    # # 在原图上绘制轮廓
    # for contour in contours:
    #     x, y, w, h = cv2.boundingRect(contour)
    #     cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 绘制绿色矩形框
    #
    # # 显示结果
    # cv2.imshow('Original Image', image)
    # cv2.imshow('Mask', mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    img = cv2.imread("temp.png")

    c = "FE9DFB"# 遗迹boss点的颜色
    res = imgFindByColor(img, c, 0.5)
    logx.info(f"符合的像素点数: {res}")

    img = cv2.imread("temp2.png")

    c = "FE9DFB"# 遗迹boss点的颜色
    res = imgFindByColor(img, c, 0.5)
    logx.info(f"符合的像素点数: {res}")