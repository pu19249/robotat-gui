import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class Listener(Node):

    def __init__(self):
        super().__init__("listener")

        # Create a subscriber to the "micro_ros_platformio_node_publisher" topic
        self.subscription = self.create_subscription(
            Int32,
            "micro_ros_platformio_node_publisher",
            self.listener_callback,
            10)

    def listener_callback(self, msg: Int32):
        # Print the data received from the publisher
        print("Received data:", msg.data)


def main():
    # Initialize the ROS client library
    rclpy.init()

    # Create a listener node
    listener = Listener()

    # Spin the ROS event loop
    rclpy.spin(listener)

    # Shutdown the ROS client library
    rclpy.shutdown()


if __name__ == "__main__":
    main()
