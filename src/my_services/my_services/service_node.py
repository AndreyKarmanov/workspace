from example_interfaces.srv import AddTwoInts
from more_interfaces.srv import AddThreeInts

import rclpy
from rclpy.node import Node


class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(AddThreeInts, 'add_two_ints', self.add_three_ints_callback)

    def add_three_ints_callback(self, request: AddThreeInts.Request, response: AddThreeInts.Response) -> AddThreeInts.Response:
        response.sum = request.a + request.b + request.c
        self.get_logger().info(f"Incoming request\na: {request.a} b: {request.b} c: {request.c}\n")
        return response


def main():
    rclpy.init()
    minimal_service = MinimalService()
    rclpy.spin(minimal_service)
    rclpy.shutdown()


if __name__ == '__main__':
    main()

