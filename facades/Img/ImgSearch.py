import time
from typing import List

import cv2
import numpy
import numpy as np
from airtest.core.api import click

from facades.Constant.Constant import IMG_PATH
from facades.Emulator.Emulator import ConnectEmulator, GetSnapShot, UpdateSnapShot
from facades.Logx.Logx import logx


def imgSearch(img :numpy.array, template :numpy.array) -> (tuple, bool):
    """
    在图像中搜索模板，并返回模板匹配的中心点坐标及是否匹配成功。

    Args:
        img (np.ndarray): 输入图像，作为 NumPy 数组。
        template (np.ndarray): 模板图像，作为 NumPy 数组。

    Returns:
        Tuple[Tuple[int, int], bool]:
            - 第一个元素是一个元组，表示模板匹配的中心点坐标 (x, y)。如果未找到匹配，则返回 (0, 0)。
            - 第二个元素是一个布尔值，表示是否找到了匹配项。如果匹配度超过阈值则为 True，否则为 False。

    Raises:
        ValueError: 如果输入图像或模板为空或形状不正确。

    Examples:
        >>> center, found = imgSearch(img, template)
        >>> if found:
        ...     print(f"模板匹配成功，中心点为: {center}")
        ... else:
        ...     print("模板匹配失败")
    """
    # 检查输入参数的有效性
    if template is None:
        raise ValueError("模板不能为空")
    if img is None:
        raise ValueError("输入图像不能为空")

    if not hasattr(img, 'shape'):
        raise ValueError("截图必须是二维数组")

    if not hasattr(template, 'shape'):
        raise ValueError("模板必须是二维数组")

    if len(img.shape) < 2 or len(template.shape) < 2:
        raise ValueError("输入图像和模板必须是二维数组")

    image_x, image_y = template.shape[:2]
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    min_val, __max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if __max_val > 0.90:
        __center = (max_loc[0] + image_y / 2, max_loc[1] + image_x / 2)
        return __center, True
    else:
        __center = (0, 0)
        return __center, False

def imgMultipleResultSearch(img :numpy.array, template :numpy.array):
    """
    多个结果搜索
    :param img:
    :param template:
    :return:
    """
    # 检查输入参数的有效性
    if template is None:
        raise ValueError("模板不能为空")
    if img is None:
        raise ValueError("输入图像不能为空")

    if not hasattr(img, 'shape'):
        raise ValueError("截图必须是二维数组")

    if not hasattr(template, 'shape'):
        raise ValueError("模板必须是二维数组")

    if len(img.shape) < 2 or len(template.shape) < 2:
        raise ValueError("输入图像和模板必须是二维数组")

    # 获取模板尺寸
    template_height, template_width = template.shape[:2]

    # 进行模板匹配
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

    # 设置匹配阈值
    threshold = 0.9

    # 找到所有大于阈值的位置
    locations = np.where(result >= threshold)

    results = []
    # 遍历所有匹配结果

    for pt in zip(*locations[::-1]):  # locations 是 (y, x) 格式，需要反转

        # 获取匹配区域的左上角坐标
        top_left = pt

        # 计算中心点坐标
        center_x = top_left[0] + template_width // 2
        center_y = top_left[1] + template_height // 2

        # logx.info(f"匹配结果的中心点: ({center_x}, {center_y})")

        # 在图像上绘制矩形框和中心点
        bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
        center = (int(center_x), int(center_y))
        results.append(center)
        # 绘制矩形框
        # cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

        # 绘制中心点
        # cv2.circle(image, center, 5, (0, 0, 255), -1)
    return results, len(results) > 0

def imgSearchClick(img :numpy.array, template :numpy.array):
    """
    搜索并且点击图片
    :param img:
    :param template:
    :return:
    """
    t,ok = imgSearch(img, template)
    if ok:
        click(t)
        return t
    else:
        return None

if __name__ == '__main__':
    ConnectEmulator()
    time.sleep(1)
    lq = IMG_PATH.joinpath("Main").joinpath("worldTree").joinpath("cards").joinpath("m1.png")

    UpdateSnapShot()
    img = GetSnapShot().img

    cvi = cv2.imread(f"{lq}")

    # 获取图片数据
    # data = cvi.getdata()
    #
    # # 创建一个新的像素列表
    # new_data = []
    # for item in data:
    #     # 如果像素接近黑色（RGB 值小于某个阈值），则设置为透明
    #     if item[0] < 50 and item[1] < 50 and item[2] < 50:  # 阈值可以根据需要调整
    #         new_data.append((0, 0, 0, 0))  # 设置为完全透明
    #     else:
    #         new_data.append(item)  # 保留原像素

    # 更新图片数据
    # cvi.putdata(new_data)


    res,ok = imgSearch(GetSnapShot().img, cvi)
    print(res,ok)