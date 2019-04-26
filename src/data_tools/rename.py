#coding:utf8
import os
import sys
import argparse

def rename(rootDir, save_folder):
    cnt = 0
    for dirpath, dirnames, filenames in os.walk(rootDir):
        filenames.sort()
        for filename in filenames:
            if filename[-3:] == 'jpg':
                path = os.path.join(dirpath, filename)
                new_path = os.path.join(save_folder, "%05d.jpg" % cnt)
                cnt += 1
                print cnt
                os.system("cp " + path + " " + new_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('rootDir')
    parser.add_argument('save_folder')
    args = parser.parse_args()

    rootDir, save_folder = args.rootDir, args.save_folder

    if not os.path.isdir(save_folder):
        os.makedirs(save_folder)

    rename(rootDir, save_folder)

