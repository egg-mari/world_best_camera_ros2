import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from rclpy.qos import QoSProfile
import cv2
import base64
import numpy as np

class ImageProcessor(Node):
    def __init__(self):
        super().__init__('sharpening')
        self.declare_parameter('thrs1', 200)
        self.declare_parameter('thrs2', 400)
        self.thrs1 = self.get_parameter('thrs1').value
        self.thrs2 = self.get_parameter('thrs2').value
        self.img_subscriber = self.create_subscription(
            Image,
            '/camera12',  
            self.image_callback,
            10)

        self.img_publisher = self.create_publisher(
            Image,
            '/sharpening',  # Where to publish the processed image data
            10)

        self.cv_bridge = CvBridge()

    def image_callback(self, msg):
        img = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        processed_img = self.process_image(img)
        pub_img = self.cv_bridge.cv2_to_imgmsg(processed_img, "bgr8")
        self.img_publisher.publish(pub_img)

    def process_image(self, img):
        kernel = np.array([[-1, -1, -1],
                   [-1,  9, -1],
                   [-1, -1, -1]])
        sharpened = cv2.filter2D(img, -1, kernel)
        return sharpened

def main(args=None):
    rclpy.init(args=args)
    image_processor = ImageProcessor()
    rclpy.spin(image_processor)
    image_processor.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()