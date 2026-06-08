import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion, TransformStamped
# import tf_transformations
from std_msgs.msg import Float32MultiArray
import math
import tf2_ros
import numpy as np
from geometry_msgs.msg import Twist

class OdomPublisher(Node):
    def __init__(self):
        super().__init__('OdomPublisher')
        
        # 订阅四个电机速度的消息
        self.subscription = self.create_subscription(
            Float32MultiArray,  
            'vel_raw', 
            self.motor_vel_callback,
            10)
        
        # 测试用，订阅四个电机速度的消息，这里直接读取cmd_vel解算出来的四个电机速度
		# create subcriber 创建订阅者
        # self.sub_cmd_vel = self.create_subscription(
        #     Twist,
        #     "cmd_vel",
        #     self.cmd_vel_callback,
        #     1)

        # 创建发布方
        # self.odom_publisher = self.create_publisher(Odometry, 'odom_raw', 10)   # 发布里程计消息
        self.odom_publisher = self.create_publisher(Odometry, 'odom', 10)   # 发布里程计消息
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)                # 发布TF消息
        
        # 定时器，用于定时发布里程计
        self.timer = self.create_timer(0.05, self.publish_odometry)  # 20Hz

        # 记录时间
        self.last_time = self.get_clock().now()
        
        # 机器人参数
        self.c = 0.636
        self.dt = 0.05  # 微分时间间隔
        
        # 状态变量
        self.x = 0.0  # 机器人全局位置 x
        self.y = 0.0  # 机器人全局位置 y
        self.heading = 0.0  # 机器人朝向
        self.vx = 0.0  # 机器人 x 方向速度
        self.vy = 0.0  # 机器人 y 方向速度
        self.delta_heading = 0.0  # 机器人朝向微分
        self.motor_speeds = [0.0, 0.0, 0.0, 0.0]  # v1, v2, v3, v4 对应前左轮、后左轮、前右轮、后右轮

    # 测试用
	#callback function
    # def cmd_vel_callback(self, msg):
    #     if not isinstance(msg, Twist): return
    #     vx = msg.linear.x
    #     vy = msg.linear.y
    #     angular = msg.angular.z

    #     A = np.array([[1, -self.c/2], [1, self.c/2]])
    #     B = np.array([vx, angular])
    #     V = np.dot(A, B)
    #     vl, vr = V

    #     self.v1 = self.v2 = vl
    #     self.v3 = self.v4 = vr


    def motor_vel_callback(self, msg):
        # 读取四个电机速度
        self.motor_speeds = msg.data
        # self.get_logger().info(f"四个轮子的速度 (m/s): {self.motor_speeds}")
    def return_smaller_by_absolute(self, a, b):
        if np.abs(a) < np.abs(b):
            return a
        else:
            return b

    def compute_odometry(self):
        current_time = self.get_clock().now()

        # 解算 COM 的线速度和角速度
        v1, v2, v3, v4 = self.motor_speeds
        c = self.c

        self.dt = (current_time - self.last_time).nanoseconds / 1e9
        self.last_time = current_time
        # self.get_logger().info(f"四个轮子的速度 (m/s): {self.motor_speeds}")

        # 根据运动学公式解算
        vl = self.return_smaller_by_absolute(v1 , v2)
        vr = self.return_smaller_by_absolute(v3 , v4)
        A = np.array([[1 / 2, 1 / 2], [-1 / c, 1 / c]])
        B = np.array([vl, vr])
        V = np.dot(A, B)
        self.vx, self.delta_heading = V
        self.delta_heading = self.delta_heading * 0.7

        # 更新机器人全局位置
        self.x += self.vx * math.cos(self.heading) * self.dt - self.vy * math.sin(self.heading) * self.dt
        self.y += self.vx * math.sin(self.heading) * self.dt + self.vy * math.cos(self.heading) * self.dt
        self.heading += self.delta_heading * self.dt

    # 欧拉角转四元数
    def get_quaternion_from_euler(self, roll, pitch, yaw):
        qx = np.sin(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) - np.cos(roll / 2) * np.sin(pitch / 2) * np.sin(
            yaw / 2)
        qy = np.cos(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.cos(pitch / 2) * np.sin(
            yaw / 2)
        qz = np.cos(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2) - np.sin(roll / 2) * np.sin(pitch / 2) * np.cos(
            yaw / 2)
        qw = np.cos(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.sin(pitch / 2) * np.sin(
            yaw / 2)

        return [qx, qy, qz, qw]

    def publish_odometry(self):
        # 计算里程计
        self.compute_odometry()

        # 获取当前时间戳
        current_time = self.get_clock().now()

        # 构造里程计消息
        odom_msg = Odometry()
        odom_msg.header.stamp = current_time.to_msg()
        odom_msg.header.frame_id = 'odom'
        odom_msg.child_frame_id = 'base_footprint'

        # 设置位置
        odom_msg.pose.pose.position.x = self.x
        odom_msg.pose.pose.position.y = self.y
        odom_msg.pose.pose.position.z = 0.0
        q = self.get_quaternion_from_euler(0.0, 0.0, self.heading)
        # q = tf_transformations.quaternion_from_euler(0, 0, self.heading)
        odom_msg.pose.pose.orientation = Quaternion()
        odom_msg.pose.pose.orientation.x = q[0]
        odom_msg.pose.pose.orientation.y = q[1]
        odom_msg.pose.pose.orientation.z = q[2]
        odom_msg.pose.pose.orientation.w = q[3]

        # 设置速度
        odom_msg.twist.twist.linear.x = self.vx
        odom_msg.twist.twist.linear.y = self.vy
        odom_msg.twist.twist.angular.z = self.delta_heading

        # 发布里程计消息
        self.odom_publisher.publish(odom_msg)

        # 发布Odom到base_link的TF坐标变换,这个现在交给ekf融合后再发布
        t = TransformStamped()
        t.header.stamp = current_time.to_msg()
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_footprint'

        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = self.heading
        q = self.get_quaternion_from_euler(0.0, 0.0, self.heading)
        # q = tf_transformations.quaternion_from_euler(0, 0, self.heading)
        t.transform.rotation = Quaternion()
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]

        # 发布TF消息
        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = OdomPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
