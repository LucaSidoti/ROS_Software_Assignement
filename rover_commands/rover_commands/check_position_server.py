import rclpy
from rclpy.node import Node
from custom_msg.srv import CheckPosition

class CheckPositionServer(Node):

    def __init__(self):
        super().__init__('check_position_server')
        # TODO: Create a server of type CheckPosition.srv that calls check_position_callback at each request.
        # Your code here
        self.srv = self.create_service(CheckPosition, 'check_position', self.check_position_callback)

        self.get_logger().info('Service server has been started.')

    def check_position_callback(self, request, response):
        # TODO: Get the inputs from the request, and process them to check the boundaries
        # Your code here
        x = request.x
        z = request.z

        x_min, x_max = -10, 10
        z_min, z_max = -10, 10

        if x_min <= x <= x_max and z_min <= z <= z_max:
            response.is_allowed = True
        else:
            response.is_allowed = False

        # TODO - BONUS: Try to give a recommendation of which move would help moving further away from the boundaries if you are too close to a boundary.
        # Your code here
        suggestion = ""
        if x <= x_min + 5:
            suggestion += "Move forward"
        elif x >= x_max - 5:
            suggestion += "Move backward"

        if z <= z_min + 5:
            suggestion += "Move right"
        elif z >= z_max - 5:
            suggestion += "Move left"

        if suggestion == "":
            suggestion = "Position is within the safe zone"

        response.suggestion = suggestion

        self.get_logger().info(f'Received request: x={x}, z={z}')
        self.get_logger().info(f'Response: is_allowed={response.is_allowed}, suggestion="{response.suggestion}"')
        return response

def main(args=None):
    rclpy.init(args=args)
    node = CheckPositionServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()