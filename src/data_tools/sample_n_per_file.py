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
    parser.add_argument('source_hf')
    parser.add_argument('save_hf')
    parser.add_argument('source_list')
    parser.add_argument('save_list')
    args = parser.parse_args()

    sample_n, src_hf, save_hf, src_list, save_list = args.sample_number, args.source_hf, args.save_hf, args.source_list, args.save_list

    with open(src_hf, "r") as f:
        src_hf_lines = [l.strip() for l in f.readlines()]
    with open(src_list, "r") as f:
        src_list_lines = [l.strip() for l in f.readlines()]

    length = len(src_lines)
    print "file length: ", length

    sample_index = random.sample(range(0, length), int(sample_n))
    cnt = 0

    with open(save_file, 'w') as fp:
        for ind in sample_index:
            cnt += 1
            fp.write(src_lines[ind] + '\n')
            sys.stdout.write('\r{} / {}'.format(cnt+1, length))
            sys.stdout.flush()

    print "\nAll done!"




