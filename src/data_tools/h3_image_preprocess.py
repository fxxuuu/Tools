# coding=utf-8
from PIL import Image
import cv2 as cv
import numpy as np
import os, argparse


def preprocess(path_list, img_root, width, height, save_folder):
    with open(path_list, 'r') as fp:
        path_lines = [l.strip() for l in fp.readlines()]
    for line in path_lines:
        im_path = os.path.join(img_root, line)
        if line[-3:] == "jpg":
            a = cv.imread(im_path)
            input_w = width
            input_h = height
            img = cv.resize(a, (input_w, input_h), interpolation=cv.INTER_LINEAR)
            img = np.array(img, dtype=np.float32)
            img_mean = np.array([[[102.9801, 115.9465, 122.7717]]]).astype(np.float32)
            img -= img_mean.astype(np.float32, copy=False)

            img = img.transpose((2, 0, 1))  # from (H,W,C) to (C,H,W)
            print(img.shape)
            dir, filename = os.path.split(os.path.join(save_folder, line))
            if not os.path.isdir(dir):
                os.makedirs(dir)

            img.astype("float32").tofile(os.path.join(save_folder, line[:-3]+"bin"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path_list')
    parser.add_argument('img_root')
    parser.add_argument('width', type=int)
    parser.add_argument('height', type=int)
    parser.add_argument('save_folder')
    args = parser.parse_args()

    preprocess(args.path_list, args.img_root, args.width, args.height, args.save_folder)