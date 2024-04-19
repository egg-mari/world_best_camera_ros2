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
        super().__init__('bolok')
        self.declare_parameter('thrs1', 200)
        self.declare_parameter('thrs2', 400)
        self.thrs1 = self.get_parameter('thrs1').value
        self.thrs2 = self.get_parameter('thrs2').value
        self.img_subscriber = self.create_subscription(
            Image,
            '/mirror_topic_hwan',  
            self.image_callback,
            10)

        self.img_publisher = self.create_publisher(
            Image,
            '/bolok',  # Where to publish the processed image data
            10)

        self.cv_bridge = CvBridge()

    def image_callback(self, msg):
        img = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        processed_img = self.process_image(img)
        pub_img = self.cv_bridge.cv2_to_imgmsg(processed_img, "bgr8")
        self.img_publisher.publish(pub_img)

    def process_image(self, img):
        height, width = img.shape[:2]
        map_y, map_x = np.indices((height,width), dtype=np.float32)
        map_lenz_x = 2*map_x/(width-1)-1
        map_lenz_y = 2*map_y/(height-1)-1
        r, theta = cv2.cartToPolar(map_lenz_x, map_lenz_y)
        r_convex = r.copy()
        r_concave = r.copy()
        r_convex[r< 1] = r_convex[r<1] **2  
        map_x_new, map_y_new = cv2.polarToCart(r_convex, theta)
        

        map_x_new = ((map_x_new + 1) * width) / 2
        map_y_new = ((map_y_new + 1) * height) / 2
        bolok_img = cv2.remap(img, map_x_new.astype(np.float32), map_y_new.astype(np.float32), cv2.INTER_LINEAR)
        return bolok_img

def main(args=None):
    rclpy.init(args=args)
    image_processor = ImageProcessor()
    rclpy.spin(image_processor)
    image_processor.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
