from geometry_msgs.msg import TwistStamped   # ① 统一用 TwistStamped
import rclpy, math
from std_msgs.msg import String

class ShapeDrawer:
    def __init__(self):
        self.n = rclpy.create_node('shape_drawer_jazzy')
        # ② 只保留一个发布者，类型 TwistStamped，话题 /demo/cmd_vel
        self.pub = self.n.create_publisher(TwistStamped, '/demo/cmd_vel', 10)
        self.n.create_subscription(String, 'voice_words', self.cb, 10)
        self.seq = []
        self.idx = 0
        self.timer = None

    # ---------------- 统一封装：发一次速度 ----------------
    def send_vel(self, vx=0.0, wz=0.0):
        tw = TwistStamped()
        tw.header.stamp = self.n.get_clock().now().to_msg()
        tw.twist.linear.x = vx
        tw.twist.angular.z = wz
        self.pub.publish(tw)

    # ---------------- 画图形定时器 ----------------
    def start_shape(self, shape, side=0.6, speed=0.25):
        if self.timer and not self.timer.is_canceled():
            self.timer.cancel()
        t_go = side / speed
        t_turn = math.radians(90 if shape == 'square' else 120) / 1.0
        n = 4 if shape == 'square' else 3
        self.seq = [(speed, 0.0, t_go), (0.0, 1.0, t_turn)] * n
        self.idx = 0
        self.timer = self.n.create_timer(0.1, self.timer_cb)

    def timer_cb(self):
        if self.idx >= len(self.seq):
            self.send_vel(0.0, 0.0)   # 结束发 0
            self.timer.cancel()
            return
        vx, wz, t = self.seq[self.idx]
        self.send_vel(vx, wz)
        self.seq[self.idx] = (vx, wz, t - 0.1)
        if self.seq[self.idx][2] <= 0:
            self.idx += 1

    # ---------------- 语音回调 ----------------
    def cb(self, msg):
        w = msg.data
        tw = TwistStamped()
        tw.header.stamp = self.n.get_clock().now().to_msg()   # 时间戳

        if '正方形' in w or 'square' in w:
            self.start_shape('square')
            return
        elif '三角形' in w or 'triangle' in w:
            self.start_shape('triangle')
            return
        elif '前进' in w:
            tw.twist.linear.x = 1.0
        elif '后退' in w:
            tw.twist.linear.x = -1.0
        elif '向左' in w:
            tw.twist.angular.z = 1.0
        elif '向右' in w:
            tw.twist.angular.z = -1.0
        elif '停下' in w:
            pass        # tw 已是全 0
        else:
            return      # 未匹配任何关键词

        self.pub.publish(tw)   # 统一发布

def main():
    rclpy.init()
    drawer = ShapeDrawer()
    rclpy.spin(drawer.n)
    rclpy.shutdown()


if __name__ == '__main__':
    main()