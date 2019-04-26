# -*- coding: utf-8 -*-
import os,shutil
import sys
import argparse

def write_pathlist(filenames):
    fout = open("img.list","w")
    for filename in filenames:
        fout.write(filename + "\n")
    print len(filenames)
    fout.close()

def move_images(filename):
    image_lines = open(filename, "r").readlines()
    for line in image_lines:
        shutil.move("images/"+line.strip() , "100_images/")



def get_filename(rootDir):
    path_list = []
    for lists in os.listdir(rootDir):
       #如果找到的是图片，则打印出来
        if lists[-3:]=='jpg':
            print lists
            path_list.append(lists)
    path_list.sort()
    return path_list

def get_recursive_filename(rootDir, start_num):
    path_list = []
    cnt = 0
    for dirpath, dirnames, filenames in os.walk(rootDir):
        filenames.sort()
        for filename in filenames:
            if filename[-3:] == 'jpg':
            # if filename[-3:] == 'png':
                # print filename
                '''
                你可能需要修改这里
                '''
                path_new = os.path.join(dirpath, filename).split("/")[start_num:]
                str = ""
                for idx, item in enumerate(path_new):
                    if idx == 0:
                        str += item
                    else:
                        str += "/" + item
                print str
                # cnt += 1
                # sys.stdout.write('\r{}'.format(cnt))
                # sys.stdout.flush()
                path_list.append(str)
    path_list.sort()
    return path_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('rootdir')
    parser.add_argument('start_num', type=int)
    args = parser.parse_args()
    rootdir, start_num = args.rootdir, args.start_num

    filenames = get_recursive_filename(rootdir, start_num)
    write_pathlist(filenames)
