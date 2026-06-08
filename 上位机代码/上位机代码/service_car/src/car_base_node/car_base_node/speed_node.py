#!/usr/bin/env python3

import sys
import signal
import serial
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray


class WheelSpeedPublisher(Node):
    """ROS 2 节点，用于发布轮子速度"""

    def __init__(self):
        super().__init__('wheel_speed_publisher')
        self.publisher_ = self.create_publisher(Float32MultiArray, 'vel_raw', 10)
        self.get_logger().info("轮子速度发布节点已启动")

    def publish_speeds(self, speeds):
        """发布速度数据"""
        msg = Float32MultiArray()
        msg.data = speeds
        self.publisher_.publish(msg)
        # self.get_logger().info(f"已发布速度数据: {msg}")


def parse_wheel_speeds(data):
    """解析四个轮子的速度值 (uint16_t 转换为 int16_t)"""
    wheel_speeds = []
    for i in range(0, len(data), 2):
        # 将接收到的两个字节按照低位在前，高位在后的方式组合成 uint16_t
        raw_speed = (data[i] | (data[i + 1] << 8))  # 第1字节是低位，第2字节是高位

        # 将 uint16_t 映射为 int16_t
        if raw_speed > 32767:  # 大于 32767 表示负数
            speed = -(65536 - raw_speed)  # 转换为负值
        else:
            speed = raw_speed

        wheel_speeds.append(speed)
        
    # 第三个和第四个数据添加负号
    if len(wheel_speeds) > 2:
        wheel_speeds[2] = -wheel_speeds[2]
    if len(wheel_speeds) > 3:
        wheel_speeds[3] = -wheel_speeds[3]
    return wheel_speeds


def serial_receive(node):
    """串口接收数据并发布 ROS 话题"""
    uart_dev = '/dev/ttyUSB_CH340'  # 替换为你的串口设备
    baudrate = 115200  # 波特率
    try:
        ser = serial.Serial(uart_dev, baudrate, timeout=1)  # 1s 超时时间
        node.get_logger().info(f"已成功打开串口 {uart_dev}，波特率 {baudrate}")
    except Exception as e:
        node.get_logger().error(f"打开串口失败！错误信息: {e}")
        return -1

    node.get_logger().info("正在等待数据帧... 按 CTRL+C 退出程序。")

    try:
        while rclpy.ok():
            # 等待接收数据
            if ser.in_waiting > 0:
                byte = ser.read(1)  # 读取一个字节
                # print("byte[0]:"+hex(byte[0]))
                # print("byte[1]:"+hex(byte[1]))
                if byte == b'\xFF' :
                    byte = ser.read(1)  # 读取一个字节
                    if byte == b'\x7F':  # 检测到帧头 0xFF
                        frame = ser.read(8)  # 读取后续 8 个字节
                        if len(frame) == 8:
                            wheel_speeds = parse_wheel_speeds(frame)  # 解析轮子速度
                            # node.get_logger().info(f"接收到有效数据帧: {frame.hex().upper()}")
                            
                            # 将速度值转换为 m/s
                            wheel_speeds_mps = [round(speed* 0.0000978,5) for speed in wheel_speeds]
                            # node.get_logger().info(f"四个轮子的速度 (m/s): {wheel_speeds_mps}")
                            node.publish_speeds(wheel_speeds_mps)  # 发布速度数据
                        else:
                            node.get_logger().warning("接收数据帧不完整！")
    except KeyboardInterrupt:
        node.get_logger().info("检测到 CTRL+C，退出程序")
    finally:
        ser.close()
        node.get_logger().info("串口已关闭")
    return 0


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # 捕获 CTRL+C 信号
    rclpy.init()
    node = WheelSpeedPublisher()

    try:
        serial_receive(node)
    finally:
        rclpy.shutdown()
        node.get_logger().info("程序结束。")


if __name__ == '__main__':
    main()
