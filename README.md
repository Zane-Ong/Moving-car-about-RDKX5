# Moving-car-about-RDKX5

An intelligent mobile service robot car project based on the D-Robotics RDK X5 and ROS2.

This repository contains the ROS2 host workspace running on the RDK X5, the Keil/MDK-ARM firmware project running on the lower-level C board, and SolidWorks mechanical structure models.

The project targets mobile service robot scenarios and provides software and hardware resources for autonomous movement, sensor fusion, mapping and navigation, visual medicine-bottle detection, behavior-tree task orchestration, and lower-level motion control.

## Highlights

- Uses the RDK X5 as the upper-level computing platform for ROS2 nodes, sensor data processing, navigation planning, and visual detection.
- Organizes the ROS2 workspace into packages for the chassis, IMU, lidar, navigation, RViz, robot description, behavior trees, and application functions.
- Supports ORadar MS200 lidar access, including scan publishing, visualization, and mapping launch files.
- Supports mapping workflows based on Cartographer, GMapping, and SLAM Toolbox, and includes an existing `service_map` map.
- Supports Nav2/DWB navigation for indoor mobile service tasks.
- Supports camera-based medicine-bottle detection, detects changes in bottle count, and publishes service status through ROS2 topics.
- Provides lower-level C-board control logic that can be opened, built, and flashed with Keil 5 / MDK-ARM.
- Provides SolidWorks 2025 mechanical models for structure review, modification, and secondary fabrication.

## Hardware Platform

### RDK X5 Host

The RDK X5 is the high-level computing core of the vehicle. It is responsible for:

- Running the ROS2 workspace `service_car`.
- Receiving data from the lidar, IMU, camera, and lower-level controller serial port.
- Publishing ROS2 messages such as `/cmd_vel`, odometry, TF, IMU, and lidar scan data.
- Running SLAM, localization, path planning, motion control, and behavior-tree tasks.
- Running OpenCV-based medicine-bottle detection and publishing task status topics.

### Lower-Level C Board

The lower-level controller handles real-time hardware control, including:

- Motor driving and speed control.
- Encoder and wheel-speed data acquisition.
- Serial communication with the RDK X5.
- Execution of motion-control commands sent by the host.
- Maintenance of low-level chassis runtime logic.

### Sensors and Peripherals

The main peripherals involved in this repository include:

- ORadar MS200 lidar.
- IMU module.
- USB camera, with the default device path set to `/dev/video2`.
- Mobile chassis motors and the C-board control system.

## Repository Structure

```text
.
├── 上位机代码/
│   └── 上位机代码/service_car/src/
│       ├── BT_ros2/                  # ROS2 behavior-tree task orchestration
│       ├── car_base_node/            # Chassis speed, odometry, and serial communication nodes
│       ├── car_bringup/              # Full-vehicle bringup, EKF parameters, and launch files
│       ├── car_ctrl/                 # Keyboard / remote-control nodes
│       ├── car_description/          # Robot URDF and model description
│       ├── car_function/             # Medicine detection, angle correction, and service logic
│       ├── car_imu_node/             # IMU data reading and publishing
│       ├── car_nav/                  # Mapping, navigation, maps, and RViz configuration
│       ├── car_rviz/                 # RViz visualization configuration
│       ├── nav2_bringup/             # Nav2 launch and configuration files
│       ├── oradar_ros/               # ORadar lidar ROS driver
│       └── turtlebot3_cartographer/  # Cartographer-related configuration
├── 下位机代码/
│   └── 下位机代码/C板/code/
│       ├── application/              # Lower-level application code
│       ├── bsp/                      # Board support package
│       ├── Drivers/                  # HAL / CMSIS drivers
│       ├── Inc/                      # Header files
│       ├── Src/                      # Source files
│       ├── MDK-ARM/                  # Keil project
│       └── can.ioc                   # STM32CubeMX project configuration
├── 模型/
│   └── 模型/                         # SolidWorks 2025 mechanical models
├── 上位机代码.zip
├── 下位机代码.zip
├── 模型.zip
└── readme.txt
```

## ROS2 Packages

| Package | Description |
| --- | --- |
| `car_bringup` | Main bringup entry point that combines the chassis, IMU, robot description, and related nodes. |
| `car_base_node` | Handles chassis serial communication, wheel-speed data, odometry publishing, and TF publishing. |
| `car_ctrl` | Provides the keyboard-control entry point `car_ctrl_keyboard`. |
| `car_imu_node` | Reads IMU data and publishes ROS2 IMU topics. |
| `car_nav` | Provides launch files for mapping, map saving, DWB/Nav2 navigation, and related workflows. |
| `oradar_ros` | ROS driver and visualization configuration for the ORadar MS200 lidar. |
| `car_function` | Service logic such as medicine-bottle detection and angle correction. |
| `BT_ros2` | Task orchestration based on BehaviorTree.CPP / Nav2 behavior trees. |
| `car_description` | Robot model description used by TF, RViz, and navigation visualization. |
| `car_rviz` | RViz visualization configuration. |
| `nav2_bringup` | Nav2 navigation launch configuration. |
| `turtlebot3_cartographer` | Cartographer mapping configuration. |

## Environment Setup

Prepare the following environment on the RDK X5:

- Ubuntu or the official RDK system environment.
- ROS2, preferably a distribution that matches the RDK X5 system.
- `colcon` build tools.
- Python 3.
- OpenCV Python bindings.
- ROS2 dependencies such as Nav2, Cartographer, `robot_localization`, and `imu_filter_madgwick`.
- Serial / USB permission rules for the ORadar MS200.

Common dependency installation example:

```bash
sudo apt update
sudo apt install -y python3-colcon-common-extensions python3-opencv
sudo apt install -y ros-$ROS_DISTRO-navigation2 ros-$ROS_DISTRO-nav2-bringup
sudo apt install -y ros-$ROS_DISTRO-robot-localization
```

If `$ROS_DISTRO` is not configured on your system, replace `$ROS_DISTRO` in the commands with the actual ROS2 distribution name.

## Build the ROS2 Workspace

Enter the ROS2 workspace on the RDK X5:

```bash
cd 上位机代码/上位机代码/service_car
source /opt/ros/$ROS_DISTRO/setup.bash
colcon build --symlink-install
source install/setup.bash
```

If some packages fail because dependencies are missing, install the corresponding ROS2 packages according to the terminal output and then run `colcon build` again.

## Run Full-Vehicle Bringup

Basic full-vehicle bringup:

```bash
cd 上位机代码/上位机代码/service_car
source install/setup.bash
ros2 launch car_bringup car_bringup.launch.py
```

This launch file currently starts:

- `car_driver` from `car_bringup`.
- `speed_node` from `car_base_node`.
- `base_node` from `car_base_node`.
- The IMU launch file from `car_imu_node`.
- The robot description from `car_description`.

The code reserves entries for EKF fusion and remote-control logic. These can be enabled in `car_bringup.launch.py` according to the actual debugging status.

## Chassis and Odometry

The `car_base_node` package includes:

- `base_node.py`
- `speed_node.py`
- `uart.py`

Main functions:

- Communicates with the lower-level C board through the serial port.
- Receives or parses four-wheel speed data.
- Publishes `vel_raw`.
- Computes odometry based on wheel speed.
- Publishes `odom`.
- Publishes the `odom -> base_footprint` TF transform.

Run nodes separately:

```bash
ros2 run car_base_node speed_node
ros2 run car_base_node base_node
```

## IMU Data

`car_imu_node` reads IMU data and publishes ROS2 messages. The package includes USB binding scripts and udev rules:

- `bind_usb.sh`
- `imu_usb.rules`
- `car_imu_node.py`
- `imu_raw_pub.py`

Run example:

```bash
ros2 launch car_imu_node rviz_and_imu.launch.py
```

If the device name is not stable, configure the udev rules first and then reconnect the IMU device.

## Lidar and Mapping

The ORadar MS200 lidar package is located at:

```text
上位机代码/上位机代码/service_car/src/oradar_ros
```

Common launch files:

```bash
ros2 launch oradar_ros ms200_scan.launch.py
ros2 launch oradar_ros ms200_scan_view.launch.py
```

`car_nav` provides multiple mapping launch options:

```bash
ros2 launch car_nav cartographer_launch.py
ros2 launch car_nav map_cartographer_launch.py
ros2 launch car_nav map_gmapping_launch.py
ros2 launch car_nav map_slam_toolbox_launch.py
```

Save a map:

```bash
ros2 launch car_nav save_map_launch.py
```

The repository already includes map files:

```text
上位机代码/上位机代码/service_car/src/car_nav/maps/service_map.yaml
上位机代码/上位机代码/service_car/src/car_nav/maps/service_map.pgm
上位机代码/上位机代码/service_car/src/car_nav/maps/service_map.pbstream
```

## Navigation

Navigation launch files are located in:

```text
上位机代码/上位机代码/service_car/src/car_nav/launch
```

Common entries:

```bash
ros2 launch car_nav navigation2_cartographer.launch.py
ros2 launch car_nav navigation_dwb_launch.py
ros2 launch car_nav nav_dwb_time_launch.py
```

The navigation workflow mainly includes:

- Map loading.
- Robot localization.
- Global path planning.
- DWB local planning.
- Velocity command output.
- Navigation goal interaction in RViz.

## Keyboard Control

`car_ctrl` provides a keyboard-control entry point:

```bash
ros2 launch car_ctrl car_ctrl.launch.py
```

Or run it directly:

```bash
ros2 run car_ctrl car_ctrl_keyboard
```

This function is suitable for chassis debugging, sensor integration testing, and basic motion verification before running navigation.

## Medicine-Bottle Detection

The medicine-bottle detection node is located at:

```text
上位机代码/上位机代码/service_car/src/car_function/car_function/medicinedetect.py
```

Run entry:

```bash
ros2 run car_function medicinedetect
```

Main logic:

- Waits for the camera device `/dev/video2`.
- Reads 1280x720 images with OpenCV.
- Detects medicine bottles based on HSV white thresholding, contour circularity, and Hough circle detection.
- Counts the number of medicine bottles in the image.
- Records a baseline count during initialization.
- Publishes the `DYF` topic after a confirmed decrease in bottle count, indicating that a medicine bottle has been taken.
- Publishes the `DYFSB` topic when confirmation fails, indicating that the bottle was not taken or detection failed.

Published topics:

| Topic | Message Type | Meaning |
| --- | --- | --- |
| `DYF` | `std_msgs/String` | The medicine bottle has been taken. |
| `DYFSB` | `std_msgs/String` | Medicine-bottle recognition failed or the status condition was not satisfied. |

Note: The camera device path is currently hard-coded as `/dev/video2`. If the actual device is different, update the corresponding path in `medicinedetect.py`.

## Angle Correction

`car_function` also includes:

- `AngleCorrectionNode.py`
- `Correctangle.py`

These files implement car attitude / angle-correction logic and can be used together with the IMU, odometry, or navigation tasks.

Run examples:

```bash
ros2 run car_function AngleCorrectionNode
ros2 run car_function Correctangle
```

## Behavior-Tree Task Orchestration

`BT_ros2` is based on `behaviortree_cpp_v3`, `nav2_behavior_tree`, and `nav2_msgs`. It is used to organize navigation, waiting, snapshot, automatic docking, and other actions into task workflows.

Behavior-tree XML files are located at:

```text
上位机代码/上位机代码/service_car/src/BT_ros2/bt_xml
```

Launch example:

```bash
ros2 launch BT_ros2 bt_ros2.launch.py
```

Executables in the package:

- `bt_ros2`
- `send_goal`

## Lower-Level Firmware Project

The lower-level code is located at:

```text
下位机代码/下位机代码/C板/code
```

Open and build the project:

1. Install Keil 5 / MDK-ARM.
2. Enter the `MDK-ARM` directory.
3. Open the corresponding `.uvprojx` project file.
4. Build the project and flash it to the C board.

The project also includes `can.ioc`, which can be opened with STM32CubeMX to inspect peripheral configuration.

The lower-level controller mainly handles real-time chassis control. The host communicates with it through the serial port to implement speed control, wheel-speed feedback, and chassis status synchronization.

## Mechanical Models

The mechanical structure models are located at:

```text
模型/模型
```

Main files include:

- `小车.SLDASM`
- `小车.SLDPRT`
- `上顶2.SLDASM`
- `铰链.SLDASM`
- Models for the lidar, camera, battery, base plate, side plates, door plates, wheel guards, and other components.

SolidWorks 2025 or a compatible version is recommended. The repository also includes some `.STEP` / `.stp` files for viewing or conversion in other CAD software.

## Recommended Debugging Workflow

1. Flash the lower-level C-board project first and confirm that the motors and low-level communication work correctly.
2. Build the `service_car` ROS2 workspace on the RDK X5.
3. Run the chassis nodes separately and confirm that the serial port, wheel speed, and `/cmd_vel` control work correctly.
4. Connect the IMU and confirm that the IMU topic is published correctly.
5. Connect the ORadar MS200 lidar and confirm that `/scan` data is normal.
6. Start RViz and check TF, the robot model, lidar scan points, and odometry.
7. Run the mapping launch file to create or verify a map.
8. Start the navigation launch file and send target poses in RViz.
9. Run `medicinedetect` and confirm camera access, bottle detection, and `DYF` / `DYFSB` topic publishing.
10. Enable the behavior tree according to the task requirements to complete the full service workflow.

## Common Issues

### Camera Not Found

Medicine-bottle detection uses `/dev/video2` by default. Check available devices first:

```bash
ls /dev/video*
```

If the actual device is not `/dev/video2`, update the device path in `medicinedetect.py`.

### IMU or Lidar Serial Port Not Found

Check device permissions:

```bash
ls /dev/ttyUSB*
ls /dev/ttyACM*
```

If needed, copy the udev rules included in the package and reload them:

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

### ROS2 Package Build Failure

First confirm that the ROS2 environment has been sourced:

```bash
source /opt/ros/$ROS_DISTRO/setup.bash
```

Then install the missing dependencies and rebuild:

```bash
colcon build --symlink-install
```

### Robot Model or TF Is Abnormal During Navigation

Check the following:

- Whether `car_description` starts correctly.
- Whether frames such as `odom`, `base_footprint`, `base_link`, and `laser` are consistent.
- Whether the IMU, odometry, and lidar topics are published normally.
- Whether EKF parameters match the actual topic names and frame settings.

## Use Cases

This project is suitable for:

- RDK X5 embedded AI / robotics development.
- ROS2 mobile robot course projects.
- Indoor service robot prototype development.
- Lidar SLAM and Nav2 navigation experiments.
- Integration of visual detection and mobile robot service workflows.
- Embedded chip design competition project archives.

## Notes

This repository is mainly an archive of source code and model resources for the project. Some paths and device names are strongly coupled to the original hardware setup. When porting the project to another vehicle or development board, adjust the serial port names, camera index, lidar model, chassis dimensions, and ROS2 distribution according to the actual hardware.
