import cv2
import rosbag
from cv_bridge import CvBridge
import os
import os.path as osp
from pprint import pprint as pp
import argparse, sys


def save_img_compressed(save_root, msg, stamp):
    cv_image = brige.compressed_imgmsg_to_cv2(msg, "bgr8")
    img_name = "{}.jpg".format(stamp)
    cv2.imwrite(osp.join(save_root, img_name), cv_image)

def save_img(save_root, msg, stamp):
    cv_image = brige.imgmsg_to_cv2(msg, "bgr8")
    img_name = "{}.jpg".format(stamp)
    cv2.imwrite(osp.join(save_root, img_name), cv_image)


def mkdir_if_missing(folder):
    if not os.path.exists(folder):
        os.system('mkdir -p ' + folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('bag_file')
    parser.add_argument('save_folder')
    parser.add_argument('topic_list_file')
    parser.add_argument('all_topics_attr', help="r for raw_image, c for compressed_image")
    args = parser.parse_args()

    bag_file = args.bag_file
    save_folder = args.save_folder
    topic_list_file = args.topic_list_file
    mkdir_if_missing(save_folder)

    topic_list = [l.strip() for l in open(topic_list_file).readlines()]

    brige = CvBridge()

    if args.all_topics_attr == "r":
        for t in topic_list:
            print osp.join(save_folder, t.split('/')[-1])
            mkdir_if_missing(osp.join(save_folder, t.split('/')[-1]))
    elif args.all_topics_attr == "c":
        names = []
        for t in topic_list:
            t = t.split('/')
            name = ""
            for idx, item in enumerate(t):
                if idx == 0 or idx == 1:
                    name += item
                else:
                    name += ("_" + item)
            names.append(name)

            print osp.join(save_folder, name)
            mkdir_if_missing(osp.join(save_folder, name))

    else:
        print "input error !!!"

    cnt = 0
    flag = False
    with rosbag.Bag(bag_file, 'r') as bag:
        for topic, msg, stamp in bag.read_messages():
            if hasattr(msg, "header") and flag == False:
                rostime_sec = msg.header.stamp.secs
                rostime_nsec = msg.header.stamp.nsecs
            else:
                if flag == False:
                    ROS_ERROR("This msg has no header !!! So we will use bag timestamp as image names !!! This may incur time skewing!!!")
                    flag = True
                rostime_sec = stamp.secs
                rostime_nsec = stamp.nsecs

            stamp = str(rostime_sec).zfill(10)+ "." + str(rostime_nsec).zfill(9)
            print "stamp is", stamp

            if topic in topic_list:
                # pass
                cnt += 1
                sys.stdout.write('\r[%d]' % cnt)
                sys.stdout.flush()
                if args.all_topics_attr == "r":
                    save_img(osp.join(save_folder, topic.split('/')[-1]), msg, stamp)
                elif args.all_topics_attr == "c":
                    index = topic_list.index(topic)
                    save_img_compressed(osp.join(save_folder, names[index]), msg, stamp)

    print cnt
