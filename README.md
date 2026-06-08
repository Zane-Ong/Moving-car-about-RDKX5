# Moving-car-about-ROS2

基于地瓜机器人 RDK X5 与 ROS2 的智能移动服务小车项目。仓库包含运行在 RDK X5 上的 ROS2 上位机工作空间、运行在下位机 C 板上的 Keil/MDK-ARM 固件工程，以及 SolidWorks 机械结构模型。

本项目面向移动服务场景，围绕“小车自主移动、传感器融合、建图导航、视觉药品检测、行为树任务编排、下位机运动控制”构建完整的软件与硬件资料。

## 项目亮点

- RDK X5 作为上位机计算平台，负责 ROS2 节点运行、传感器数据处理、导航规划与视觉检测。
- ROS2 工作空间按功能拆分为底盘、IMU、雷达、导航、RViz、机器人描述、行为树和业务功能包。
- 支持 ORadar MS200 激光雷达接入，提供雷达扫描、可视化与建图启动文件。
- 支持 Cartographer、GMapping、SLAM Toolbox 等建图流程，并提供已有 `service_map` 地图文件。
- 支持 Nav2/DWB 导航流程，可用于室内移动服务任务。
- 支持摄像头药瓶检测，检测药瓶数量变化并通过 ROS2 话题发布业务状态。
- 下位机工程提供 C 板底层控制逻辑，可通过 Keil 5 / MDK-ARM 打开、编译和烧录。
- 提供 SolidWorks 2025 机械模型，便于结构查看、修改和二次加工。

## 硬件平台

### RDK X5 上位机

RDK X5 是整车的高层计算核心，主要负责：

- 运行 ROS2 工作空间 `service_car`
- 接收雷达、IMU、摄像头、下位机串口等数据
- 发布 `/cmd_vel`、里程计、TF、IMU、雷达扫描等 ROS2 消息
- 运行 SLAM、定位、路径规划、运动控制和行为树任务
- 运行 OpenCV 药瓶检测逻辑，并输出任务状态话题

### 下位机 C 板

下位机负责更靠近硬件的实时控制，包括：

- 电机驱动与速度控制
- 编码器/轮速等底层数据采集
- 与 RDK X5 通过串口通信
- 执行上位机发送的运动控制指令
- 维护底盘底层运行逻辑

### 传感器与外设

仓库代码中涉及的主要外设包括：

- ORadar MS200 激光雷达
- IMU 模块
- USB 摄像头，默认设备路径为 `/dev/video2`
- 移动底盘电机与 C 板控制系统

## 仓库结构

```text
.
├── 上位机代码/
│   └── 上位机代码/service_car/src/
│       ├── BT_ros2/                  # ROS2 行为树任务编排
│       ├── car_base_node/            # 底盘速度、里程计和串口通信节点
│       ├── car_bringup/              # 整车启动、EKF 参数和 bringup launch
│       ├── car_ctrl/                 # 键盘/遥控控制节点
│       ├── car_description/          # 小车 URDF/模型描述
│       ├── car_function/             # 药品检测、角度校正等业务功能
│       ├── car_imu_node/             # IMU 数据读取与发布
│       ├── car_nav/                  # 建图、导航、地图和 RViz 配置
│       ├── car_rviz/                 # RViz 显示相关配置
│       ├── nav2_bringup/             # Nav2 启动与配置
│       ├── oradar_ros/               # ORadar 激光雷达 ROS 驱动
│       └── turtlebot3_cartographer/  # Cartographer 相关配置
├── 下位机代码/
│   └── 下位机代码/C板 code/
│       ├── application/              # 下位机应用层代码
│       ├── bsp/                      # 板级支持包
│       ├── Drivers/                  # HAL/CMSIS 等驱动
│       ├── Inc/                      # 头文件
│       ├── Src/                      # 源文件
│       ├── MDK-ARM/                  # Keil 工程
│       └── can.ioc                   # STM32CubeMX 工程配置
├── 模型/
│   └── 模型/                         # SolidWorks 2025 机械模型
├── 上位机代码 .zip
├── 下位机代码.zip
├── 模型.zip
└── readme.txt
```

## ROS2 功能包说明

| 功能包 | 作用 |
| --- | --- |
| `car_bringup` | 整车启动入口，组合底盘、IMU、小车描述等节点 |
| `car_base_node` | 处理底盘串口通信、轮速数据、里程计发布和 TF 发布 |
| `car_ctrl` | 提供键盘控制入口 `car_ctrl_keyboard` |
| `car_imu_node` | 读取 IMU 数据并发布 ROS2 IMU 话题 |
| `car_nav` | 提供建图、地图保存、DWB/Nav2 导航等 launch 文件 |
| `oradar_ros` | ORadar MS200 激光雷达 ROS 驱动与可视化配置 |
| `car_function` | 药瓶检测、角度校正等业务逻辑 |
| `BT_ros2` | 基于 BehaviorTree.CPP / Nav2 行为树的任务编排 |
| `car_description` | 小车模型描述，用于 TF、RViz 和导航显示 |
| `car_rviz` | RViz 可视化配置 |
| `nav2_bringup` | Nav2 导航启动配置 |
| `turtlebot3_cartographer` | Cartographer 建图相关配置 |

## 环境准备

建议在 RDK X5 上准备以下环境：

- Ubuntu / RDK 官方系统环境
- ROS2，建议使用与 RDK X5 系统匹配的发行版
- `colcon` 构建工具
- Python 3
- OpenCV Python 绑定
- Nav2、Cartographer、robot_localization、imu_filter_madgwick 等 ROS2 依赖
- ORadar MS200 对应串口/USB 权限规则

常用依赖安装示例：

```bash
sudo apt update
sudo apt install -y python3-colcon-common-extensions python3-opencv
sudo apt install -y ros-$ROS_DISTRO-navigation2 ros-$ROS_DISTRO-nav2-bringup
sudo apt install -y ros-$ROS_DISTRO-robot-localization
```

如果系统未配置 `$ROS_DISTRO`，请将命令中的 `$ROS_DISTRO` 替换为实际 ROS2 版本名。

## 编译上位机 ROS2 工作空间

进入 RDK X5 上的 ROS2 工作空间：

```bash
cd 上位机代码/上位机代码/service_car
source /opt/ros/$ROS_DISTRO/setup.bash
colcon build --symlink-install
source install/setup.bash
```

如果部分包依赖未安装，先根据终端提示安装对应 ROS2 包，再重新执行 `colcon build`。

## 运行整车 Bringup

整车基础启动入口：

```bash
cd 上位机代码/上位机代码/service_car
source install/setup.bash
ros2 launch car_bringup car_bringup.launch.py
```

该 launch 当前会启动：

- `car_bringup` 中的 `car_driver`
- `car_base_node` 中的 `speed_node`
- `car_base_node` 中的 `base_node`
- `car_imu_node` 的 IMU 启动文件
- `car_description` 小车模型描述

代码中预留了 EKF 融合和遥控控制入口，可按实际调试情况在 `car_bringup.launch.py` 中启用。

## 底盘与里程计

`car_base_node` 包含：

- `base_node.py`
- `speed_node.py`
- `uart.py`

主要功能：

- 与下位机 C 板进行串口通信
- 接收或解析四轮速度数据
- 发布 `vel_raw`
- 根据轮速计算里程计
- 发布 `odom`
- 发布 `odom -> base_footprint` TF

单独运行示例：

```bash
ros2 run car_base_node speed_node
ros2 run car_base_node base_node
```

## IMU 数据

`car_imu_node` 用于读取 IMU 并发布 ROS2 消息，包内包含 USB 绑定脚本和 udev 规则：

- `bind_usb.sh`
- `imu_usb.rules`
- `car_imu_node.py`
- `imu_raw_pub.py`

运行示例：

```bash
ros2 launch car_imu_node rviz_and_imu.launch.py
```

如果设备名不固定，建议先配置 udev 规则，再重新插拔 IMU 设备。

## 雷达与建图

ORadar MS200 雷达包位于：

```text
上位机代码/上位机代码/service_car/src/oradar_ros
```

常用启动文件：

```bash
ros2 launch oradar_ros ms200_scan.launch.py
ros2 launch oradar_ros ms200_scan_view.launch.py
```

`car_nav` 提供多种建图启动方式：

```bash
ros2 launch car_nav cartographer_launch.py
ros2 launch car_nav map_cartographer_launch.py
ros2 launch car_nav map_gmapping_launch.py
ros2 launch car_nav map_slam_toolbox_launch.py
```

保存地图：

```bash
ros2 launch car_nav save_map_launch.py
```

仓库中已包含地图文件：

```text
上位机代码/上位机代码/service_car/src/car_nav/maps/service_map.yaml
上位机代码/上位机代码/service_car/src/car_nav/maps/service_map.pgm
上位机代码/上位机代码/service_car/src/car_nav/maps/service_map.pbstream
```

## 导航功能

导航相关启动文件位于：

```text
上位机代码/上位机代码/service_car/src/car_nav/launch
```

常用入口：

```bash
ros2 launch car_nav navigation2_cartographer.launch.py
ros2 launch car_nav navigation_dwb_launch.py
ros2 launch car_nav nav_dwb_time_launch.py
```

导航功能主要包括：

- 地图加载
- 机器人定位
- 全局路径规划
- DWB 局部规划
- 速度指令输出
- RViz 导航目标点交互

## 键盘控制

`car_ctrl` 提供键盘控制入口：

```bash
ros2 launch car_ctrl car_ctrl.launch.py
```

或直接运行：

```bash
ros2 run car_ctrl car_ctrl_keyboard
```

该功能适合底盘调试、传感器联调和导航前的基础运动验证。

## 药品检测功能

药品检测节点位于：

```text
上位机代码/上位机代码/service_car/src/car_function/car_function/medicinedetect.py
```

运行入口：

```bash
ros2 run car_function medicinedetect
```

功能逻辑：

- 等待摄像头设备 `/dev/video2`
- 使用 OpenCV 读取 1280x720 图像
- 基于 HSV 白色阈值、轮廓圆度和霍夫圆检测识别药瓶
- 统计画面中的药瓶数量
- 初始化阶段记录基准数量
- 当检测到数量减少并持续确认后，发布 `DYF` 话题，表示药瓶已被拿走
- 如果确认失败，发布 `DYFSB` 话题，表示药瓶未被拿走或检测失败

发布话题：

| 话题 | 消息类型 | 含义 |
| --- | --- | --- |
| `DYF` | `std_msgs/String` | 药瓶已被拿走 |
| `DYFSB` | `std_msgs/String` | 药瓶识别失败或状态未满足 |

注意：摄像头设备路径目前写死为 `/dev/video2`，如实际设备不同，需要在代码中修改对应路径。

## 角度校正功能

`car_function` 中还包含：

- `AngleCorrectionNode.py`
- `Correctangle.py`

这部分用于小车姿态/角度校正类业务逻辑，可配合 IMU、里程计或导航任务使用。

运行示例：

```bash
ros2 run car_function AngleCorrectionNode
ros2 run car_function Correctangle
```

## 行为树任务编排

`BT_ros2` 基于 `behaviortree_cpp_v3`、`nav2_behavior_tree` 和 `nav2_msgs`，用于把导航、等待、快照、自动对接等动作组织成任务流程。

行为树 XML 位于：

```text
上位机代码/上位机代码/service_car/src/BT_ros2/bt_xml
```

启动示例：

```bash
ros2 launch BT_ros2 bt_ros2.launch.py
```

包内可执行文件：

- `bt_ros2`
- `send_goal`

## 下位机工程

下位机代码位于：

```text
下位机代码/下位机代码/C板 code
```

打开方式：

1. 安装 Keil 5 / MDK-ARM。
2. 进入 `MDK-ARM` 目录。
3. 打开对应 `.uvprojx` 工程文件。
4. 编译工程并烧录到 C 板。

工程同时包含 `can.ioc`，可使用 STM32CubeMX 查看外设配置。

下位机主要承担底层实时控制任务，上位机通过串口与其通信，实现速度控制、轮速反馈和底盘状态同步。

## 机械模型

机械结构模型位于：

```text
模型/模型
```

主要文件包括：

- `小车.SLDASM`
- `小车.SLDPRT`
- `上顶2.SLDASM`
- `铰链.SLDASM`
- 雷达、摄像头、电池、底板、侧板、门板、轮挡等零部件模型

建议使用 SolidWorks 2025 或兼容版本打开。仓库中也包含部分 `.STEP` / `.stp` 文件，便于在其他 CAD 软件中查看和转换。

## 推荐调试流程

1. 先烧录下位机 C 板工程，确认电机和底层通信正常。
2. 在 RDK X5 上编译 `service_car` ROS2 工作空间。
3. 单独运行底盘节点，确认串口、轮速和 `/cmd_vel` 控制正常。
4. 接入 IMU，确认 IMU 话题发布正常。
5. 接入 ORadar MS200 雷达，确认 `/scan` 数据正常。
6. 启动 RViz，检查 TF、机器人模型、雷达点云/扫描和里程计。
7. 运行建图 launch，生成或验证地图。
8. 启动导航 launch，在 RViz 中下发目标点。
9. 运行 `medicinedetect`，确认摄像头、药瓶检测和 `DYF` / `DYFSB` 话题发布。
10. 根据任务需求启用行为树，实现完整服务流程。

## 常见问题

### 找不到摄像头

药品检测默认使用 `/dev/video2`。可先执行：

```bash
ls /dev/video*
```

如果实际设备不是 `/dev/video2`，请修改 `medicinedetect.py` 中的设备路径。

### 找不到 IMU 或雷达串口

检查设备权限：

```bash
ls /dev/ttyUSB*
ls /dev/ttyACM*
```

必要时复制包内 udev 规则，并重新加载：

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

### ROS2 包无法编译

先确认已 source ROS2 环境：

```bash
source /opt/ros/$ROS_DISTRO/setup.bash
```

再安装缺失依赖后重新构建：

```bash
colcon build --symlink-install
```

### 导航时机器人模型或 TF 异常

建议检查：

- `car_description` 是否正常启动
- `odom`、`base_footprint`、`base_link`、`laser` 等 frame 是否一致
- IMU、里程计、雷达话题是否正常发布
- EKF 参数是否与实际话题匹配

## 适用场景

本项目适合用于：

- RDK X5 嵌入式 AI/机器人开发
- ROS2 移动机器人课程设计
- 室内服务小车原型开发
- 雷达 SLAM 与 Nav2 导航实验
- 视觉检测与移动机器人业务联动
- 嵌入式芯片设计竞赛作品资料整理

## 说明

本仓库当前以作品源码与模型资料归档为主，部分路径和设备名与实际硬件绑定较强。移植到其他小车或开发板时，请根据实际串口号、摄像头编号、雷达型号、底盘尺寸和 ROS2 发行版进行调整。
