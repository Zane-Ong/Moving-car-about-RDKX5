from ament_index_python.packages import get_package_share_path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    urdf_tutorial_path = get_package_share_path('car_description')
    default_model_path = urdf_tutorial_path / 'urdf/service_car.urdf'

    model_arg = DeclareLaunchArgument(name='model', default_value=str(default_model_path),
                                      description='Absolute path to robot urdf file')
    robot_description = ParameterValue(Command(['xacro ', LaunchConfiguration('model')]),
                                       value_type=str)

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
    )
    
    # base_footprint - base_link 的TF关系
    tf_base_footprint_to_base_link = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0.141', '0.0', '0.0', '0.0', 'base_footprint', 'base_link'],
    )

    # base_link - lidar_link 的TF关系
    tf_base_link_to_lidar_link = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0.03', '0.0', '0.0', '0.0', 'base_link', 'lidar_link'],
    )

    # base_link - imu_link 的TF关系
    tf_base_link_to_imu_link = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['-0.088', '0.0', '-0.03', '0.0', '0.0', '0.0', 'base_link', 'imu_link'],
    )

    # base_link - camera_link 的TF关系
    tf_base_link_to_camera_link = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0.05', '0.0', '0.0', '0.0', 'base_link', 'camera_link'],
    )

    return LaunchDescription([
        model_arg,
        joint_state_publisher_node,
        robot_state_publisher_node,
        tf_base_footprint_to_base_link,
        tf_base_link_to_lidar_link,
        tf_base_link_to_imu_link,
        # tf_base_link_to_camera_link,
    ])
