import rclpy
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle
from rclpy.node import Node
from rclpy.task import Future

from more_interfaces.action import Fibonacci, Fibonacci_GetResult_Response


class FibonacciActionClient(Node):

    def __init__(self):
        super().__init__('fibonacci_action_client')
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')

    def send_goal(self, order: int) -> None:
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        self._action_client.wait_for_server()

        self._send_goal_future: Future = self._action_client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback)
        
        print("send_goal_future", type(self._send_goal_future))

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future: Future) -> None:
        goal_handle: ClientGoalHandle = future.result()
        print("goal_handle", type(goal_handle))
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future: Future):
        response: Fibonacci_GetResult_Response = future.result()
        result: Fibonacci.Result = response.result
        print("response", type(response), "result", type(result))
        self.get_logger().info('Result: {0}'.format(result.sequence))
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg: Fibonacci.Impl.FeedbackMessage):
        feedback: Fibonacci.Feedback = feedback_msg.feedback
        print("feedbackmsg", type(feedback_msg), "feedback", type(feedback))
        self.get_logger().info(f'Feedback: {feedback.partial_sequence}')


def main(args=None):
    rclpy.init(args=args)

    action_client = FibonacciActionClient()

    action_client.send_goal(10)

    rclpy.spin(action_client)


if __name__ == '__main__':
    main()
