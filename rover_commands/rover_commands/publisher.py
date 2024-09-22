import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TrajectoryPublisher(Node):

    def __init__(self):
        super().__init__('trajectory_publisher')
        # TODO: Create a publisher of type Twist
        # Your code here
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)

        self.get_logger().info('Publisher node has been started.')

        # TODO: Create a loop here to ask users a prompt and send messages accordingly
        self.create_timer(0.1, self.cmd_acquisition)

    # Function that prompts user for a direction input, and sends the command
    def cmd_acquisition(self):
        command = input("Enter command (w/a/s/d/t/y): ")
        # TODO: Complete the function to transform the input into the right command.
        # Your code here
        msg = Twist()

        if command == 'w':
            msg.linear.x = 1.0  # Move Forward
            msg.linear.z = 0.0
            msg.angular.y = 0.0
        elif command == 's':
            msg.linear.x = -1.0  # Move Backward
            msg.linear.z = 0.0
            msg.angular.y = 0.0
        elif command == 'a':
            msg.linear.x = 0.0
            msg.linear.z = -1.0 # Slide Left
            msg.angular.y = 0.0
        elif command == 'd':
            msg.linear.x = 0.0
            msg.linear.z = 1.0 # Slide Right
            msg.angular.y = 0.0
        elif command == 't':
            msg.linear.x = 0.0
            msg.linear.z = 0.0
            msg.angular.y = 1.0 # Rotate Left
        elif command == 'y':
            msg.linear.x = 0.0
            msg.linear.z = 0.0
            msg.angular.y = -1.0 # Rotate Right
        else:
            self.get_logger().warn('Invalid command. Please use one of the following: w, a, s, d, t, y')
            return

        self.publisher_.publish(msg)
        # self.get_logger().info(f'Publishing: {command}')
        self.get_logger().info(f'Published: linear:\n'
                           f'  x: {msg.linear.x}\n'
                           f'  y: {msg.linear.y}\n'
                           f'  z: {msg.linear.z}\n'
                           f'angular:\n'
                           f'  x: {msg.angular.x}\n'
                           f'  y: {msg.angular.y}\n'
                           f'  z: {msg.angular.z}')

def main(args=None):
    rclpy.init(args=args)   # Init ROS python
    node = TrajectoryPublisher()  # Create a Node instance
    rclpy.spin(node)  # Run the node in a Thread
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()