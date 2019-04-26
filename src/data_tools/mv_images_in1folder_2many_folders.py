# -*- coding=utf-8 -*-
import argparse
import os, sys
import cv2

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('path_list')
    parser.add_argument('img_root')
    parser.add_argument('save_folder')
    args = parser.parse_args()

    path_list, img_root, save_folder = args.path_list, args.img_root, args.save_folder

    img_names = [l.strip() for l in open(path_list, "r").readlines()]
    size = len(img_names)

    cnt = 0
    for img_name in img_names:
        im_path = os.path.join(img_root, img_name)
        # dest_path_pre = os.path.join(save_folder, img_name)
        #
        # dir, filename = os.path.split(dest_path_pre)
        # if not os.path.isdir(dir):
        #     os.makedirs(dir)
        folder_order1 = cnt / 100
        folder_order2 = cnt / 10000
        folder_order3 = cnt / 1000000
        cnt += 1
        sys.stdout.write('\r{}/{}'.format(cnt, size))
        sys.stdout.flush()

        tmp_dir, tmp_filename = os.path.split(img_name)

        dest_folder = os.path.join(save_folder, str(folder_order1))
        dest_path = os.path.join(dest_folder, tmp_filename)
        dir, filename = os.path.split(dest_path)
        if not os.path.isdir(dir):
            os.makedirs(dir)

        try:
            os.system("cp " + im_path + " " + dest_path)
        except Exception, e:
            print "cp ", im_path, " failed"
            print e







