from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node

import os
from ament_index_python.packages import get_package_share_directory

from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    # 启动底盘
    bringup_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
        get_package_share_directory('car_bringup'), 'launch'),
        '/car_bringup.launch.py'])
    )

    # 启动雷达
    # ms200_scan_node = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource([os.path.join(
    #      get_package_share_directory('rplidar_ros'), 'launch'),
    #      '/rplidar_a1_launch.py'])
    # )
    ms200_scan_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
         get_package_share_directory('oradar_lidar'), 'launch'),
         '/ms200_scan.launch.py'])
    )
    # 启动摄像头


    # 静态TF关系在car_description中定义

    launch_description = LaunchDescription([
        ms200_scan_node,
        bringup_node
        ]) 
    return launch_description
