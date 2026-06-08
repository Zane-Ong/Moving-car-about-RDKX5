import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    package_path = get_package_share_directory('car_nav')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    # 定义参数
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    nav2_param_path = LaunchConfiguration(
        'params_file', default=os.path.join(package_path, 'params', 'dwb_nav_params.yaml')
    )

    # 启动激光雷达相关节点
    laser_bringup_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [os.path.join(package_path, 'launch'), '/laser_bringup_launch.py']
        )
    )

    # 启动 Cartographer（建图）
    cartographer_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [os.path.join(package_path, 'launch'), '/cartographer_launch.py']
        )
    )

    # 启动 Nav2（导航，不加载静态地图）
    nav2_bringup_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [os.path.join(nav2_bringup_dir, 'launch'), '/bringup_launch.py']
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'params_file': nav2_param_path,
            'use_map_server': 'false',  # 禁用静态地图
            'map': ''
        }.items(),
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value=use_sim_time,
                              description='Use simulation (Gazebo) clock if true'),
        DeclareLaunchArgument('params_file', default_value=nav2_param_path,
                              description='Full path to param file to load'),
        laser_bringup_launch,
        cartographer_launch,
        nav2_bringup_launch,
    ])
