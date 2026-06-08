import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import launch

def generate_launch_description():

    # 启动设备
    laser_bringup_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
        get_package_share_directory('car_nav'), 'launch'),
         '/laser_bringup_launch.py'
        ])
    )

    # 启动建图相关节点
    slam_toolbox_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('slam_toolbox'),
                'launch',
                'online_sync_launch.py'
            )
        )
    )

    return LaunchDescription([laser_bringup_launch, slam_toolbox_launch])