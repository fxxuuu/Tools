# -*- coding: utf-8 -*-
import os
import sys
import time
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('total_list')
    parser.add_argument('save_file')
    args = parser.parse_args()

    total_list_lines = [l.strip() for l in open(args.total_list, 'r').readlines()]

    print len(total_list_lines)

    with open(args.save_file, 'w') as fp:
        for path in total_list_lines:
            dir, filename = os.path.split(path)
            fp.write(filename + "\n")

    print "done!"

