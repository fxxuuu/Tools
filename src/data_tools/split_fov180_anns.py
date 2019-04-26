#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import argparse
import random
import sys

def get_filename(rootDir):
    file_list = []
    for file in os.listdir(rootDir):
        file_list.append(file)
    file_list.sort()
    return file_list

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('hf_file')
    parser.add_argument('path_list')
    parser.add_argument('wh_file')
    parser.add_argument('save_folder')
    args = parser.parse_args()

    hf_file, path_list, wh_file, save_folder = args.hf_file, args.path_list, args.wh_file, args.save_folder

    with open(hf_file, "r") as f:
        hf_lines = [l.strip() for l in f.readlines()]
    with open(path_list, "r") as f:
        path_lines = [l.strip() for l in f.readlines()]
    with open(wh_file, "r") as f:
        wh_lines = [l.strip() for l in f.readlines()]

    length = len(hf_lines)
    print "file length: ", length

    if not os.path.isdir(save_folder):
        os.makedirs(save_folder)

    fov144_path = open(os.path.join(save_folder, "Fisheye_fov144.list"), "w")
    fov144_hf = open(os.path.join(save_folder, "Fisheye_fov144.hf"), "w")
    fov144_wh = open(os.path.join(save_folder, "Fisheye_fov144.wh"), "w")
    fov180_path = open(os.path.join(save_folder, "Fisheye_fov180.list"), "w")
    fov180_hf = open(os.path.join(save_folder, "Fisheye_fov180.hf"), "w")
    fov180_wh = open(os.path.join(save_folder, "Fisheye_fov180.wh"), "w")


    for idx, path in enumerate(path_lines):
        sys.stdout.write('\r{} / {}'.format(idx, length))
        sys.stdout.flush()
        try:
            if "undis_image" in path:
                fov144_hf.write(hf_lines[idx] + "\n")
                fov144_path.write(path_lines[idx] + "\n")
                fov144_wh.write(wh_lines[idx] + "\n")
            elif "origin_image" in path:
                fov180_hf.write(hf_lines[idx] + "\n")
                fov180_path.write(path_lines[idx] + "\n")
                fov180_wh.write(wh_lines[idx] + "\n")
        except Exception, e:
            print e


    print "\nAll done!"




