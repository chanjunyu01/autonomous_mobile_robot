import rclpy
from example_interfaces.msg import String
from rclpy.node import Node


class StatusPublisher(Node):
    def __init__(self):
        super().__init__('status_publisher')
        self.publisher = self.create_publisher(String, 'status', 10)
        self.timer = self.create_timer(1.0, self.publish_status)
        self.get_logger().info('Status publisher started.')

    def publish_status(self):
        message = String()
        message.data = 'Robot basics publisher is running.'
        self.publisher.publish(message)
        self.get_logger().info(f'Publishing: "{message.data}"')


def main(args=None):
    rclpy.init(args=args)
    node = StatusPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
