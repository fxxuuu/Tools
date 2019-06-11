import rosbag
import argparse
import sys
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--camera_number', required=True, help='input camera number')
parser.add_argument('-i', '--input_list_files', required=True, help='input jpeg image path list file(s), can be multi-files, split by comma, and these images must be named by timestamp')
parser.add_argument('-t', '--topic_names_file', required=True, help="topic names old and new, split by space")
parser.add_argument('-d', '--dest_path', required=True, help="save BGR rosbag path")
args = parser.parse_args()

camera_num = int(args.camera_number)
input_list_files = args.input_list_files
dest_path = args.dest_path

print "camera_num is", camera_num

input_list_files = input_list_files.split(',')
print "len(input_list_files) is", len(input_list_files)
assert camera_num == len(input_list_files)

topic_list = [l.strip() for l in open(args.topic_names_file).readlines()]
print "len(topic_list) is", len(topic_list)
assert camera_num == len(topic_list)

dst_bag = rosbag.Bag(dest_path, 'w')

bridge = CvBridge()

for i in range(camera_num):
    input_list_file = input_list_files[i]
    with open(input_list_file, 'r') as fp:
        input_image_list = [l.strip() for l in fp.readlines()]
    topic_name = topic_list[i]
    cnt = 0
    for input_img_path in input_image_list:
        ts_str = input_img_path.split('/')[-1][:-4]
        ts_sec_str = ts_str.split('.')[0]
        ts_nsec_str = ts_str.split('.')[1]
        cv_image = cv2.imread(input_img_path)
        imgmsg = bridge.cv2_to_imgmsg(cv_image, "bgr8")
        imgmsg.header.stamp.secs = int(ts_sec_str)
        imgmsg.header.stamp.nsecs = int(ts_nsec_str)
        cnt += 1
        sys.stdout.write('\rcamera %d: [%d / %d]' % (i, cnt, len(input_image_list)))
        sys.stdout.flush()
        dst_bag.write(topic_name, imgmsg, imgmsg.header.stamp)
    sys.stdout.write('\n')
    sys.stdout.flush()

dst_bag.close()
