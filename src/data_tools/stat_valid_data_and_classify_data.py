import os, sys, argparse


def stat_valid_data(hf_file, up_idx, under_idx):

    hf_lines, hf_up_lines, hf_under_lines = [], [], []

    with open(hf_file, 'r') as fp:
        lines = fp.readlines()
        size = len(lines)
        for i in range(size):
            hf = lines[i]
            hf_lines.append(hf)
            if i in up_idx:
                hf_up_lines.append(hf)
            elif i in under_idx:
                hf_under_lines.append(hf)

    valid_img_num = 0
    print ""
    print len(hf_lines)
    for hf_line in hf_lines:
        if hf_line[0] == '0':
            valid_img_num += 1

    up_valid_img_num = 0
    print len(hf_up_lines)
    for hf_line in hf_up_lines:
        if hf_line[0] == '0':
            up_valid_img_num += 1

    under_valid_img_num = 0
    print len(hf_under_lines)
    for hf_line in hf_under_lines:
        if hf_line[0] == '0':
            under_valid_img_num += 1

    return valid_img_num, up_valid_img_num, under_valid_img_num

def stat_class(path_list):
    with open(path_list, 'r') as fp:
        path_lines = [l.strip() for l in fp.readlines()]
    length = len(path_lines)
    up_cnt, under_cnt, total_cnt = 0, 0, 0
    up_idx, under_idx = [], []
    for idx, path in enumerate(path_lines):
        total_cnt += 1
        sys.stdout.write('\r{}/{}'.format(total_cnt, length))
        sys.stdout.flush()
        if 'underground' in path:
            under_cnt += 1
            under_idx.append(idx)
        else:
            up_cnt += 1
            up_idx.append(idx)
        # if 'upground' in path:
            # up_cnt += 1
            # up_idx.append(idx)
        # elif 'underground' in path:
            # under_cnt += 1
            # under_idx.append(idx)
        # else:
            # print "error!"
    return up_cnt, under_cnt, up_idx, under_idx




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path_list')
    parser.add_argument('hf_file')
    args = parser.parse_args()

    path_list, hf_file = args.path_list, args.hf_file

    up_cnt, under_cnt, up_idx, under_idx = stat_class(path_list)
    valid_img_num, up_num, under_num = stat_valid_data(hf_file, up_idx, under_idx)

    print ""
    print "valid_img_num =", valid_img_num
    print "upground {}/{}".format(up_num, up_cnt)
    print "underground {}/{}".format(under_num, under_cnt)

