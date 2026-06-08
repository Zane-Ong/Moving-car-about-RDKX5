import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped
from cartographer_ros_msgs.srv import SubmapQuery

class LocalizationNode(Node):
    def __init__(self):
        super().__init__('localization_node')

        # 创建服务客户端调用Cartographer的Submap查询
        self.submap_client = self.create_client(SubmapQuery, '/cartographer/submap_query')

        # 等待服务可用
        while not self.submap_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')

        # 设置初始位姿
        self.initial_pose_pub = self.create_publisher(PoseWithCovarianceStamped, '/initialpose', 10)

    def set_initial_pose(self, pose):
        msg = PoseWithCovarianceStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "map"  # 根据你自己的坐标系来调整
        msg.pose.pose = pose
        msg.pose.covariance[0] = 1e-3
        msg.pose.covariance[7] = 1e-3
        msg.pose.covariance[35] = 1e-3

        self.initial_pose_pub.publish(msg)
        self.get_logger().info(f'Initial pose set: {pose}')

    def search_for_initial_pose(self):
        # 查询Cartographer的submap来找到合适的初始位姿
        req = SubmapQuery.Request()
        req.trajectory_id = 0  # 根据你的实际情况设置
        req.submap_index = 0    # 根据需要设置子地图索引

        future = self.submap_client.call_async(req)

        # 获取响应数据
        future.add_done_callback(self.process_submap_response)

    def process_submap_response(self, future):
        try:
            response = future.result()
            # 提取位姿
            initial_pose = response.slice_pose

            # 设置机器人的初始位姿
            self.set_initial_pose(initial_pose)
        except Exception as e:
            self.get_logger().error(f"Failed to call service: {e}")

def main(args=None):
    rclpy.init(args=args)
    localization_node = LocalizationNode()

    # 启动初始位姿搜索
    localization_node.search_for_initial_pose()

    rclpy.spin(localization_node)

    localization_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
