#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import argparse
import sys

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('img_list')
    parser.add_argument('img_root')
    parser.add_argument('save_folder')
    args = parser.parse_args()

    img_list_f, img_root, dest_img_root = args.img_list, args.img_root, args.save_folder


    with open(img_list_f, 'r') as fp:
        img_list = [r.strip() for r in fp.readlines()]

    cnt = 0
    for idx, line in enumerate(img_list):
        path = os.path.join(img_root, line)
        dest_path = os.path.join(dest_img_root, line)
        if not os.path.isfile(dest_path):
            try:
                cnt += 1
                dir, filename = os.path.split(dest_path)
                if not os.path.isdir(dir):
                    os.makedirs(dir)
                os.system("cp " + path + " " + dest_path)
                # os.system("mv " + path + " " + dest_path)
            except Exception, e:
                print e
        sys.stdout.write('\r{}, {} / {}'.format(idx, cnt, len(img_list)))
        sys.stdout.flush()

    # cnt = 0
    # for idx, line in enumerate(img_list):
        # path = os.path.join(img_root, line)
        # if os.path.isfile(path):
            # try:
                # cnt += 1
                # os.system("rm " + path)
            # except Exception, e:
                # print e
        # sys.stdout.write('\r{}, {} / {}'.format(idx, cnt, len(img_list)))
        # sys.stdout.flush()
