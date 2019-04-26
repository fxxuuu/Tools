import os, sys
import argparse
import threading
import time
from Queue import Queue
import shutil


def exec_cmd(q, save_folder, total_num, count):
    while True:
        im_p = q.get()
        if im_p == -1:
            break
        try:
            if not os.path.exists(os.path.join(save_folder, im_p)):
                shutil.copyfile(im_p, os.path.join(save_folder, im_p))
            count[0] += 1
            if not count[0] % 100:
                sys.stdout.write('\r[%d/%d]' % (count[0], total_num))
                sys.stdout.flush()
        except Exception as e:
            print e
            print('Copy error: '+im_p)

        q.task_done()


def cp_files(args):
    th_num = args.thread_num
    img_src = args.img_src
    save_folder = args.save_folder
    assert th_num >= 1, 'thread_num should be positive!'
    assert os.path.isdir(img_src), 'IMG_SRC PATH ERROR: ' + img_src

    folder = os.getcwd()
    print('Current folder: ' + folder)
    if save_folder[0] != '/':
        save_folder = os.path.join(folder, save_folder)
    if not os.path.isdir(save_folder):
        os.makedirs(save_folder)

    cp_list = []
    with open(args.cp_list) as f:
        for line in f:
            line = line.rstrip('\n')
            cp_list.append(line)

    total_num = len(cp_list)
    cp_num = args.cp_num
    if cp_num:
        assert cp_num <= total_num, 'cp files exceed max!'
        cp_list = cp_list[:cp_num]
        total_num = cp_num

    print('ready to cp: %d (multi_thread: %d)' % (total_num, th_num))
    th = time.time()

    cp_count = [0]
    q = Queue()
    for i in xrange(th_num):
        t = threading.Thread(target=exec_cmd, args=(q, save_folder, total_num, cp_count,))
        t.start()

    for im_p in cp_list:
        save_p = os.path.join(save_folder, im_p)
        pre_fld, _ = os.path.split(save_p)
        if not os.path.isdir(pre_fld):
            os.makedirs(pre_fld)

    os.chdir(img_src)
    for im_p in cp_list:
        q.put(im_p)

    q.join()
    for i in xrange(th_num):
        q.put(-1)
    print ('\tdone in %.6fs' % (time.time() - th))
    print('\ncopied %d to %s.'%(cp_count[0], save_folder))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cp_list')
    parser.add_argument('img_src')
    parser.add_argument('save_folder')
    parser.add_argument('-n', dest='cp_num', default=None, type=int)
    parser.add_argument('-t', dest='thread_num', default=8, type=int)
    args = parser.parse_args()

    cp_files(args)

