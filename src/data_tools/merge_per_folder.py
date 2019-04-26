# -*- coding: utf-8 -*-
import os, sys
import argparse

def merge(in_folder, save_file):

    filenames = get_filename(in_folder)

    with open(save_file, 'w') as fout:
        for filename in filenames:
            with open(filename, 'r') as fp:
                lines = [l.strip() for l in fp.readlines()]
            for line in lines:
                fout.write(line + '\n')
            print "\nwrite ", filename, " done."
        print "\n\n All done!"

def get_filename(rootDir):
    path_list = []
    for lists in os.listdir(rootDir):
        if lists[-4:]=='list':
            print lists
            path_list.append(lists)
    path_list.sort()
    return path_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('in_folder')
    parser.add_argument('save_file')
    args = parser.parse_args()

    merge(args.in_folder, args.save_file)

