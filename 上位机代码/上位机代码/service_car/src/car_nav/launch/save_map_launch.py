from ament_index_python.packages import get_package_share_path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node
import os


def generate_launch_description():
    package_share_path = str(get_package_share_path('car_nav'))
    package_path = os.path.abspath(os.path.join(
        package_share_path, "../../../../src/car_nav"))
    map_name = "service_map"
    default_map_path = os.path.join(package_path, 'maps', map_name)

    # 保存的地图路径
    map_arg = DeclareLaunchArgument(name='map_path', default_value=str(default_map_path),
                                    description='The path of the map')

    # 保存功能启动
    map_saver_node = Node(
        package='nav2_map_server',
        executable='map_saver_cli',
        arguments=[
            '-f', LaunchConfiguration('map_path')],
    )
    # , '--ros-args', '-p', 'save_map_timeout:=60000'
    return LaunchDescription([
        map_arg,
        map_saver_node
    ])
