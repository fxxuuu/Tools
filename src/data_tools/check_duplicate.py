# -*- coding: utf-8 -*-
import os
import sys
import time
import argparse





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('pathlist_1')
    parser.add_argument('pathlist_2')
    args = parser.parse_args()

    path_list_1 = [l.strip() for l in open(args.pathlist_1, 'r').readlines()]
    path_list_2 = [l.strip() for l in open(args.pathlist_2, 'r').readlines()]
    joint = list(set(path_list_1).intersection(set(path_list_2)))
    print len(joint)

    with open("duplicate.list", 'w') as fp:
        for item in joint:
            fp.write(item.strip() + "\n")
