import rosbag
import argparse
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--src', required=True, help='JPG rosbag')
parser.add_argument('-d', '--dist', required=True, help="BGR rosbag")
args = parser.parse_args()

src_path = args.src
dist_path = args.dist

src_bag = rosbag.Bag(src_path)
dst_bag = rosbag.Bag(dist_path, 'w')

imgmsg = Image()
bridge = CvBridge()

for topic, msg, time in src_bag.read_messages(topics=['/mvp/drv/sv_front_raw_img/jpeg', '/mvp/drv/sv_right_raw_img/jpeg', '/mvp/drv/sv_behind_raw_img/jpeg', '/mvp/drv/sv_left_raw_img/jpeg']):
    print msg.header

    try:
        cv_image = bridge.compressed_imgmsg_to_cv2(msg)
        imgmsg = bridge.cv2_to_imgmsg(cv_image, "bgr8")
        imgmsg.header = msg.header
    except CvBridgeError as e:
        print e

    dst_bag.write(topic.rstrip('/jpeg'), imgmsg, time)

src_bag.close()
dst_bag.close()
