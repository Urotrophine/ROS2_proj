#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from ament_index_python.packages import get_package_share_directory
import os

class RobotDescriptionPublisher(Node):
    def __init__(self):
        super().__init__('robot_description_publisher')
        pkg_path = get_package_share_directory('car2')
        urdf_file = os.path.join(pkg_path, 'urdf', 'car2.urdf')
        with open(urdf_file, 'r') as f:
            robot_desc = f.read()

        self.pub = self.create_publisher(String, '/robot_description', 10)
        # 每秒发一次（足够）
        self.timer = self.create_timer(1.0, lambda: self._publish(robot_desc))

    def _publish(self, text):
        msg = String()
        msg.data = text
        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = RobotDescriptionPublisher()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
