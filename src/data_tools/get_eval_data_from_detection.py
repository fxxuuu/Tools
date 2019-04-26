import os
import random
import json
import numpy as np

gt_hf_path = '/share10/public/fanggao/eval_data/alignmetDataset/human/tsinghua1h/human_box_testset_v4.hf'
det_hf_path = '/share10/public/fanggao/eval_data/alignmetDataset/human/tsinghua1h/gather_predict.hf'
im_path_path = '/share10/public/fanggao/eval_data/alignmetDataset/human/tsinghua1h/human_box_testset_v4_origin_path.list'
wh_path = '/share10/public/fanggao/eval_data/alignmetDataset/human/tsinghua1h/human_box_testset_v4.wh'
save_neg = '/share10/public/fanggao/eval_data/alignmetDataset/human/tsinghua1h/tsinghua_neg.data'
save_pos = '/share10/public/fanggao/eval_data/alignmetDataset/human/tsinghua1h/tsinghua_pos.data'



def get_iou(bb, bbgt):
    bi = [np.max((bb[0], bbgt[0])), np.max((bb[1], bbgt[1])), np.min((bb[2], bbgt[2])), np.min((bb[3], bbgt[3]))]
    iw = bi[2] - bi[0] + 1
    ih = bi[3] - bi[1] + 1
    if iw > 0 and ih > 0:
        # compute overlap as area of intersection / area of union
        ua = (bb[2] - bb[0] + 1.) * (bb[3] - bb[1] + 1.) + \
             (bbgt[2] - bbgt[0] + 1.) * \
             (bbgt[3] - bbgt[1] + 1.) - iw * ih
        ov = iw * ih / ua
        return ov
    return 0.0

def get_ioo(bb, bbgt):
    bi = [np.max((bb[0], bbgt[0])), np.max((bb[1], bbgt[1])), np.min((bb[2], bbgt[2])), np.min((bb[3], bbgt[3]))]
    iw = bi[2] - bi[0] + 1
    ih = bi[3] - bi[1] + 1
    if iw > 0 and ih > 0:
        # compute overlap as area of intersection / area of union
        ua = (bb[2] - bb[0] + 1.) * (bb[3] - bb[1] + 1.)
        ov = iw * ih / ua
        return ov
    return 0.0


def gen_eval_data():
    with open(gt_hf_path, 'r') as gt_file, open(det_hf_path, 'r') as det_file, open(im_path_path, 'r') as im_path_file, \
            open(save_neg, 'w') as neg_file, open(save_pos, 'w') as pos_file, open(wh_path, 'r') as wh_file:
        gt_list = gt_file.readlines()
        det_list = det_file.readlines()
        wh_list = wh_file.readlines()
        im_list = im_path_file.readlines()
        for idx in range(len(gt_list)):
            gt_data = gt_list[idx].strip()
            det_data = det_list[idx].strip()
            im_data = im_list[idx].strip()
            wh_data = [int(wh_list[idx].strip().split(' ')[i]) for i in range(2)]
            s_g_d = gt_data.split(' ')
            s_d_d = det_data.split(' ')
            gt_num = int(s_g_d[0])
            det_num = int(s_d_d[0])
            neg_boxes = []
            pos_boxes = []
            gt_boxes = []
            for gt_idx in range(gt_num):
                box_info = {}
                box_info['box'] = [float(s_g_d[1 + gt_idx * 5 + i]) for i in range(4)]
                box_info['visual'] = int(s_g_d[1 + gt_idx * 5 + 4])
                gt_boxes.append(box_info)
            for det_idx in range(det_num):
                det_box_info = {}
                det_box_info['box'] = [float(s_d_d[1 + det_idx * 5 + i]) for i in range(4)]
                det_box_info['conf'] = float(s_d_d[1 + det_idx * 5 + 4])
                is_neg = True
                for gt_id in range(gt_num):
                    if get_iou(det_box_info['box'], gt_boxes[gt_id]['box']) > 0.5:
                        if gt_boxes[gt_id]['visual'] == 2:
                            a_pos_box = {}
                            a_pos_box['det'] = det_box_info['box']
                            a_pos_box['gt'] = gt_boxes[gt_id]['box']
                            pos_boxes.append(a_pos_box)
                    if get_iou(det_box_info['box'], gt_boxes[gt_id]['box']) > 0.3 or \
                            get_ioo(det_box_info['box'], gt_boxes[gt_id]['box']) > 0.3:
                        is_neg = False
                        break
                if is_neg:
                    a_neg_box = {}
                    a_neg_box['det'] = det_box_info['box']
                    a_neg_box['gt'] = [0, 0, 0, 0]
                    neg_boxes.append(a_neg_box)
            if len(pos_boxes):
                pos_file.write(json.dumps([im_data, wh_data, pos_boxes]) + '\n')
            if len(neg_boxes):
                neg_file.write(json.dumps([im_data, wh_data, neg_boxes]) + '\n')


def gen_neg_sample():
    with open(gt_hf_path, 'r') as gt_file, open(det_hf_path, 'r') as det_file, open(im_path_path, 'r') as im_path_file, \
            open(save_neg, 'w') as neg_file:
        gt_list = gt_file.readlines()
        det_list = det_file.readlines()
        im_list = im_path_file.readlines()
        for idx in range(len(gt_list)):
            gt_data = gt_list[idx].strip()
            det_data = det_list[idx].strip()
            im_data = im_list[idx].strip()
            s_g_d = gt_data.split(' ')
            s_d_d = det_data.split(' ')
            gt_num = int(s_g_d[0])
            det_num = int(s_d_d[0])
            gt_boxes = []
            for gt_idx in range(gt_num):
                box_info = {}
                box_info['box'] = [float(s_g_d[1 + gt_idx * 5 + i]) for i in range(4)]
                box_info['visual'] = int(s_g_d[1 + gt_idx * 5 + 4])
                gt_boxes.append(box_info)
            for det_idx in range(det_num):
                det_box_info = {}
                det_box_info['box'] = [float(s_d_d[1 + det_idx * 5 + i]) for i in range(4)]
                det_box_info['conf'] = float(s_d_d[1 + det_idx * 5 + 4])
                is_neg = True
                for gt_id in range(gt_num):
                    if get_iou(det_box_info['box'], gt_boxes[gt_id]['box']) > 0.2 or \
                            get_ioo(det_box_info['box'], gt_boxes[gt_id]['box']) > 0.2:
                        is_neg = False
                        break
                if is_neg:
                    s = im_data + ' {} {} {} {}\n'.format(det_box_info['box'][0], det_box_info['box'][1],
                                                        det_box_info['box'][2], det_box_info['box'][3])
                    neg_file.write(s)


gen_neg_sample()
