# -*- coding=utf-8 -*-
import argparse
import os, sys
from PIL import Image

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('path_list')
    parser.add_argument('img_prefix')
    parser.add_argument('save_file')
    args = parser.parse_args()

    path_list, img_prefix, save_file = args.path_list, args.img_prefix, args.save_file

    path_list_lines = [l.strip() for l in open(path_list, 'r').readlines()]
    fp = open(save_file, 'w')

    for idx, im_path_postfix in enumerate(path_list_lines):
        im_p = os.path.join(img_prefix, im_path_postfix)
        try:
            im = Image.open(im_p)
            w, h = im.size
            fp.write(str(w) + " " + str(h) + "\n")

        except Exception, e:
            print e
            print('open image error: ' + im_p)
            fp.write("-1 -1\n")

        if not idx % 1000:
            sys.stdout.write('\r[%d/%d]' % (idx, len(path_list_lines)))
            sys.stdout.flush()


