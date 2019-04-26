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
    parser.add_argument('hf_file')
    parser.add_argument('wh_file')
    parser.add_argument('save_file')
    args = parser.parse_args()

    hf_lines = [l.strip() for l in open(args.hf_file, 'r').readlines()]
    wh_lines = [l.strip() for l in open(args.wh_file, 'r').readlines()]

    fp = open(args.save_file, 'w')

    for idx, hf_line in enumerate(hf_lines):
        hf_line = hf_line.split()
        wh_line = wh_lines[idx].split()
        w_h = list(map(float, wh_line))
        bbox_num = int(hf_line[0])
        bbox_info = list(map(float, hf_line[1:]))

        new_boxes = []
        width, height = w_h[0], w_h[1]

        for i in range(bbox_num):
            score = bbox_info[5 * i + 4]
            x1, y1, x2, y2 = bbox_info[5 * i: 5 * i + 4]
            temp = [width - x2 - 1, y1, width - x1 - 1, y2]
            new_boxes.append(temp[0])
            new_boxes.append(temp[1])
            new_boxes.append(temp[2])
            new_boxes.append(temp[3])
            new_boxes.append(float(score))
        fp.write(str(bbox_num))
        for item in new_boxes:
            fp.write(" " + str(item) )
        fp.write("\n")

    fp.close()