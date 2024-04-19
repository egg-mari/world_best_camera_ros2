import rclpy
from rclpy.node import Node
import cv2
import numpy as np
import pyautogui
import subprocess
from datetime import datetime
from pynput import keyboard

class ScreenRecorder(Node):
    def __init__(self):
        super().__init__('screen_recorder')
        self.declare_parameter('record', False)
        self.fps = 15  # FPS 값을 조정하세요.
        self.timer = self.create_timer(1.0 / self.fps, self.timer_callback)  # FPS에 맞춰 타이머 설정
        self.out = None
        self.window_geometry = None
        self.title = "rqt"
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def get_window_geometry(self, title):
        try:
            output = subprocess.check_output(['wmctrl', '-lG'], text=True)
            lines = output.splitlines()
            for line in lines:
                if title in line:
                    _, x, y, width, height, _ = line.split(maxsplit=5)
                    # 여기에서 y 좌표 조정
                    return int(x)+ 100, int(y) + 100, int(width) + 1150, int(height) - 100  # 제목 표시줄의 높이만큼 y 좌표 조정
        except subprocess.CalledProcessError:
            self.get_logger().info("Failed to get window geometry")
            return None

    def on_press(self, key):
        try:
            if key.char == 'r':
                if not self.out:
                    self.start_recording()
                else:
                    self.stop_recording()
            elif key.char == 's':  # s 키를 누를 때 스크린샷 기능 추가
                self.take_screenshot()
        except AttributeError:
            pass

    def start_recording(self):
        if not self.window_geometry:
            self.window_geometry = self.get_window_geometry(self.title)
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.out = cv2.VideoWriter(f'{current_time}.avi', cv2.VideoWriter_fourcc(*'XVID'), self.fps, (self.window_geometry[2], self.window_geometry[3]))
        self.get_logger().info("Recording started.")

    def stop_recording(self):
        if self.out:
            self.out.release()
            self.out = None
            cv2.destroyAllWindows()
            self.get_logger().info("Recording stopped.")

    def timer_callback(self):
        if self.out:
            self.window_geometry = self.get_window_geometry(self.title)
            if not self.window_geometry:
                self.get_logger().info("Window no longer available.")
                self.stop_recording()
                return

            x, y, width, height = self.window_geometry
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            self.out.write(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop_recording()
                self.destroy_node()
                rclpy.shutdown()
    def take_screenshot(self):
        if self.window_geometry:
            x, y, width, height = self.window_geometry
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = f'screenshot_{current_time}.png'
            screenshot.save(screenshot_path)  # 스크린샷을 파일로 저장
            self.get_logger().info(f"Screenshot saved as {screenshot_path}")
def main(args=None):
    rclpy.init(args=args)
    screen_recorder = ScreenRecorder()
    rclpy.spin(screen_recorder)
    screen_recorder.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
