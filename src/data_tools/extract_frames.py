# -*- coding=utf-8 -*-
import argparse
import os, sys
from PIL import Image

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('path_list')
    parser.add_argument('save_file')
    parser.add_argument('interval', type=int)
    args = parser.parse_args()

    path_list, save_file = args.path_list, args.save_file

    path_list_lines = [l.strip() for l in open(path_list, 'r').readlines()]
    fp = open(save_file, 'w')

    cnt = 0
    for idx, im_path_postfix in enumerate(path_list_lines):
        if idx % args.interval  == 0:
            cnt += 1
            fp.write(im_path_postfix + "\n")
        if not cnt % 10:
            sys.stdout.write('\r[%d/%d]' % (cnt, len(path_list_lines)))
            sys.stdout.flush()

    fp.close()
    print "\n\nFile length after extraction is :", cnt
    print "\nAll done!"



