# coding:utf-8

from proxy_and_image import *
from config import ROBOT_IP  # 导入统一IP
# 移动角度
def change_the_postion(mt_proxy, name, targetAngles):
    mt_proxy.angleInterpolationWithSpeed(name, targetAngles, 0.2)
    return True


if __name__ == '__main__':
    ip = ROBOT_IP  # 使用统一IP
    mt_proxy = get_Proxy("ALMotion", ip)
    mt_proxy.moveTo(0.4, 0, 0)

