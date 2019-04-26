import argparse
import os
from PIL import Image

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('path_list')
    parser.add_argument('image_root')
    args = parser.parse_args()
    path, image_root = args.path_list, args.image_root

    path_list = [l.rstrip('\n') for l in open(path).readlines()]

    total_num = len(path_list)
    print total_num
    batch_size = total_num / 100
    missing_count = 0
    missing_pics = []

    f_wh = open("img.wh", "w")

    for idx, item in enumerate(path_list):
        file_name = os.path.join(image_root, item)
        # print file_name
        if not os.path.isfile(file_name):
            missing_count += 1
            missing_pics.append(item)
        else:
            try:
                im = Image.open(file_name)
                width, height = im.size
                f_wh.write(str(width) + " " + str(height) + "\n")
                #print "not missing !!!", file_name
            except Exception, e:
                print e, file_name
                missing_count += 1
                missing_pics.append(item)

        if idx % batch_size == 1:
            print('{}% processed, missing count : {}'.format(idx / batch_size, missing_count))
    f = open('missing.path', 'w')
    for item in missing_pics:
        f.write(item + '\n')
    f_wh.close()

