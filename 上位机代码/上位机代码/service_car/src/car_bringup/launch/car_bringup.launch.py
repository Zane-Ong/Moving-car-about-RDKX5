from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node

import os
from ament_index_python.packages import get_package_share_directory

from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    # 负责小车的驱动控制；发布四轮速度vel_raw话题并发布到/base_node节点
    driver_node = Node(
        package='car_bringup',
        executable='car_driver',
    )

    # 订阅四轮速度信息，发布里程计Odom_raw话题和坐标变换
    speed_node = Node(
        package='car_base_node',
        executable='speed_node',
        output = "screen"
    )
    base_node = Node(
        package='car_base_node',
        executable='base_node',
        output = "screen"
    )

    # 获取imu数据并发布imu/data_raw到/imu_filter_node节点
    imu_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
         get_package_share_directory('car_imu_node'), 'launch'),
         '/rviz_and_imu.launch.py'])
    )

    imu_filter_config = os.path.join(
         get_package_share_directory('car_bringup'), 
         'params',
         'imu_filter_param.yaml'
    ) 
    # 对imu_raw数据进行滤波,发布imu/data数据到ekf_node进行融合
    # imu_filter_node = Node(
    #     package='imu_filter_madgwick',
    #     executable='imu_filter_madgwick_node',
    #     parameters=[imu_filter_config]
    # )
    # imu_filter_node = Node(
    #     PythonLaunchDescriptionSource([os.path.join(
    #      get_package_share_directory('imu_filter_madgwick'), 'launch'),
    #      '/imu_filter.launch.py'])
    # )

    ekf_config = os.path.join(
         get_package_share_directory('car_bringup'), 
         'params',
         # 'ekf_yahboom.yaml'
         'ekf_param.yaml'
    )
    # 接收base_node发的odom_raw数据和imu_filter_node滤波后的的imu/data数据，使用扩展卡尔曼滤波（EKF）配置发布里程计数据
    ekf_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
         get_package_share_directory('car_bringup'), 'launch'),
         '/ekf.launch.py']),
        launch_arguments={'params_file': ekf_config}.items()  # 传递参数文件路径
    )

    # 遥控控制功能
    joy_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
         get_package_share_directory('car_ctrl'), 'launch'),
         'car_ctrl.launch.py'])
    )
    
    # 加载小车的模型描述
    car_description_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
         get_package_share_directory('car_description'), 'launch'),
         '/description_launch.py'])
    )

    return LaunchDescription([
        driver_node,
        speed_node,
        base_node,          
        imu_node,
        # imu_filter_node,  
        # ekf_node, 
        # joy_node,
        car_description_node,
    ])
