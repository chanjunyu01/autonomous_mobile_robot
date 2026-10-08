import rclpy
from example_interfaces.msg import String
from rclpy.node import Node


class StatusSubscriber(Node):
    def __init__(self):
        super().__init__('status_subscriber')
        self.subscription = self.create_subscription(
            String,
            'status',
            self.status_callback,
            10,
        )
        self.get_logger().info('Status subscriber started.')

    def status_callback(self, message):
        self.get_logger().info(f'Received: "{message.data}"')


def main(args=None):
    rclpy.init(args=args)
    node = StatusSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
