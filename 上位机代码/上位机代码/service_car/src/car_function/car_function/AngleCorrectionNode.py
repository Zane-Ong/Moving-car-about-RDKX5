import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
import math
import time

class AngleCorrectionNode(Node):
    def __init__(self):
        super().__init__('angle_correction_node')

        # 订阅 IMU 数据
        self.subscription = self.create_subscription(
            Imu,
            '/imu/data',
            self.imu_callback,
            10
        )

        # 发布控制命令
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        # PID 控制参数
        self.kp = 0.1  # 比例系数
        self.ki = 0.0  # 积分系数
        self.kd = 0.1 # 微分系数

        # PID 初始化
        self.prev_error = 0.0
        self.integral = 0.0

        # 目标角度，用户输入
        # self.target_angle = 0.0  # 目标角度，假设为90度
        self.declare_parameter('target_angle', 20.0)  # 默认值为 0.0
        self.target_angle = self.get_parameter('target_angle').get_parameter_value().double_value
        
        self.current_angle = 0.0
        self.is_correcting = True

        self.get_logger().info(f"目标角度设置为: {self.target_angle}°")

    def EulerAndQuaternionTransform(self, intput_data):
        """
            四元素与欧拉角互换
        """
        data_len = len(intput_data)
        angle_is_not_rad = False

        if data_len == 4:
    
            x = intput_data[0] 
            y = intput_data[1]
            z = intput_data[2]
            w = intput_data[3]
    
            r = math.atan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y))
            p = math.asin(2 * (w * y - z * x))
            y = math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))
    
            if angle_is_not_rad : # pi -> 180
                r = math.degrees(r)
                p = math.degrees(p)
                y = math.degrees(y)
            return [r,p,y]

    def imu_callback(self, msg):
        # 获取四元数数据
        orientation_q = msg.orientation
        # 转换四元数为欧拉角
        euler = self.EulerAndQuaternionTransform([orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w])

        # 只关心 Z 轴的角度（偏航角）
        self.current_angle = euler[2] * 180.0 / 3.141592653589793  # 将弧度转为度

        # 输出当前角度
        self.get_logger().info(f"当前角度: {self.current_angle:.2f}°")

        # 调用 PID 算法计算控制信号
        self.angle_correction_pid()

    def angle_correction_pid(self):
        # 计算误差
        # error = self.target_angle - self.current_angle
        error = (self.target_angle - self.current_angle + 180) % 360 - 180

        # 判断是否已经稳定
        if abs(error) < 0.1:
            self.is_correcting = False
            self.stop_robot()
            self.get_logger().info('目标角度已达成，停止控制')
            return

        self.is_correcting = True

        # PID 算法
        self.integral += error
        derivative = error - self.prev_error

        # PID 控制器输出
        output = self.kp * error + self.ki * self.integral + self.kd * derivative

        # 限制控制输出的范围
        max_speed = 0.2 # 最大速度
        min_speed = -0.2  # 最小速度
        output = max(min(output, max_speed), min_speed)

        # 输出PID控制信号
        self.get_logger().info(f"PID 输出角速度: {output:.2f}")

        # 发布控制命令
        self.publish_command(output)

        # 更新上次误差
        self.prev_error = error

    def publish_command(self, angular_speed):
        # 创建 Twist 消息控制车速
        cmd = Twist()
        cmd.angular.z = angular_speed

        # 发布消息
        self.publisher.publish(cmd)

        self.get_logger().info(f"发布控制命令，角速度: {angular_speed:.2f}")

    def stop_robot(self):
        # 发布停止命令
        cmd = Twist()
        self.publisher.publish(cmd)
        self.get_logger().info("发布停止命令，机器人已停止")

def main(args=None):
    rclpy.init(args=args)
    node = AngleCorrectionNode()

    try:
        while rclpy.ok():
            if not node.is_correcting:
                break
            rclpy.spin_once(node)
    except KeyboardInterrupt:
        pass

    # 清理节点
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
