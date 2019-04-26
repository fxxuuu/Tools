#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import argparse
import random

def get_filename(rootDir):
    file_list = []
    for file in os.listdir(rootDir):
        file_list.append(file)
    file_list.sort()
    return file_list

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('sample_number')
    parser.add_argument('source_folder')
    parser.add_argument('save_folder')
    args = parser.parse_args()
    sample_n, src_folder, save_folder = args.sample_number, args.source_folder, args.save_folder

    file_list = get_filename(src_folder)
    with open(os.path.join(src_folder, file_list[0]), "r") as f:
        length = len(f.readlines())
        print "file length: ", length

    sample_index = random.sample(range(0, length), int(sample_n))
    cnt = 0
    print sample_index

    if not os.path.isdir(save_folder):
        os.mkdir(save_folder)



    for file_name in file_list:
        with open(os.path.join(src_folder, file_name), "r") as fin, open(os.path.join(save_folder, file_name), "w") as fout:
            lines = [line.strip() for line in fin.readlines()]
            for ind in sample_index:
                cnt += 1
                # print cnt
                fout.write(lines[ind] + "\n")

    print "\nAll done!"




