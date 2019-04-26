import time
import os
import argparse
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('hf_path')
    parser.add_argument('path_list')
    parser.add_argument('save_folder')
    parser.add_argument('prefix_name')
    parser.add_argument('-mh', dest='min_h_thres', type=int, default=40)
    parser.add_argument('-min', dest='min_score_thres', type=float, default=0.0)
    parser.add_argument('-max', dest='max_score_thres', type=float, default=1.0)
    args = parser.parse_args()

    hf_lines = [l.strip() for l in open(args.hf_path).readlines()]
    path_lines = [l.strip() for l in open(args.path_list).readlines()]

    idx_list = []
    cnt = 0
    end = False

    for i in range(len(hf_lines)):
        # if end:
            # break
        hf_line = hf_lines[i]
        path = path_lines[i]

        hf_line = hf_line.split()
        bbox_num = int(hf_line[0])
        bbox_info = list(map(float, hf_line[1:]))
        scores = []
        boxes = []
        for ii in range(bbox_num):
            scores.append(bbox_info[5 * ii + 4])
            boxes.append(bbox_info[5 * ii: 5 * ii + 4])
        flg = False
        for j, box in enumerate(boxes):

            if box[3] - box[1] >= args.min_h_thres and scores[j] > args.min_score_thres and scores[j] < args.max_score_thres:
                flg = True
                print box, scores[j]
                print box[3] - box[1]
                sys.stdout.write('\r{}'.format(cnt+1))
                sys.stdout.flush()
                cnt += 1
                idx_list.append(i)
                sys

                # if cnt >= args.number:
                    # end = True
                # print cnt, args.number, flg, end

                if flg == True:
                    break

    print "\ntotal_length =", len(hf_lines)
    print "valid_num =", cnt

    if not os.path.isdir(args.save_folder):
        os.makedirs(args.save_folder)
    with open(os.path.join(args.save_folder, args.prefix_name+"_"+str(len(idx_list))+".hf"), 'w') as fp1:
            with open(os.path.join(args.save_folder, args.prefix_name + "_" + str(len(idx_list)) + ".list"), 'w') as fp3:
                for idx in idx_list:
                    fp1.write(hf_lines[idx] + '\n')
                    fp3.write(path_lines[idx] + '\n')



