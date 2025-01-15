import cv2
import numpy
import numpy as np
from airtest.core.api import click

from facades.Constant.Constant import IMG_PATH


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