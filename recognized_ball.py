# coding:utf-8

import cv2
import numpy as np
from choose_color import *


# arr1 为底闸值， arr2为高闸值
def recognized(bgr_img, arr1, arr2):
    # 转换为HSV
    hue_image = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)

    # 用颜色分割图像
    #low_range = np.array([160, 83, 100])
    #high_range = np.array([180, 255, 255])
    low_range = np.array(arr1)
    high_range = np.array(arr2)

    th = cv2.inRange(hue_image, low_range, high_range)
    # cv2.imshow('result', th)
    # cv2.waitKey(0)

    # 平滑处理
    gaus = cv2.GaussianBlur(th, (7, 7), 1.5)
    # cv2.imshow('result', gaus)
    # cv2.waitKey(0)

    # 腐蚀
    eroded = cv2.erode(gaus, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4)), iterations=2)
    # cv2.imshow('result', eroded)
    # cv2.waitKey(0)

    # 膨胀
    dilated = cv2.dilate(eroded, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)
    # cv2.imshow('result', dilated)
    # cv2.waitKey(0)

    # Hough Circle
    circles = cv2.HoughCircles(dilated, cv2.cv.CV_HOUGH_GRADIENT, 1, 100, param1=15, param2=7, minRadius=15, maxRadius=100)

    center = None
    radius = None
    # 绘制
    if circles is not None:
        x, y, radius = circles[0][0]
        center = (x, y)
        cv2.circle(bgr_img, center, radius, (0, 255, 0), 2)

    return center, radius


def recognized_toBytes(bgr_img, arr1, arr2, arr3, arr4):
    # 转换为HSV
    hue_image = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)

    # 用颜色分割图像
    # low_range = np.array([160, 83, 100])
    # high_range = np.array([180, 255, 255])
    low_range = np.array(arr1)
    high_range = np.array(arr2)
    low_range2 = np.array(arr3)
    high_range2 = np.array(arr4)

    th = cv2.inRange(hue_image, low_range, high_range)
    th1 = cv2.inRange(hue_image, low_range2, high_range2)
    cv2.add(th, th1)
    # cv2.imshow('result', th)
    # cv2.waitKey(0)

    # 平滑处理
    gaus = cv2.GaussianBlur(th, (7, 7), 1.5)
    # cv2.imshow('result', gaus)
    # cv2.waitKey(0)

    # 腐蚀
    eroded = cv2.erode(gaus, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4)), iterations=2)
    # cv2.imshow('result', eroded)
    # cv2.waitKey(0)

    # 膨胀
    dilated = cv2.dilate(eroded, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)
    # cv2.imshow('result', dilated)
    # cv2.waitKey(0)
    return dilated


# arr1 为底闸值， arr2为高闸值
def recognized_contist(bgr_img, arr1, arr2, arr3, arr4):
    # dilated为一个经过平滑、腐蚀、膨胀后的图片
    dilated1 = recognized_toBytes(bgr_img, arr1, arr2, arr3, arr4)

    # dilated2 = recognized_toBytes(bgr_img, arr3, arr4)
    # dilated = contist(dilated1, dilated2)
    # eroded = cv2.erode(dilated1, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4)), iterations=2)

    # Hough Circle
    circles = cv2.HoughCircles(dilated1, cv2.cv.CV_HOUGH_GRADIENT, 1, 100, param1=15, param2=7, minRadius=15, maxRadius=100)

    center = None
    radius = None
    # 绘制
    if circles is not None:
        x, y, radius = circles[0][0]
        center = (x, y)
    cv2.circle(bgr_img, center, radius, (0, 255, 0), 2)
    # 返回圆心坐标以及半径
    return center, radius

#white_low = [0, 4, 99]
#white_high = [48, 255, 255]
#black_low = [0, 0, 0]
#black_high = [179, 255, 92]
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)

    while 1:
        success, img = cap.read()
        recognized_contist(img, white_low, white_high, black_low, black_high)
        cv2.imshow("res", img)
        cv2.waitKey(1)
