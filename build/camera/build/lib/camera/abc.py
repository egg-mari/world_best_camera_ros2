import rosbag
from cv_bridge import CvBridge
import cv2
from datetime import datetime

# 현재 시간을 문자열 형식으로 얻기
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# .bag 파일 열기
bag = rosbag.Bag('../../../2024-04-18-13-25-46/2024-04-18-13-25-46_0.db3', 'r')
bridge = CvBridge()

# VideoWriter 객체 생성, 파일 이름에 현재 시간 사용
out = cv2.VideoWriter(f'output_{current_time}.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))

# .bag 파일에서 이미지 메시지 읽기
for topic, msg, t in bag.read_messages(topics=['/camera12']):
    if topic == '/camera12':
        cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        out.write(cv_image)

# 자원 정리
out.release()
bag.close()
