import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
import os
from datetime import datetime

class VideoRecorder(Node):
    def __init__(self):
        super().__init__('video_recorder')
        self.subscription = self.create_subscription(Image, '/camera/front', self.image_callback, 10)
        self.bridge = CvBridge()

        timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        video_filename = f"recording_{timestamp}.mp4"
        self.video_filepath = os.path.join(self.recordings_path, video_filename)

        self.video_writer = cv2.VideoWriter('front_camera_view.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30.0, (640, 480))

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        self.video_writer.write(frame)

    def destroy_node(self):
        self.video_writer.release()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    video_recorder = VideoRecorder()
    rclpy.spin(video_recorder)
    video_recorder.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
