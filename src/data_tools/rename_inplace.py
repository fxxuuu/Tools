#coding:utf8
import os
import sys
import argparse

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

def rename(rootDir):
    cnt = 0
    paths = get_recursive_filename(rootDir, 0)
    for path in paths:
        # print filename
        dir, filename = os.path.split(path)
        if filename[-3:] == 'jpg':
            if not os.path.isdir(dir):
                os.makedirs(dir)
            new_path = os.path.join(dir, "%05d.jpg" % cnt)
            cnt += 1
            # print cnt
            # os.system("mv " + path + " " + new_path)
            os.rename(path, new_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('rootDir')
    args = parser.parse_args()

    rename(args.rootDir)
