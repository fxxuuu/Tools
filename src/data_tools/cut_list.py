# -*- coding: utf-8 -*-
import os
import sys
import time
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('total_list')
    parser.add_argument('del_list')
    parser.add_argument('save_file')
    args = parser.parse_args()

    total_list_lines = [l.strip() for l in open(args.total_list, 'r').readlines()]
    del_list_lines = [l.strip() for l in open(args.del_list, 'r').readlines()]

    left = list(set(total_list_lines).difference(set(del_list_lines)))
    print len(total_list_lines), len(del_list_lines)
    print len(left)

    with open(args.save_file, 'w') as fp:
        for item in left:
            fp.write(item + "\n")
