#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

if __name__ == "__main__":

    print "here"

    prefix1 = "/share10/public/human/labels/train/"
    wrong_path = open(prefix1 + "wrong.path", "r").readlines()
    wrong_md5 = open(prefix1 + "wrong.md5", "r").readlines()

    prefix2 = "/share10/public/fangxin/mvp_data/valid_data/"
    data_path = open(prefix2 + "human_mvp_origin_path.list", "r").readlines()
    data_md5 = open(prefix2 + "human_mvp_md5.list", "r").readlines()

    hf_list_len = len(data_path)

    wrong_path_set = set(wrong_path)
    data_path_set = set(data_path)
    aaaa = wrong_path_set & data_path_set
    print aaaa

    print "original image num:", hf_list_len
    print "wrong image num:", len(aaaa)



