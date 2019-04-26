from mrdk.det.utils import crop_image_with_labels, prep_im_for_blob, bbox_transform_inv, clip_boxes, \
    load_fmt_batch_data, get_detection_net_info, im_to_blob, nms, parallel_cpu_nms
from mrdk.det.rpn import TargetGenerator, AnchorGenerator
from pyrocs import deployCallback
from pyrocs.core.callbacks import Callback

from pyrocs.env import RootOnly
import logging
import numpy as np
from random import randint

import os
import argparse
import cPickle
from pyrocs.env import RootOnly, MPI_rank, MPI, MPI_size

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('orig_hf_path')
    parser.add_argument('save_file')
    args = parser.parse_args()

    low_th = 0
    nms_th = 0.3
    gpu_id = 0

    orig_hf_lines = [l.strip() for l in open(args.orig_hf_path, 'r').readlines()]
    for idx, hf_line in enumerate(orig_hf_lines):
        hf_line = hf_line.split()
        bbox_num = int(hf_line[0])
        bbox_info = list(map(float, hf_line[1:]))


        scores = []
        boxes = []
        for i in range(bbox_num):
            scores.append([bbox_info[5*i+4]])
            boxes.extend(bbox_info[5*i: 5*i+4])
        # print scores
        # print boxes
        # print '---'
        scores = [np.array(scores, dtype=np.float32)]
        # scores = scores.astype(np.float32)
        boxes = [np.array(np.reshape(boxes, (bbox_num, 4)),dtype=np.float32)]
        # boxes = boxes.astype(np.float32)


        for i in range(len(boxes)):
            keep = np.where(scores[i] >= low_th)[0]
            boxes[i] = boxes[i][keep, :]
            scores[i] = scores[i][keep]
            print scores
            print boxes
            # print type(scores), type(boxes)
            print 'hhhhh'
            if bbox_num != 0:
                keep = nms(np.hstack((boxes[i], scores[i])), nms_th, True, gpu_id)
                boxes[i] = boxes[i][keep, :]
                scores[i] = scores[i][keep]
            else:
                boxes[i] = []
                scores[i] = []
            print boxes[i], scores[i]


        assert len(boxes) == len(scores)
        out_str = ''
        total_num = 0
        for _bbox, _score in zip(boxes, scores):
            num = len(_score)
            for i in range(num):
                x1, y1, x2, y2 = _bbox[i].tolist()
                s = _score[i]

                # x1,y1,x2,y2,score
                _str = '%.3f %.3f %.3f %.3f %.6f ' % (x1, y1, x2, y2, s)

                out_str += _str
            total_num += num
        out_line = '%d %s\n' % (total_num, out_str.rstrip())
        with open(args.save_file, 'a') as ft:
            ft.write(out_line)