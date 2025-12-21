from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_path = get_package_share_directory('car2')
    urdf_file = os.path.join(pkg_path, 'urdf', 'car2.urdf')

    # 读取 URDF 内容，传给 robot_state_publisher 的参数（这样它会发布 TF）
    with open(urdf_file, 'r') as f:
        robot_desc = f.read()

    return LaunchDescription([
        # 发布 /robot_description topic（我们安装的脚本）
        Node(
            package='car2',
            executable='robot_description_publisher.py',
            output='screen'
        ),

        # 发布 robot_description 为 parameter 以便 robot_state_publisher 使用（并发布 TF）
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_desc}],
            output='screen'
        ),

        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            output='screen'
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            output='screen'
        )
    ])
