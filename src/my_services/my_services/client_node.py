import sys

from example_interfaces.srv import AddTwoInts
from tutorial_interfaces.srv import AddThreeInts
import rclpy
from rclpy.node import Node


class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(AddThreeInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AddThreeInts.Request()

    def send_request(self, a, b, c):
        self.req.a = a
        self.req.b = b
        self.req.c = c
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()


def main():
    rclpy.init()

    minimal_client = MinimalClientAsync()
    a, b, c = sys.argv[1:4]
    response: AddThreeInts.Response = minimal_client.send_request(int(a), int(b), int(c))
    minimal_client.get_logger().info(f"Result of add_two_ints: {a} + {b} + {c} = {response.sum}")
    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
