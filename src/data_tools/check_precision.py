import os, sys, argparse
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file1', help="x86")
    parser.add_argument('file2', help="h3")
    args = parser.parse_args()

    lines_1 = [l.strip() for l in open(args.file1).readlines()]
    lines_2 = [l.strip() for l in open(args.file2).readlines()]

    len1 = len(lines_1)
    len2 = len(lines_2)
    assert (len1 == len2)

    score_ab_error = []
    x1_ab_error = []
    y1_ab_error = []
    x2_ab_error = []
    y2_ab_error = []

    score_re_error = []
    x1_re_error = []
    y1_re_error = []
    x2_re_error = []
    y2_re_error = []

    max_score_error = 0
    max_x1_error = 0
    max_y1_error = 0
    max_x2_error = 0
    max_y2_error = 0

    for i in range(0, len1, 4):
        # print lines_1[i], lines_2[i]
        # print lines_1[i+1], lines_2[i+1]
        # print lines_1[i+2], lines_2[i+2]

        score1 = float(lines_1[i + 1].strip())
        score2 = float(lines_2[i + 1].strip())
        score_ab_error.append(abs(score1 - score2))
        if abs(score1 - score2) > max_score_error:
            max_score_error = abs(score1 - score2)
        score_re_error.append(abs(score1 - score2) / score1)

        bboxs1 = list(map(float, lines_1[i + 2].split()))
        bboxs2 = list(map(float, lines_2[i + 2].split()))
        x1_ab_error.append(abs(bboxs1[0] - bboxs2[0]))
        if abs(bboxs1[0] - bboxs2[0]) > max_x1_error:
            max_x1_error = abs(bboxs1[0] - bboxs2[0])
        x1_re_error.append(abs(bboxs1[0] - bboxs2[0]) / bboxs1[0])

        y1_ab_error.append(abs(bboxs1[1] - bboxs2[1]))
        if abs(bboxs1[1] - bboxs2[1]) > max_y1_error:
            max_y1_error = abs(bboxs1[1] - bboxs2[1])
        y1_re_error.append(abs(bboxs1[1] - bboxs2[1]) / bboxs1[1])

        x2_ab_error.append(abs(bboxs1[2] - bboxs2[2]))
        if abs(bboxs1[2] - bboxs2[2]) > max_x2_error:
            max_x2_error = abs(bboxs1[2] - bboxs2[2])
        x2_re_error.append(abs(bboxs1[2] - bboxs2[2]) / bboxs1[2])

        y2_ab_error.append(abs(bboxs1[3] - bboxs2[3]))
        if abs(bboxs1[3] - bboxs2[3]) > max_y2_error:
            max_y2_error = abs(bboxs1[3] - bboxs2[3])
        y2_re_error.append(abs(bboxs1[3] - bboxs2[3]) / bboxs1[3])

    score_re_error = np.array(score_re_error, dtype=np.float32)
    x1_re_error = np.array(x1_re_error, dtype=np.float32)
    y1_re_error = np.array(y1_re_error, dtype=np.float32)
    x2_re_error = np.array(x2_re_error, dtype=np.float32)
    y2_re_error = np.array(y2_re_error, dtype=np.float32)

    score_ab_error = np.array(score_ab_error, dtype=np.float32)
    x1_ab_error = np.array(x1_ab_error, dtype=np.float32)
    y1_ab_error = np.array(y1_ab_error, dtype=np.float32)
    x2_ab_error = np.array(x2_ab_error, dtype=np.float32)
    y2_ab_error = np.array(y2_ab_error, dtype=np.float32)

    ave_score_error = np.mean(score_re_error)
    ave_x1_error = np.mean(x1_re_error)
    ave_y1_error = np.mean(y1_re_error)
    ave_x2_error = np.mean(x2_re_error)
    ave_y2_error = np.mean(y2_re_error)

    ave_score_error_ab = np.mean(score_ab_error)
    ave_x1_error_ab = np.mean(x1_ab_error)
    ave_y1_error_ab = np.mean(y1_ab_error)
    ave_x2_error_ab = np.mean(x2_ab_error)
    ave_y2_error_ab = np.mean(y2_ab_error)

    print "max absolute score error:", max_score_error
    print "max absolute x1 error:", max_x1_error
    print "max absolute y1 error:", max_y1_error
    print "max absolute x2 error:", max_x2_error
    print "max absolute y2 error:", max_y2_error

    print ""

    print "average relative score error:", ave_score_error
    print "average relative x1 error:", ave_x1_error
    print "average relative y1 error:", ave_y1_error
    print "average relative x2 error:", ave_x2_error
    print "average relative y2 error:", ave_y2_error

    print ""

    print "average absolute score error:", ave_score_error_ab
    print "average absolute x1 error:", ave_x1_error_ab
    print "average absolute y1 error:", ave_y1_error_ab
    print "average absolute x2 error:", ave_x2_error_ab
    print "average absolute y2 error:", ave_y2_error_ab













