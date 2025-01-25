import glob
import os

import cv2
import numpy
import numpy as np

from facades.Constant.Constant import IMG_PATH
from facades.Emulator.Emulator import ConnectEmulator, GetSnapShot, UpdateSnapShot, Click
from facades.Img import find_template, find_all_template
from facades.Img.ImgRead import MyImread
from facades.Logx.Logx import logx


def imgSearch(img :numpy.array, template :numpy.array, threshold=0.90) -> (tuple, bool):
    """
    在图像中搜索模板，并返回模板匹配的中心点坐标及是否匹配成功。

    Args:
        img (np.ndarray): 输入图像，作为 NumPy 数组。
        template (np.ndarray): 模板图像，作为 NumPy 数组。
        threshold: 可信度

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

    if __max_val > threshold:
        __center = (int(max_loc[0] + image_y / 2), int(max_loc[1] + image_x / 2))
        return __center, True
    else:
        __center = (0, 0)
        return __center, False

def imgMultipleResultSearch(img :numpy.array, template :numpy.array, threshold=0.92):
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
        Click(t)
        return t
    else:
        return None

def imgSearchArea(image :numpy.array, template :numpy.array,roi, threshold=0.9):
    """
    匹配局部区域,返回所有可能的位置
    :param image:
    :param template:
    :param roi :[x,y,w,h] 左上角坐标，宽，高
    :param threshold:可信度
    :return:
    """
    # 检查输入参数的有效性
    if template is None:
        raise ValueError("模板不能为空")
    if image is None:
        raise ValueError("输入图像不能为空")

    if not hasattr(image, 'shape'):
        raise ValueError("截图必须是二维数组")

    if not hasattr(template, 'shape'):
        raise ValueError("模板必须是二维数组")

    if len(image.shape) < 2 or len(template.shape) < 2:
        raise ValueError("输入图像和模板必须是二维数组")

    # 读取图像和模板
    # 获取模板尺寸
    template_height, template_width = template.shape[:2]

    # 定义局部区域的左上角和右下角坐标
    x1, y1 = (roi[0] , roi[1])  # 局部区域的左上角
    x2, y2 = (roi[0] + roi[2], roi[1] + roi[3])  # 局部区域的右下角

    # 提取局部区域
    local_region = image[y1:y2, x1:x2]

    # 进行模板匹配
    result = cv2.matchTemplate(local_region, template, cv2.TM_CCOEFF_NORMED)

    # 找到所有大于阈值的位置
    locations = np.where(result >= threshold)

    results = []
    # 遍历所有匹配结果

    for pt in zip(*locations[::-1]):  # locations 是 (y, x) 格式，需要反转
        if len(results) >0:
            break
        # 获取匹配区域的左上角坐标
        top = pt


        # 找到最佳匹配位置
        # 将局部区域的坐标转换为全局坐标
        top_left = (int(top[0] + x1), int(top[1] + y1))

        # 计算中心点坐标
        center_x = top_left[0] + (template_width / 2)
        center_y = top_left[1] + (template_height / 2)
        center = (int(center_x), int(center_y))
        results.append(center)

        bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
        # logx.info(f"lef {top_left}")
        # logx.info(f"center {center}")
        # logx.info(f"right {bottom_right}")

        # 在原始图像上绘制矩形框
        # cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
        # cv2.imshow("Match Result", image)
        # cv2.waitKey(0)

    if len(results) > 0:
        return results, True
    else:
        return [], False
        # 显示结果
        # cv2.imshow("Match Result", image)
        # cv2.waitKey(2000)
        # cv2.destroyAllWindows()

def mask():
    cardRoi = [[293, 565, 200, 40], [555, 565, 200, 40], [800, 565, 200, 40]]
    path = ['l', 'm', 'r']

    result = []
    # 第一个位置要是一个都没有就直接返回 False
    for i, roi in enumerate(cardRoi):
        # 定义目录路径
        directory = f"{IMG_PATH.joinpath(f'Main/worldTree/cards/{path[i]}')}"

        # 使用 glob 读取目录下的 .png 文件
        png_files = glob.glob(os.path.join(directory, "*.png"))
        for file in png_files:
            tempImg = MyImread(file)
            # imgSearchArea(img, tempImg,[(293,428),(293+135,428+30)])
            pots, ok = imgSearchArea(GetSnapShot(), tempImg, roi, 0.87)
            if ok:
                pot = pots[0]
                fName = file.split('/')[-1].split('.')[0]
                result.append({"pot": (pot[0], pot[1]), "name": fName})
                # 找到了就直接返回
                break


    return result

if __name__ == '__main__':

    ConnectEmulator()

    while True:
        UpdateSnapShot()
        img = GetSnapShot()
        imgG = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        temp = MyImread("point__975_417_80_23__925_367_180_123.png")
        tempG = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)

        # 设定亮度阈值（0-255，值越小，亮度要求越低）
        brightness_threshold = 100

        # 创建掩码：亮度低于阈值的区域为黑色，其余为白色
        mask = cv2.threshold(imgG, brightness_threshold, 255, cv2.THRESH_BINARY)[1]

        # 将掩码应用到原图上
        imgG = cv2.bitwise_and(imgG, imgG, mask=mask)

        res = find_all_template(imgG, tempG, threshold=0.75)
        #

        # res , ok = imgMultipleResultSearch(imgG, tempG)
        #
        # logx.info(f"ok :{ok}, res: {res}")

        for item in res:
            left = item['rectangle'][0]
            bottom = item['rectangle'][3]
            cv2.rectangle(img, left, bottom, (0, 255, 0), 2)

        cv2.imshow("png", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # 按 'q' 退出
            cv2.destroyAllWindows()
            break
        # while True:

