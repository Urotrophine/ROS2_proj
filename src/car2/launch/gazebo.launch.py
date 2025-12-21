from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_share = get_package_share_directory('car2')
    urdf_file = os.path.join(pkg_share, 'urdf', 'car2.urdf')

    # 读取 URDF
    with open(urdf_file, 'r') as f:
        robot_description = f.read()

    # 启动 Gazebo Harmonic (gz-sim)
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            )
        ),
        launch_arguments={
            'gz_args': '-r empty.sdf'
        }.items()
    )

    # 发布 robot_description
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    # 在 Gazebo 中生成机器人
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'car2',
            '-string', robot_description,
            '-x', '0',
            '-y', '0',
            '-z', '0.1'   # 整体抬高 10cm
        ],
        output='screen'
    )


    # ROS2 静态 TF（替代 tf/static_transform_publisher）
    static_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'base_footprint']
    )

    return LaunchDescription([
        gz_sim,
        rsp_node,
        static_tf,
        spawn_entity
    ])
