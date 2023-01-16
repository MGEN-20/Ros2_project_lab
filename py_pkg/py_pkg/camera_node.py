import rclpy # Python Client Library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library
 
class CameraNode(Node):
  def __init__(self):
    super().__init__('camera_node')
      
    self.publisher_ = self.create_publisher(Image, 'video_frames', 10)
      
    timer_period = 0.1

    self.timer = self.create_timer(timer_period, self.timer_callback)
    self.cap = cv2.VideoCapture(0)
    self.br = CvBridge()
   
  def timer_callback(self):
    ret, frame = self.cap.read()
          
    if ret == True:
      self.publisher_.publish(self.br.cv2_to_imgmsg(frame))

    self.get_logger().info('Publishing video frame')
  
def main(args=None):
  rclpy.init(args=args)
  image_publisher = CameraNode()
  rclpy.spin(image_publisher)
  image_publisher.destroy_node()
  rclpy.shutdown()
  
if __name__ == '__main__':
  main()