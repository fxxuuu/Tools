#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

if __name__ == "__main__":

    print "here"

    prefix1 = "/share10/public/fangxin/mvp_data/5_2_valid_data/"
    hf_list = open(prefix1 + "human.hf","r").readlines()
    #hf_nopnt_list = open(prefix1 + "human_keypoints_upground_noPnt.hf", "r").readlines()
    path_list = open(prefix1 + "human_imag_path.list", "r").readlines()
    md5_list = open(prefix1 + "human_md5.list", "r").readlines()
    wh_list = open(prefix1 + "human_mvp.wh", "r").readlines()

    #prefix2 = "/share10/public/wangtong/testset_images/mvp_2.3w_dongsheng/"
    prefix2 = "/share10/public/momenta_train_images/"

    output_dir = "/share10/public/fangxin/mvp_data/5_2_valid_data/"
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    hf_list_valid = open(output_dir + "human_new.hf", "w")
    #hf_nopnt_list_valid = open(output_dir + "human_keypoints_upground_noPnt.hf", "w")
    path_list_valid = open(output_dir + "human_imag_path_new.list", "w")
    md5_list_valid = open(output_dir + "human_md5_new.list", "w")
    wh_list_valid = open(output_dir + "human_mvp_new.wh", "w")

    '''
    output_dir_2 = "/share10/public/fangxin/waist_workspace/hgt_workspace/hgt_file/train_file/upground/6-5-invalid/"
    if not os.path.isdir(output_dir_2):
        os.makedirs(output_dir_2)
    hf_list_invalid = open(output_dir_2 + "human_keypoints_upground.hf", "w")
    hf_nopnt_list_invalid = open(output_dir_2 + "human_keypoints_upground_noPnt.hf", "w")
    path_list_invalid = open(output_dir_2 + "human_keypoints_upground_origin_path.list", "w")
    md5_list_invalid = open(output_dir_2 + "human_keypoints_upground_md5.list", "w")
    wh_list_invalid = open(output_dir_2 + "human_keypoints_upground.wh", "w")
    '''

    f1 = open("/share10/public/fangxin/eval_results/deploy_result/deploy_all_/gather_predict.hf", "r").readlines()
    f2 = open("/share10/public/fangxin/eval_results/deploy_result/deploy_all_/gather_predict_new.hf", "w")

    len = len(hf_list)
    print len
    cnt = 0
    for i in range(len):
        image_path = path_list[i].strip()
        if ' (' in image_path:
            continue
        else:
            cnt += 1
            hf_list_valid.write(hf_list[i].strip() + "\n")
            path_list_valid.write(path_list[i].strip() + "\n")
            md5_list_valid.write(md5_list[i].strip() + "\n")
            wh_list_valid.write(wh_list[i].strip() + "\n")
            f2.write(f1[i].strip() + "\n")

    print cnt
    f1.close()
    f2.close()

    '''
    hf_list_len = len(hf_list)
    print hf_list_len
    count = 0
    err_count = 0
    for i in range(hf_list_len):
        image_path = path_list[i].strip()
        if os.path.isfile(prefix2 + image_path) == True:
            count += 1
            hf_list_valid.write(hf_list[i].strip() + "\n")
            hf_nopnt_list_valid.write(hf_nopnt_list[i].strip() + "\n")
            path_list_valid.write(path_list[i].strip() + "\n")
            md5_list_valid.write(md5_list[i].strip() + "\n")
            wh_list_valid.write(wh_list[i].strip() + "\n")
        else:
            err_count += 1
            print "open image:", prefix2, image_path , "error!"
            hf_list_invalid.write(hf_list[i].strip() + "\n")
            hf_nopnt_list_invalid.write(hf_nopnt_list[i].strip() + "\n")
            path_list_invalid.write(path_list[i].strip() + "\n")
            md5_list_invalid.write(md5_list[i].strip() + "\n")
            wh_list_invalid.write(wh_list[i].strip() + "\n")

    print "original image num:", hf_list_len
    print "valid image num:", count
    print "invalid image num:", err_count
    '''



