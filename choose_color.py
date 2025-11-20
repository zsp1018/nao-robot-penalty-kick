# coding:utf-8
"""
本代码主要用于图像的颜色掩膜处理，通过HSV颜色空间中的阈值来提取特定颜色范围。
包含滑动条交互功能，可以动态调整颜色参数来选择特定颜色。
同时包含了处理黑白两个颜色范围的示例代码。
"""

# 导入所需库
import numpy as np
import cv2
from recognized_ball import *
from mainright import *


# 定义空的回调函数，用于滑动条
def empty(a):
    pass


print("Package Imported")

# 设置图片路径
path = "./soccer.jpg"


def choose_color_1():
    """
    创建滑动条来调整HSV颜色空间的阈值，实时显示掩膜效果
    可以通过滑动条动态调整H(色相)、S(饱和度)、V(明度)的最小值和最大值
    """
    # 创建滑动条窗口
    cv2.namedWindow("TrackBars")
    cv2.resizeWindow("TrackBars", 640, 240)

    # 创建六个滑动条，分别控制HSV三个通道的最小值和最大值
    cv2.createTrackbar("Hue Min", "TrackBars", 0, 179, empty)
    cv2.createTrackbar("Hue Max", "TrackBars", 179, 179, empty)
    cv2.createTrackbar("Sat Min", "TrackBars", 0, 255, empty)
    cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, empty)
    cv2.createTrackbar("Val Min", "TrackBars", 0, 255, empty)
    cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)

    while True:
        # 读取并调整图片大小
        img = cv2.imread(path)
        imgRe = cv2.resize(img, (0, 0), None, 0.5, 0.5)

        # 将图片从BGR转换到HSV颜色空间
        imgHSV = cv2.cvtColor(imgRe, cv2.COLOR_BGR2HSV)

        # 获取滑动条的当前位置
        h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
        s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
        s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
        h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
        v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
        v_max = cv2.getTrackbarPos("Val Max", "TrackBars")

        # 打印当前阈值
        print(h_min, h_max, s_min, s_max, v_min, v_max)

        # 创建颜色范围的下限和上限
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])

        # 创建掩膜，只保留指定颜色范围内的像素
        mask = cv2.inRange(imgHSV, lower, upper)

        # 使用掩膜进行位与操作，获取结果图像
        imgResult = cv2.bitwise_and(imgRe, imgRe, mask=mask)

        # 显示各个图像
        cv2.imshow("Output", imgRe)
        cv2.imshow("Output1", imgHSV)
        cv2.imshow("mask", mask)
        cv2.imshow("mask", imgResult)
        cv2.waitKey(1)


def contist(img1, img2):
    """
    组合两个二值图像
    将两个二值图像相加，并将大于1的值设为1
    """
    res = img1 + img2
    for i in res:
        for j in i:
            if j > 1:
                j = 1
    return res


# 主程序入口
if __name__ == '__main__':
    # 读取图片
    img = cv2.imread(path)

    # 识别白色和黑色区域
    res1 = recognized_toBytes(img, white_low, white_high)
    res2 = recognized_toBytes(img, black_low, black_high)

    # 组合两个识别结果
    res = contist(res1, res2)

    # 显示结果
    cv2.imshow("res", res)
    cv2.waitKey(0)

    # 注释掉的choose_color_1()函数调用，如需使用可取消注释
    # choose_color_1()
