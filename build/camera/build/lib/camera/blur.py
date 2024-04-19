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
        super().__init__('mosaic')
        self.declare_parameter('thrs1', 200)
        self.declare_parameter('thrs2', 400)
        self.thrs1 = self.get_parameter('thrs1').value
        self.thrs2 = self.get_parameter('thrs2').value
        self.declare_parameter('width', 640)
        self.width = self.get_parameter('width').value
        self.declare_parameter('length', 480)
        self.length = self.get_parameter('length').value
        self.img_subscriber = self.create_subscription(
            Image,
            '/camera',  
            self.image_callback,
            10)

        self.img_publisher = self.create_publisher(
            Image,
            '/mosaic',  # Where to publish the processed image data
            10)

        self.cv_bridge = CvBridge()

    def image_callback(self, msg):
        img = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        processed_img = self.process_image(img,mosaic_factor=0.1)
        pub_img = self.cv_bridge.cv2_to_imgmsg(processed_img, "bgr8")
        self.img_publisher.publish(pub_img)

    def process_image(self, img,mosaic_factor=0.1):
        height, width = img.shape[:2]
    
    # 모자이크 처리: 이미지를 축소했다가 확대
        small_img = cv2.resize(img, (int(width * mosaic_factor), int(height * mosaic_factor)), interpolation=cv2.INTER_LINEAR)
        mosaic_img = cv2.resize(small_img, (width, height), interpolation=cv2.INTER_NEAREST)
        return mosaic_img

def main(args=None):
    rclpy.init(args=args)
    image_processor = ImageProcessor()
    rclpy.spin(image_processor)
    image_processor.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
