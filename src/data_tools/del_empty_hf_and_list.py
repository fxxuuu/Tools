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

    if not os.path.isdir(args.save_folder):
        os.makedirs(args.save_folder)

    orig_path_lines = [l.strip() for l in open(args.orig_pathlist, 'r').readlines()]
    hf_lines = [l.strip() for l in open(args.hf_file, 'r').readlines()]

    with open(os.path.join(args.save_folder, "img.hf"), 'w') as f1:
        with open(os.path.join(args.save_folder, "img.list"), 'w') as f2:
            for idx, hf in enumerate(hf_lines):
                if hf[0] != "0":
                    f1.write(hf+"\n")
                    f2.write(orig_path_lines[idx]+"\n")

    print "done!"
