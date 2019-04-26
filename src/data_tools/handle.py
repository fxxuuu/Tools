# -*- coding: utf-8 -*-
import os, sys
import argparse

def merge(in_path, in_cf, out_path, out_cf):
    fin_path = open(in_path, 'r')
    fin_cf = open(in_cf, 'r')
    fout_path = open(out_path, 'a+')
    fout_cf = open(out_cf, 'a+')

    in_path_lines = fin_path.readlines()
    in_cf_lines = fin_cf.readlines()
    for line in in_path_lines:
        fout_path.write(line.strip() + "\n")
    for line in in_cf_lines:
        fout_cf.write(line.strip() + "\n")

    fin_cf.close()
    fin_path.close()
    fout_cf.close()
    fout_path.close()

def del_empty(in_path, in_cf, out_path, out_cf):
    in_path_lines = open(in_path, 'r').readlines()
    in_cf_lines = open(in_cf, 'r').readlines()
    fout_path = open(out_path, 'w')
    fout_cf = open(out_cf, 'w')
    out_path_lines = []
    out_cf_lines = []
    cnt = 0

    assert len(in_path_lines) == len(in_cf_lines)
    length = len(in_path_lines)
    print length

    for i in range(length):
        box_num = in_cf_lines[i].strip().split()[0]
        if box_num == '0':
            continue
        #print box_num
        out_path_lines.append(in_path_lines[i].strip() + "\n")
        out_cf_lines.append(in_cf_lines[i].strip() + "\n")
        cnt += 1
    print cnt
    for i in range(cnt):
        fout_path.write(out_path_lines[i])
        fout_cf.write(out_cf_lines[i])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('in_path')
    parser.add_argument('in_cf')
    parser.add_argument('out_path')
    parser.add_argument('out_cf')
    args = parser.parse_args()

    #merge(args.in_path, args.in_cf, args.out_path, args.out_cf)
    del_empty(args.in_path, args.in_cf, args.out_path, args.out_cf)