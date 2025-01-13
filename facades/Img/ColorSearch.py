import cv2
import numpy as np

from facades.Constant.Constant import IMG_PATH


def rgb_to_hsv(rgb_color):
    """
    将RGB颜色转换为HSV颜色。

    Args:
        rgb_color (list): RGB颜色列表，例如 [130, 97, 70]。

    Returns:
        tuple: HSV颜色元组，例如 (h, s, v)。
    """
    rgb_color = np.uint8([[rgb_color]])
    hsv_color = cv2.cvtColor(rgb_color, cv2.COLOR_RGB2HSV)[0][0]
    return hsv_color


def colorSearch(img: np.ndarray, color_rgb):
    """
    在图像中检测特定RGB颜色并标记出来。

    Args:
        img (np.ndarray): 输入图像，作为 NumPy 数组。
        color_rgb (list): 要检测的RGB颜色列表，例如 [130, 97, 70]。
    """
    # 读取图像
    image = img

    # 转换为HSV颜色空间
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 将RGB颜色转换为HSV颜色
    color_hsv = rgb_to_hsv(color_rgb)

    # 定义颜色范围（可以根据需要调整范围）
    lower_hsv = np.array([color_hsv[0] - 10, color_hsv[1] - 50, color_hsv[2] - 50])
    upper_hsv = np.array([color_hsv[0] + 10, color_hsv[1] + 50, color_hsv[2] + 50])

    # 创建掩码
    mask = cv2.inRange(hsv_image, lower_hsv, upper_hsv)

    # 用掩码提取特定颜色的区域
    color_image = cv2.bitwise_and(image, image, mask=mask)

    # 寻找轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 绘制轮廓
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:  # 可根据需要调整面积阈值
            cv2.drawContours(image, [contour], -1, (0, 255, 0), 3)  # 绿色轮廓

    # 显示结果
    cv2.imshow('Original Image', image)
    cv2.imshow('Mask', mask)
    cv2.imshow('Result', color_image)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()

    # 保存结果
    cv2.imwrite('./result.jpg', image)


if __name__ == "__main__":
    img = IMG_PATH.joinpath("WorldTree").joinpath("quit.png")
    imgL = cv2.imread(f"{img}")
    colorSearch(imgL, [130, 97, 70])