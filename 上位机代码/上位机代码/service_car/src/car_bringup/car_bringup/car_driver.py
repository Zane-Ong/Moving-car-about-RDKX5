import struct
import serial
from math import pi

# ROS 2 库
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import numpy as np


class car_driver(Node):
    def __init__(self, name):
        super().__init__(name)
        self.max_speed = 2.0
        self.c = 0.636
        self.v1 = self.v2 = self.v3 = self.v4 = 0.0

        # 初始化串口
        try:
            self.serial_port = serial.Serial('/dev/ttyUSB_CH340', baudrate=115200, timeout=1)
            self.get_logger().info("速度串口初始化成功")
        except serial.SerialException as e:
            self.get_logger().error(f"串口初始化失败: {e}")
            raise

        # 创建订阅者
        self.sub_cmd_vel = self.create_subscription(Twist, "cmd_vel", self.cmd_vel_callback, 1)

    def cmd_vel_callback(self, msg):
        try:
            # 检查消息类型
            if not isinstance(msg, Twist):
                return

            # 提取线速度和角速度
            vx = msg.linear.x
            vy = msg.linear.y
            angular = msg.angular.z

            # 逆运动学解算
            A = np.array([[1, -self.c / 2], [1, self.c / 2]])
            B = np.array([vx, angular])
            V = np.dot(A, B)
            vl, vr = V

            # 限制速度
            self.v1 = self.v2 = np.clip(vl, -self.max_speed, self.max_speed)
            self.v3 = self.v4 = np.clip(vr, -self.max_speed, self.max_speed)
            
            self.v1 = self.v2 = int(self.v1 / 0.0000978)
            self.v3 = self.v4 = int(self.v3 / 0.0000978)

            # 转换为字节数组并发送
            data = struct.pack('>hhhh', self.v1, self.v2, self.v3, self.v4)
            frame = b'\xF0' + data
            self.serial_port.write(frame)
            # self.get_logger().info(f"四个轮子的速度 (m/s): {self.v1, self.v2, self.v3, self.v4}")
            # self.get_logger().info(f"发送数据帧: {frame.hex().upper()}")
        except Exception as e:
            self.get_logger().error(f"处理 cmd_vel 消息时出错: {e}")


def main():
    rclpy.init()
    driver = car_driver('driver_node')
    rclpy.spin(driver)
