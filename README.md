# NAO足球机器人控制系统

## 项目概述

这是一个基于Python开发的NAO机器人足球控制系统，利用OpenCV实现视觉识别功能，结合NAOqi API控制机器人进行足球比赛中的各种动作，如寻球、定位、行走和踢球等。
<p align="center">
  <img src="kick.gif" alt="动作演示">  <img src="keepdoor.gif" alt="动作演示">
</p>


## 功能特点

- **视觉识别**：使用OpenCV进行足球识别和跟踪
- **运动控制**：控制NAO机器人的行走、转身和踢球动作
- **位置感知**：根据摄像头反馈调整机器人位置和姿态
- **模块化设计**：代码结构清晰，便于维护和扩展

## 系统架构

项目主要包含以下几个核心模块：

- **视觉处理模块**：负责图像采集和足球识别
- **运动控制模块**：控制机器人的各种动作
- **策略决策模块**：根据识别结果决定下一步行动
- **配置管理模块**：集中管理IP地址等配置参数

## 目录结构
├── config.py # 配置文件，包含机器人IP和端口设置 ├── control_NAO.py # NAO机器人控制模块 ├── choose_color.py # 颜色选择和调试工具 ├── recognized_ball.py # 足球识别核心算法 ├── proxy_and_image.py # 代理和图像处理模块 ├── mainleft.py # 踢左边主程序 ├── mainright.py # 踢右边主程序 ├── main_middle.py # 踢中间主程序 ├── keepdoor.py # 守门员功能模块 ├── opencv.ipynb # OpenCV测试笔记本 ├── ball.jpg # 识别示例图片 ├── ball_right.jpg # 右侧识别示例图片 └── README.md

## 依赖要求

- Python 2.x
- OpenCV (cv2)
- NumPy
- NAOqi Python SDK

## 安装说明

1. 安装Python 2.x环境
2. 安装必要的Python库：
   ```bash
   pip install opencv-python numpy
   ```
3. 安装NAOqi Python SDK（可从SoftBank Robotics官方网站下载）
4. 克隆本仓库到本地

## 使用方法

1. 修改`config.py`文件中的机器人IP地址，设置为您的NAO机器人实际IP：
   ```python
   ROBOT_IP = "192.168.1.x"  # 替换为您的机器人IP
   ```

2. 根据比赛位置需求运行相应的主程序：
   - 左侧位置：
     ```bash
     python mainleft.py
     ```
   - 右侧位置：
     ```bash
     python mainright.py
     ```
   - 中间位置：
     ```bash
     python main_middle.py
     ```

## 颜色调试

如果需要调整足球识别的颜色参数，可以运行颜色调试工具：

```bash
python choose_color.py
```

## 主要功能说明

1. **足球识别**：使用Hough圆变换和颜色阈值过滤识别足球
2. **位置调整**：根据足球在画面中的位置调整机器人移动方向
3. **踢球动作**：当足球位于合适位置时执行踢球动作
4. **自动导航**：在未识别到足球时进行探索移动

## 注意事项

- 确保NAO机器人已连接到与计算机相同的网络
- 调整光线条件以获得最佳的足球识别效果
- 根据实际场地情况可能需要微调识别参数
- 初次运行前请确保机器人有足够的活动空间

## 贡献指南

欢迎提交Issue和Pull Request来帮助改进这个项目！

## 许可证

本项目采用MIT许可证。详情请参阅LICENSE文件。
