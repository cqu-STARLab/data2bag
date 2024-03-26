import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, LogInfo, TimerAction
from launch.conditions import UnlessCondition, IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    yaml_config_dir = os.path.join(get_package_share_directory('data2bag'), 'config', 'kitti.yaml')
    rviz_config_dir = os.path.join(get_package_share_directory('data2bag'), 'config', 'kitti.rviz')
    save_bag_path = "/home/myx/develop/data/test_data/data_bag"

    return LaunchDescription([
        DeclareLaunchArgument('if_bag_record', default_value='True', description='Whether to record bag or not'),
        DeclareLaunchArgument('if_rviz2_open', default_value='True', description='Whether to open rviz2 or not'),

        Node(
            package='data2bag',
            executable='data2bag_kitti',
            name='data2bag_kitti',
            output='screen',
            parameters=[yaml_config_dir],
        ),

        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            output="screen",
            arguments=['-d', rviz_config_dir],
            condition=IfCondition(LaunchConfiguration("if_rviz2_open"))
        ),

        ExecuteProcess(
            cmd=['ros2', 'bag', 'record', '-o', save_bag_path, "/kitti/point_cloud", "/kitti/image/gray/left",
                 "/kitti/image/gray/right", "/kitti/image/color/left", "/kitti/image/color/right", "/kitti/imu",
                 "/kitti/nav_sat_fix", "/kitti/marker_array"],
            output='screen',
            condition=IfCondition(LaunchConfiguration("if_bag_record"))
        ),
        Node(package="tf2_ros",
             executable="static_transform_publisher",
             arguments="0 0 0 0 0 0 base_link velodyne".split(" "),
             parameters=[]),
        Node(package="tf2_ros",
             executable="static_transform_publisher",
             arguments="0 0 0 0 0 0 base_link gray_camera_left".split(" "),
             parameters=[]),
        Node(package="tf2_ros",
             executable="static_transform_publisher",
             arguments="0 0 0 0 0 0 base_link gray_camera_right".split(" "),
             parameters=[]),
        Node(package="tf2_ros",
             executable="static_transform_publisher",
             arguments="0 0 0 0 0 0 base_link color_camera_left".split(" "),
             parameters=[]),
        Node(package="tf2_ros",
             executable="static_transform_publisher",
             arguments="0 0 0 0 0 0 base_link color_camera_right".split(" "),
             parameters=[]),
        Node(package="tf2_ros",
             executable="static_transform_publisher",
             arguments="0 0 0 0 0 0 base_link imu".split(" "),
             parameters=[]),
        Node(package="tf2_ros",
             executable="static_transform_publisher",
             arguments="0 0 0 0 0 0 base_link oxts".split(" "),
             parameters=[]),
    ])
