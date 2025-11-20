# coding:utf-8
# 导入OpenCV图像处理库
import cv2
# 导入NumPy数值计算库
import numpy as np
# 导入NAO机器人API和视觉定义模块
from naoqi import ALProxy
from config import ROBOT_IP, ROBOT_PORT
import vision_definitions
# 导入数学计算库
import math



#  基本参数设置
resolution = vision_definitions.kVGA  # 设置图像分辨率为VGA(640x480)
colorSpace = vision_definitions.kBGRColorSpace  # 设置色彩空间为BGR格式
fps = 5  # 设置帧率为5fps
frameHeight = 0  # 初始化帧高度
frameWidth = 0  # 初始化帧宽度
frameChannels = 0  # 初始化帧通道数
frameArray = None  # 初始化帧数组
cameraPitchRange = 47.64/180*math.pi  # 计算相机俯仰角范围（弧度）
cameraYawRange = 60.97/180*math.pi  # 计算相机偏航角范围（弧度）
ip = ROBOT_IP
# port = 9559  # 注释掉的端口号（默认为9559）

# 封装代理函数，用于创建与NAO机器人服务的连接
def get_Proxy(modelName, ip, port=9559):
    """
    创建并返回一个ALProxy实例
    参数:
        modelName: 要连接的服务名称
        ip: NAO机器人的IP地址
        port: 端口号，默认为9559
    返回:
        ALProxy实例
    """
    proxy = ALProxy(modelName, ip, port)
    return proxy

def get_image_from_camera(camera_id, camera_proxy, videoClient):
    """
    从相机获取图像帧
    参数:
        camera_id: 相机ID（0为顶部相机，1为底部相机）
        camera_proxy: 相机代理对象
        videoClient: 视频客户端对象
    返回:
        numpy数组形式的图像帧
    """
    # 获取图片, 一帧一帧组成视频流
    camera_proxy.setActiveCamera(camera_id)  # 设置活动相机

    # 返回的frame中， 第一维为图像的宽，第二维为图片的高，第三维为图片的通道数，第六维为图片本身数组
    frame = camera_proxy.getImageRemote(videoClient)
    frameWidth = frame[0]  # 获取图像宽度
    frameHeight = frame[1]  # 获取图像高度
    frameChannels = frame[2]  # 获取图像通道数

    # 将图片转换成numpy数组，并且reshape成标准的形状，方便我们使用cv2来展示
    frameArray = np.frombuffer(frame[6], dtype=np.uint8).reshape([frameHeight, frameWidth, frameChannels])
    return frameArray



if __name__ == '__main__':
    # 创建视频设备代理
    vd_proxy = get_Proxy("ALVideoDevice", ip)
    # 订阅视频服务
    videoClient = vd_proxy.subscribe("python_GVM", resolution, colorSpace, fps)
    # 持续获取并显示图像
    while 1:
        # 从底部相机获取图像
        img = get_image_from_camera(1, vd_proxy, videoClient)
        # 显示图像
        cv2.imshow("res", img)
        # 等待1ms，确保图像能够正常显示
        cv2.waitKe# coding:utf-8
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
        cv2.imshow("mask",mask)
        cv2.imshow("mask",imgResult)
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

