#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('path_list')
    parser.add_argument('img_prefix')
    # parser.add_argument('save_file')
    args = parser.parse_args()

    with open(args.path_list, 'r') as fp:
        img_list = [r.strip() for r in fp.readlines()]
    img_root = args.img_prefix

    cnt = 0
    for idx, line in enumerate(img_list):
        path = os.path.join(img_root, line)
        if os.path.isfile(path):
            try:
                cnt += 1
                os.system("rm " + path)
            except Exception, e:
                print e
        sys.stdout.write('\r{}, {} / {}'.format(idx, cnt, len(img_list)))
        sys.stdout.flush()
