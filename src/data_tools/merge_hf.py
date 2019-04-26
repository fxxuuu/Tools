import time
import os
import argparse
import sys

'''
This script is used to merge 2 hf file which have the same pathlist but different bbox/scores.
'''

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('root_hf_path')
    parser.add_argument('slave_hf_path')
    parser.add_argument('save_file')
    args = parser.parse_args()

    root_hf_lines = [l.strip() for l in open(args.root_hf_path, 'r').readlines()]
    slave_hf_lines = [l.strip() for l in open(args.slave_hf_path, 'r').readlines()]

    with open(args.save_file, 'w') as fp:
        for idx, root_hf_line in enumerate(root_hf_lines):
            root_hf_line = root_hf_line.split()
            bbox_num_1 = int(root_hf_line[0])
            bbox_info_1 = root_hf_line[1:]
            bbox_num_2 = int(slave_hf_lines[idx].split()[0])
            bbox_info_2 = slave_hf_lines[idx].split()[1:]
            bbox_num = bbox_num_1 + bbox_num_2
            # print bbox_num
            fp.write(str(bbox_num))
            for item in bbox_info_1:
                fp.write(" " + item)
            for item in bbox_info_2:
                fp.write(" " + item)
            fp.write("\n")
