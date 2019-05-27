import rosbag
import argparse
import sys
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mode', required=True, help='c2r:compress->raw, r2c:raw->compress')
parser.add_argument('-s', '--src', required=True, help='JPG rosbag')
parser.add_argument('-d', '--dist', required=True, help="BGR rosbag")
parser.add_argument('-t', '--topic_names_file', required=True, help="topic names old and new, split by space")
args = parser.parse_args()

src_path = args.src
dist_path = args.dist
topic_list = [l for l in open(args.topic_names_file).readlines()]
topic_dict = {}

for pair in topic_list:
    pair = pair.split()
	#for item in pair:
	#    print item
    print pair[0], pair[1]
    topic_dict[pair[0]] = pair[1]


src_bag = rosbag.Bag(src_path)
dst_bag = rosbag.Bag(dist_path, 'w')

imgmsg = Image()
bridge = CvBridge()
cnt = 0
for topic, msg, time in src_bag.read_messages():
    if topic in topic_dict.keys():
        try:
            if args.mode == 'c2r':
                cv_image = bridge.compressed_imgmsg_to_cv2(msg)
                imgmsg = bridge.cv2_to_imgmsg(cv_image, "bgr8")
            elif args.mode == 'r2c':
                cv_image = bridge.imgmsg_to_cv2(msg)
                imgmsg = bridge.cv2_to_compressed_imgmsg(cv_image,"jpg")
            else:
                print "transfer mode is wrong!"
            imgmsg.header = msg.header
            cnt += 1
            sys.stdout.write('\r[%d], new topic name is [%s]' % (cnt, topic_dict[topic]))
            sys.stdout.flush()
        except CvBridgeError as e:
            print e
        dst_bag.write(topic_dict[topic], imgmsg, time)
    else:
	    dst_bag.write(topic, msg, time)

src_bag.close()
dst_bag.close()
