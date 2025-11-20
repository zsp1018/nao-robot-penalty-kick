# -*- coding: utf-8 -*-
#Zhang Shaopeng 11.4
from naoqi import ALProxy
from config import ROBOT_IP
robotIP =  ROBOT_IP
PORT = 9559

try:
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)

    motionProxy.wakeUp()


    print("start")
    postureProxy.goToPosture("SitRelax",1.2)#Sit down
    import time
    time.sleep(1)
    names = [
        "LHipRoll",
        "RHipRoll",
        "LKneePitch",
        "RKneePitch",
        "LAnkleRoll",
        "RAnkleRoll"
    ]
    angles = [
        1.0,
        -1.0,
        1.0,
        1.0,
        0.3,
        -0.3
    ]
    fractionMaxSpeed = 0.8
    motionProxy.setAngles(names, angles, fractionMaxSpeed)
    # 将睡眠时间从5秒改为3600秒（1小时）
    time.sleep(3600)
    # 如果你希望永久保持这个姿势，可以替换为：
    # while True:
    #     time.sleep(1)
    postureProxy.goToPosture("Sit", 0.5)
    motionProxy.rest()

except Exception as e:
    print("Error: ", e)
