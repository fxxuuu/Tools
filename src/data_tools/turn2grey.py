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
    cnt = 0
    size = len(img_names)
    for img_name in img_names:
        im_path = os.path.join(img_root, img_name)
        dest_path = os.path.join(save_folder, img_name)

        dir, filename = os.path.split(dest_path)
        if not os.path.isdir(dir):
            os.makedirs(dir)

        if not os.path.isfile(dest_path):
            try:
                cnt += 1
                sys.stdout.write('\r{}/{}'.format(cnt, size))
                sys.stdout.flush()

                im = cv2.imread(im_path, cv2.IMREAD_GRAYSCALE)
                # print im.shape
                cv2.imwrite(dest_path, im)

            except Exception, e:
                print "open image ", im_path, " error!"
                print e

    print "\ndone!"