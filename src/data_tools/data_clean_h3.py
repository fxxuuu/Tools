# -*- coding: utf-8 -*-
import os
import sys
import time
import argparse


def del_hf_and_list_by_list(keyword, hf_lines, path_list): # keyword = "human_2_underground"
    new_hf = []
    new_path = []
    for idx, path in enumerate(path_list):
        if keyword not in path:
            new_hf.append(hf_lines[idx])
            new_path.append(path)
    return new_hf, new_path

def write_lines(lines, filename):
    with open(filename, 'w') as fp:
        for line in lines:
            fp.write(line.strip() + '\n')


def clip_file_by_list(select_path, path_list_complete, hf_list_complete, md5_list_complete):
    new_path_list, new_hf_list, new_md5_list = [], [], []
    for idx, path in enumerate(path_list_complete):
        if path in select_path:
            new_path_list.append(path)
            new_hf_list.append(hf_list_complete[idx])
            new_md5_list.append(md5_list_complete[idx])
    return new_path_list, new_hf_list, new_md5_list

def alter_hf(select_md5_list, select_hf_list, hf_list, path_list, md5_list):
    new_hf_list, new_path_list, new_md5_list = [], [], []
    for idx, md5 in enumerate(md5_list):
        if md5 in select_md5_list:





if __name__ == "__main__":

    select_path_file = "/home/fangxin/mrdk_output/35_finetune_pretrained_on_plusdistort150w_h3_fov180_sn-raw15-16-32-32-fc32-fc128_51w/end2end_deploy/scene1_and_2_384/meva_result5m/recalls_result_all_human_format/recall.list"
    path_file = "/home/fangxin/h3_workspace/1211_formal_testset/mu3_all.list"
    hf_file = "/home/fangxin/h3_workspace/1211_formal_testset/mu3_all.hf"
    md5_file = "/home/fangxin/h3_workspace/1211_formal_testset/mu3_all.md5"
    select_path_list = [l.strip() for l in open(select_path_file, 'r').readlines()]
    path_list = [l.strip() for l in open(path_file, 'r').readlines()]
    hf_list = [l.strip() for l in open(hf_file, 'r').readlines()]
    md5_list = [l.strip() for l in open(md5_file, 'r').readlines()]
    path_list, hf_list, md5_list = clip_file_by_list(select_path_list, path_list, hf_list, md5_list)

    write_lines(path_list,'/home/fangxin/mrdk_output/35_finetune_pretrained_on_plusdistort150w_h3_fov180_sn-raw15-16-32-32-fc32-fc128_51w/end2end_deploy/scene1_and_2_384/meva_result5m/recalls_result_all_human_format/mu3.list')
    write_lines(hf_list, '/home/fangxin/mrdk_output/35_finetune_pretrained_on_plusdistort150w_h3_fov180_sn-raw15-16-32-32-fc32-fc128_51w/end2end_deploy/scene1_and_2_384/meva_result5m/recalls_result_all_human_format/mu3.hf')
    write_lines(md5_list, '/home/fangxin/mrdk_output/35_finetune_pretrained_on_plusdistort150w_h3_fov180_sn-raw15-16-32-32-fc32-fc128_51w/end2end_deploy/scene1_and_2_384/meva_result5m/recalls_result_all_human_format/mu3.md5')

    # parser = argparse.ArgumentParser()
    # parser.add_argument('hf_file')
    # parser.add_argument('path_list')
    # parser.add_argument('')
    # args = parser.parse_args()
    # keyword = "human_2_underground"
    # hf_file = "/home/fangxin/mrdk_output/35_finetune_pretrained_on_plusdistort150w_h3_fov180_sn-raw15-16-32-32-fc32-fc128_51w/end2end_deploy/scene1_and_2_384/meva_result5m/recalls_result_all_human_format/img.hf"
    # path_file = "/home/fangxin/mrdk_output/35_finetune_pretrained_on_plusdistort150w_h3_fov180_sn-raw15-16-32-32-fc32-fc128_51w/end2end_deploy/scene1_and_2_384/meva_result5m/recalls_result_all_human_format/img.list"
    # hf_lines = [l.strip() for l in open(hf_file, 'r').readlines()]
    # path_list = [l.strip() for l in open(path_file, 'r').readlines()]
    #
    # hf_lines, path_list = del_hf_and_list_by_list("human_2_underground", hf_lines, path_list)
    #
    # # write_lines(hf_lines, '/home/fangxin/mrdk_output/35_finetune_pretrained_on_plusdistort150w_h3_fov180_sn-raw15-16-32-32-fc32-fc128_51w/end2end_deploy/scene1_and_2_384/meva_result5m/recalls_result_all_human_format/mu3.hf')
    # write_lines(path_list, '/home/fangxin/mrdk_output/35_finetune_pretrained_on_plusdistort150w_h3_fov180_sn-raw15-16-32-32-fc32-fc128_51w/end2end_deploy/scene1_and_2_384/meva_result5m/recalls_result_all_human_format/mu3.list')
