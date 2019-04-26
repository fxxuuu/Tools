# -*- coding: utf-8 -*-
import sys
import os
import argparse
import hashlib



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path_file')
    parser.add_argument('md5_file')
    parser.add_argument('img_root')
    args = parser.parse_args()
    path_file, md5_file, img_root = args.path_file, args.md5_file, args.img_root

    path_list = [item.strip() for item in open(path_file, 'r').readlines()]
    size = len(path_list)

    with open(md5_file, 'w') as fout:
        for idx, path in enumerate(path_list):
            try:
                with open(os.path.join(img_root, path.strip()), 'r') as fd:
                    fcont = fd.read()
                    fmd5 = hashlib.md5(fcont).hexdigest()
                    fout.write(fmd5.strip() + "\n")

                    sys.stdout.write('\r{}/{}'.format(idx, size))
                    sys.stdout.flush()
            except Exception, e:
                print 'open ',os.path.join(img_root, path.strip()), ' error!'
                print e

