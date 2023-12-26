import sys

from example_interfaces.srv import AddTwoInts
from more_interfaces.srv import AddThreeInts
import rclpy
from rclpy.node import Node


class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.declare_parameter('a', 1)
        self.declare_parameter('b', 2)
        self.declare_parameter('c', 3)
        self.cli = self.create_client(AddThreeInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AddThreeInts.Request()

    def send_request(self, a=None, b=None, c=None):

        if a is None:
            a = self.get_parameter('a').value
        if b is None:
            b = self.get_parameter('b').value
        if c is None:
            c = self.get_parameter('c').value

        self.req.a = a
        self.req.b = b
        self.req.c = c
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()


def main():
    rclpy.init()

    minimal_client = MinimalClientAsync()
    # a, b, c = sys.argv[1:4]
    # response: AddThreeInts.Response = minimal_client.send_request(int(a), int(b), int(c))
    response: AddThreeInts.Response = minimal_client.send_request()
    # minimal_client.get_logger().info(f"Result of add_two_ints: {a} + {b} + {c} = {response.sum}")
    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
