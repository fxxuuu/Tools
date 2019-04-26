# -*- coding: utf-8 -*-
import os
import sys
import time
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('orig_pathlist')
    parser.add_argument('hf_file')
    parser.add_argument('save_folder')
    args = parser.parse_args()

    ## MVP_data_set_20180907_undis/case5_test7/surround_cam/undis_image/camera00/1504655315873.jpg

    orig_path_lines = [l.strip() for l in open(args.orig_pathlist, 'r').readlines()]
    hf_lines = [l.strip() for l in open(args.hf_file, 'r').readlines()]

    case_num_list = [1, 2, 3, 4, 5, 6]
    fp_dict = {}
    for i in case_num_list:
        fp_dict[i] = open(os.path.join(args.save_folder, "case"+str(i)+".list"), 'w')
        fp_dict[i+100] = open(os.path.join(args.save_folder, "case"+str(i)+".hf"), "w")


    for idx, path_line in enumerate(orig_path_lines):
        path_line = path_line.split("/")
        case_info = path_line[1].split("_")[0]
        case_num = int(case_info[4:])

        fp_dict[case_num].write(orig_path_lines[idx] + "\n")
        fp_dict[case_num+100].write(hf_lines[idx] + "\n")



