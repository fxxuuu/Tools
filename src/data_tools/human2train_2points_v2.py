# -*- coding: utf-8 -*-
'''
This script is used to transfer human_format data to ".data" format data
'''
import numpy as np
import argparse
import cPickle as pk
import json
import os
import sys
import copy

DEBUG = True

def flip_boxes(raw_boxes, width_t):
    boxes = []
    for r_box in raw_boxes:
        box_temp = []
        for x in r_box:
            box_temp.append(x)
        temp = box_temp[0]
        box_temp[0] = width_t - box_temp[2] - 1
        box_temp[2] = width_t -temp - 1
        boxes.append(box_temp)
    return boxes

def dump_fmt_data(fmt_data_obj, save_file):
    assert type(fmt_data_obj) == dict and 'data' in fmt_data_obj and 'info' in fmt_data_obj
    dp_data = [json.dumps(item)+'\n' for item in fmt_data_obj['data']]
    dp_info = json.dumps(fmt_data_obj['info']) + '\n'
    dp_out = [dp_info] + dp_data
    fd = os.path.dirname(save_file)
    if len(fd) and not os.path.isdir(fd):
        os.makedirs(fd)
    with open(save_file, 'w') as ft:
        ft.writelines(dp_out)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('img_list')
    parser.add_argument('hf_path')
    parser.add_argument('wh_path')
    parser.add_argument('img_root')
    parser.add_argument('save_file')
    parser.add_argument('-ig', dest='with_ignore',default=1, type=int)
    parser.add_argument('-n', dest='top_n', help='only load top_n images', default=-1, type=int)
    args = parser.parse_args()
    img_list, hf_path, wh_path, img_root, save_file, with_ignore, with_Pnt, top_n = args.img_list, args.hf_path, args.wh_path, args.img_root, args.save_file, args.with_ignore, args.with_Pnt, args.top_n


    bbox_width_orig = 5
    keypoints_num = 4 ## 4 points -> 2 points in use
    bbox_width = bbox_width_orig + 4 * 3 ## 17
    data = []

    invalid_pic_num = 0

    '''
    handle error hgt choices:
    1 -> regard them as ignore boxes
    2 -> regard them as if there are no boxes
    '''
    handle_error_hgt_choice = 1
    count_error_hgt = 0

    img_list_lines = [l.strip() for l in open(img_list, 'r').readlines()]
    wh_lines = [l.strip() for l in open(wh_path, 'r').readlines()]
    hf_lines = [l.strip() for l in open(hf_path, 'r').readlines()]
    assert len(img_list_lines) == len(wh_lines) and len(wh_lines) == len(hf_lines)

    for idx, img_path in enumerate(img_list_lines):

        if idx % 1000 == 0:
            sys.stdout.write('\r{}/{}, error_hgt:{}, invalid_pic_num:{}'.format(idx, len(hf_lines), count_error_hgt, invalid_pic_num))
            sys.stdout.flush()

        if 0 < top_n < len(img_list_lines) and idx >= top_n:
            break
        width, height = wh_lines[idx].split(" ")

        if width == "[-1]":
            width = "-1"
        elif width[0] == "[": # the wh_file from yuhang has format like : [width] height
            width = width[1:-1]
        else:
            width = width

        if float(width) == -1 or float(height) == -1:  # filter invalid images
            invalid_pic_num += 1
            continue
        if " " in img_path:
            invalid_pic_num += 1
            continue

        hf_line = hf_lines[idx].split()  #string format
        label_info = [float(v) for v in hf_line]
        bbox_scores = label_info[5 :: bbox_width]
        # waist_hgt = label_info[bbox_width-1::bbox_width]

        if DEBUG:
            print 'bbox_scores:', bbox_scores

        im_label = {'gt_classes':[], 'gt_boxes':[], 'gt_ignore_classes':[], 'gt_ignore_boxes':[], 'flipped':False}
        box_count = int(hf_line[0])
        assert box_count == len(bbox_scores)
        for i in range(box_count):
            if bbox_scores[i] == 2: # valid bbox
                im_label['gt_classes'].append(1)

                box = label_info[1 + i * bbox_width : 5 + i * bbox_width]
                keypoints = label_info[6 + i * bbox_width : bbox_width + 1 + i * bbox_width]
                shoulder_x1, shoulder_y1, shoulder_x2, shoulder_y2 = keypoints[0:4]
                waist_x1, waist_y1, waist_x2, waist_y2 = keypoints[4:8]
                shoulder_v1, shoulder_v2, waist_v1, waist_v2 = keypoints[8:12]

                if shoulder_v1 == 0 or shoulder_v2 == 0 or waist_v1 == 0 or waist_v2 == 0:  ## 四个点中有一个点未标注，则这个gt框丢弃(比例非常低，不影响)
                    continue ## filter invalid gt_box

                shoulder_x = (shoulder_x1 + shoulder_x2) / 2.0
                shoulder_y = (shoulder_y1 + shoulder_y2) / 2.0
                shoulder_v = 1 if (shoulder_v1 == 1 and shoulder_v2 == 1) else 2
                waist_x = (waist_x1 + waist_x2) / 2.0
                waist_y = (waist_y1 + waist_y2) / 2.0
                waist_v = 1 if (waist_v1 == 1 and waist_v2 == 1) else 2


                gt_box = []
                gt_box.extend(box)
                gt_box.extend([])
                im_label['gt_boxes'].append(gt_box)

            else: # ignore bbox
                if with_ignore == 1:
                    im_label['gt_ignore_classes'].append(1)
                    im_label['gt_ignore_boxes'].append(label_info[(1 + i * bbox_width):(bbox_width + i * bbox_width)])
        # print height, width
        data.append({'file_name': img_path, 'size': (float(height), float(width)), 'labels': im_label})


    fmt_data = {'data': data, 'info': {'img_prefix': img_root}}
    for d in data:
        for k,v in d['labels'].items():
            if type(v) == np.ndarray:
                d['labels'][k] = v.tolist()
    dump_fmt_data(fmt_data, save_file)
    print '\nconverted {} to {}.'.format(len(data), save_file)


