import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from functools import partial
from custom_msg.srv import CheckPosition

class TrajectorySubscriber(Node):

    def __init__(self):
        super().__init__('trajectory_subscriber')

        # TODO: Create a subscriber of type Twist, that calls listener_callback
        # Your code here
        self.subscriber_ = self.create_subscription(Twist, 'cmd_vel', self.listener_callback, 10)

        # TODO: Create a server client of type CheckPosition
        # Your code here
        self.client_ = self.create_client(CheckPosition, 'check_position')
        while not self.client_.wait_for_service(1.0):
            self.get_logger().warn("Waiting for CheckPosition service...")

        self.get_logger().info('Subscriber node has been started.')
        self.position = {'x': 0.0, 'z': 0.0, 'ry': 0.0}

    def send_request(self, x, z):
        # TODO: Send the request to the server synchronously
        # Your code here
        request = CheckPosition.Request()
        request.x = x
        request.z = z

        # Call the service asynchronously and handle the response in the callback
        future = self.client_.call_async(request)
        future.add_done_callback(partial(self.callback_check_position, x=x, z=z))

    def callback_check_position(self, future, x, z):
        try:
            # Get the service response
            response = future.result()
            is_allowed = response.is_allowed
            suggestion = response.suggestion

            # Log the result and suggestion
            self.get_logger().info(f"Position (x={x}, z={z}): Allowed = {is_allowed}, Suggestion = {suggestion}")
            return is_allowed, suggestion
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")
            return False, ""

    def listener_callback(self, msg):
        # TODO: Interpret the received commands and log the result using self.get_logger().info()
        # Your code here
        linear_x = msg.linear.x
        linear_z = msg.linear.z
        angular_y = msg.angular.y

        # Filter invalid movements
        if linear_z != 0.0 and angular_y != 0.0:  # Tz and Ry
            self.get_logger().info('Forbidden move')
        elif linear_x != 0.0 and linear_z != 0.0:  # Tx and Tz
            self.get_logger().info('Forbidden move')
        else:
            # Valid movements
            if linear_x > 0.0:
                self.get_logger().info('Go Forward')
                self.position['x'] += linear_x
            elif linear_x < 0.0:
                self.get_logger().info('Go Backward')
                self.position['x'] += linear_x

            if linear_z > 0.0:
                self.get_logger().info('Slide Right')
                self.position['z'] += linear_z
            elif linear_z < 0.0:
                self.get_logger().info('Slide Left')
                self.position['z'] += linear_z

            if angular_y > 0.0:
                self.get_logger().info('Rotating on itself to the Left')
                self.position['ry'] += angular_y
            elif angular_y < 0.0:
                self.get_logger().info('Rotating on itself to the Right')
                self.position['ry'] += angular_y

        # TODO: Call send_request and wait for the result. Then, update the position of your virtual rover if allowed
        # Your code here
        self.send_request(self.position['x'], self.position['z'])
        self.get_logger().info(f"Current Position: {self.position}")

def main(args=None):
    rclpy.init(args=args)
    node = TrajectorySubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
