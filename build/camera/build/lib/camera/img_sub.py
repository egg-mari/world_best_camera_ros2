import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class ImgSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')
        self.subscription = self.create_subscription(
            Image,
            '/camera12',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.cv_bridge = CvBridge()

    def listener_callback(self, msg):
        # 메시지를 OpenCV 이미지로 변환
        cv_image = self.cv_bridge.imgmsg_to_cv2(msg, "bgr8")
        
        # 이미지를 그레이스케일로 변환
        gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # 그레이스케일 이미지 표시
        cv2.imshow("Subscribed Gray Image", gray_image)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    subscriber = ImgSubscriber()
    rclpy.spin(subscriber)
    subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
