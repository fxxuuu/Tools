# -*- coding: utf-8 -*-
import os, sys
import argparse

def merge(file1, file2, outfile):
    fp1 = open(file1, 'r')
    fp2 = open(file2, 'r')

    file1_lines = fp1.readlines()
    file2_lines = fp2.readlines()

    fp1.close()
    fp2.close()

    fout = open(outfile, 'w')

    for line in file1_lines:
        fout.write(line.strip() + "\n")
    for line in file2_lines:
        fout.write(line.strip() + "\n")

    fout.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file1')
    parser.add_argument('file2')
    parser.add_argument('outfile')
    args = parser.parse_args()

    merge(args.file1, args.file2, args.outfile)

