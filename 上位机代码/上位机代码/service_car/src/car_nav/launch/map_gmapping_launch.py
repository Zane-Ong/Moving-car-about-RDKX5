from launch import LaunchDescription
from launch_ros.actions import Node
import os
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    # 启动设备
    laser_bringup_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
        get_package_share_directory('car_nav'), 'launch'),
         '/laser_bringup_launch.py'])
    )

    # 启动建图相关节点
    slam_gmapping_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
        get_package_share_directory('slam_gmapping'), 'launch'),
         '/test_gmapping.launch.py'])
    ) # 官网使用的好像是slam_gmapping.launch.py

    # 启动建图相关节点
    # slam_gmapping_launch = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource([os.path.join(
    #     get_package_share_directory('slam_gmapping'), 'launch'),
    #      '/slam_gmapping.launch.py'])
    # )

    return LaunchDescription([laser_bringup_launch, slam_gmapping_launch])
