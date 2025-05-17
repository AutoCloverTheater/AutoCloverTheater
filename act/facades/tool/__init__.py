import os
import shutil

import cv2
import numpy

from act.facades.Constant.Constant import ROOT_PATH
from act.facades.Logx.Logx import logx


def resize_image(img):
    # 读取图片
    if img is None:
        logx.exception("无法加载图片，请检查路径是否正确！")
        return

    # 获取图片的宽度和高度
    height, width = img.shape[:2]

    # 检查是否满足条件：宽高比为16:9且宽度大于1280
    if width / height == 16 / 9 and width > 1280:
        # 缩放到1280x720
        resized_img = cv2.resize(img, (1280, 720))
        # 保存缩放后的图片
        logx.info(f"图片已缩放为1280x720并保存到")
    else:
        logx.warning("图片不符合条件（宽高比不是16:9或宽度不大于1280），未进行缩放。")

def create_env_if_not_exists():
    # 定义文件路径
    env_file = ROOT_PATH.joinpath("etc/env.yaml")
    env_example_file = ROOT_PATH.joinpath("etc/env.yaml.example")

    # 检查 .env 文件是否存在
    if not os.path.exists(env_file):
        print(f"{env_file} 文件不存在，正在从 {env_example_file} 创建...")

        # 检查 .env.example 文件是否存在
        if os.path.exists(env_example_file):
            # 复制 .env.example 到 .env
            shutil.copyfile(env_example_file, env_file)
            print(f"{env_file} 文件已创建。")
        else:
            print(f"错误：{env_example_file} 文件不存在，无法创建 {env_file}。")
    else:
        print(f"{env_file} 文件已存在，无需创建。")

def cutImgByRoi(img, roi)-> numpy.array:
    x, y, w, h = roi
    return img[y:y+h, x:x+w]

if __name__ == '__main__':
    create_env_if_not_exists()