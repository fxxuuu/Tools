# -*- coding: utf-8 -*-
import numpy as np
import cv2
from random import randint
import copy
import math
import os
import time
import logging
import sys
import argparse
import boto3
from datetime import datetime


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path_list')
    parser.add_argument('img_root')
    parser.add_argument('save_folder')
    args = parser.parse_args()

    path_lines = [l.strip() for l in open(args.path_list, 'r').readlines()]
    for idx, filename in enumerate(path_lines):
        im_path = os.path.join(args.img_root, filename)
        im = cv2.imread(im_path)
        if im is None:
            logging.fatal('Load image %s failed!' % im_path)

        imgflip = cv2.flip(im, 1)
        im_path_new = os.path.join(args.save_folder, filename)
        dir, filename = os.path.split(im_path_new)
        if not os.path.isdir(dir):
             os.makedirs(dir)
        try:
            cv2.imwrite(im_path_new, imgflip)
            sys.stdout.write('\r{} / {}'.format(idx, len(path_lines)))
            sys.stdout.flush()
        except Exception, e:
            print e
