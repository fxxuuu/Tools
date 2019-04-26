import sys,os
from sklearn.cluster import KMeans
from sklearn.externals import joblib
import numpy
import math
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

ratio_num = 5
scale_num = 10
human_ratio_num = 3
ofo_ratio_num = 4
car_ratio_num = 4
human_scale_num = 5
ofo_scale_num = 5
car_scale_num = 5

def read_labels(labels_path):
    with open(labels_path,'r') as f_in:
        labels_dic = json.load(f_in)
    print("load json file")
    images = labels_dic['images']
    anns = labels_dic['annotations']
    cluster_dic = {}
    for image in images :
       img_id = image['id']
       cluster_dic[img_id] = {}
       cluster_dic[img_id]['width'] = image['width']
       cluster_dic[img_id]['height'] = image['height']
    print("load image info")
    anchor_scales = []
    anchor_ratios = []
    human_anchor_ratios = []
    human_anchor_ratios_plot = []
    human_anchor_scales = []
    human_anchor_scales_plot = []
    ofo_anchor_ratios = []
    ofo_anchor_ratios_plot = []
    ofo_anchor_scales = []
    ofo_anchor_scales_plot = []
    car_anchor_ratios = []
    car_anchor_ratios_plot = []
    car_anchor_scales = []
    car_anchor_scales_plot = []
    anchor_ratios_plot = []
    anchor_scales_plot = []
    discard_ratio_cnt = 0
    for idx,ann in enumerate(anns):
        if not cluster_dic.has_key(ann['image_id']) :
            print("id not exist")
            print ann['image_id']
            continue
        scale = []
        ratio = []
        human_ratio = []
        human_scale = []
        ofo_ratio = []
        ofo_scale = []
        car_ratio = []
        car_scale = []
        x0 = ann['bbox'][0]
        y0 = ann['bbox'][1]
        x1 = x0 + ann['bbox'][2]
        y1 = y0 + ann['bbox'][3]
        #w = ann['bbox'][2]
        #h = ann['bbox'][3]
        img_w = cluster_dic[ann['image_id']]['width']
        img_h = cluster_dic[ann['image_id']]['height']
        h_ratio = float(img_h)/float(448)
        if h_ratio == 0 :print cluster_dic[ann['image_id']]
        #cut edge
        if x0 < 0 : x0 = 0
        if y0 < 0 : y0 = 0
        if x1 > img_w : x1 = img_w
        if y1 > img_h : y1 = img_h
        w = float(x1 - x0)
        h = float(y1 - y0)
        if h/w <= 5.0:
            anchor_ratios_plot.append(h/w)
            ratio.append(h/w)
            anchor_ratios.append(ratio)
            if ann['category_id'] == 1 :
                human_anchor_ratios_plot.append(h/w)
                if h/w >= 2.00 :
                    human_ratio.append(h/w)
                    human_anchor_ratios.append(human_ratio)
            if ann['category_id'] == 2 :
                ofo_anchor_ratios_plot.append(h/w)
                if h/w >= 1.00 and h/w <= 2.00 :
                    ofo_ratio.append(h/w)
                    ofo_anchor_ratios.append(ofo_ratio)
            if ann['category_id'] == 3 :
                car_anchor_ratios_plot.append(h/w)
                if h/w <= 1.00 :
                    car_ratio.append(h/w)
                    car_anchor_ratios.append(car_ratio)
        else :
            discard_ratio_cnt += 1
        area = math.sqrt(w*h)
        anchor_scales_plot.append(area/h_ratio)
        scale.append(area/h_ratio)
        anchor_scales.append(scale)
        if ann['category_id'] == 1 :
            human_anchor_scales_plot.append(area/h_ratio)
            human_scale.append(area/h_ratio)
            human_anchor_scales.append(human_scale)
        if ann['category_id'] == 2 :
            ofo_anchor_scales_plot.append(area/h_ratio)
            ofo_scale.append(area/h_ratio)
            ofo_anchor_scales.append(ofo_scale)
        if ann['category_id'] == 3 :
            car_anchor_scales_plot.append(area/h_ratio)
            car_scale.append(area/h_ratio)
            car_anchor_scales.append(car_scale)
    #print discard_ratio_cnt
    print len(anns)
    print len(human_anchor_scales)
    print len(ofo_anchor_scales)
    print len(car_anchor_scales)
    print len(car_anchor_ratios) + len(ofo_anchor_ratios) + len(human_anchor_ratios)
    print("calc ratios&scales")
    return human_anchor_ratios, human_anchor_scales, ofo_anchor_ratios, ofo_anchor_scales, car_anchor_ratios, car_anchor_scales, human_anchor_ratios_plot,human_anchor_scales_plot, ofo_anchor_ratios_plot,ofo_anchor_scales_plot, car_anchor_ratios_plot,car_anchor_scales_plot, anchor_ratios_plot, anchor_scales_plot, anchor_ratios, anchor_scales

def cluster(anchor_ratios, anchor_scales, para_k_ratio = 10, para_k_scale = 10):
    clf_ratio = KMeans(n_clusters=para_k_ratio)
    ratio_res = clf_ratio.fit(anchor_ratios)
    clf_scale = KMeans(n_clusters=para_k_scale)
    scale_res = clf_scale.fit(anchor_scales)
    return ratio_res.cluster_centers_, scale_res.cluster_centers_

def plt_things(anchor_ratios_plot, anchor_scales_plot, plt_name = "") :
    y_ratios = range(len(anchor_ratios_plot))
    y_scales = range(len(anchor_scales_plot))
    anchor_ratios_plot.sort()
    anchor_scales_plot.sort()

    plt.figure(plt_name)
    sns.set(rc={"figure.figsize": (8, 4)})
    ax = sns.distplot(anchor_ratios_plot)
    plt.show()

if __name__ == "__main__":
    labels_path = "/home/fangxin/fxx_waist_workspace/dataset/upground/with_ignore/original_from_db/waist_4_upground_148w_1486895_updated.json"
    human_anchor_ratios, human_anchor_scales, ofo_anchor_ratios, ofo_anchor_scales, car_anchor_ratios, car_anchor_scales, human_anchor_ratios_plot,human_anchor_scales_plot, ofo_anchor_ratios_plot,ofo_anchor_scales_plot, car_anchor_ratios_plot,car_anchor_scales_plot, anchor_ratios_plot,anchor_scales_plot, anchor_ratios, anchor_scales = read_labels(labels_path)
    #human_ratio_res,human_scale_res = cluster(human_anchor_ratios, human_anchor_scales, human_ratio_num, human_scale_num)
    #ofo_ratio_res,ofo_scale_res = cluster(ofo_anchor_ratios, ofo_anchor_scales, ofo_ratio_num, ofo_scale_num)
    #car_ratio_res,car_scale_res = cluster(car_anchor_ratios, car_anchor_scales, car_ratio_num, car_scale_num)
    ratio_res,scale_res = cluster(anchor_ratios, anchor_scales, ratio_num, scale_num)
    #plt_things(human_anchor_ratios_plot,human_anchor_scales_plot, "human")
    #plt_things(ofo_anchor_ratios_plot,ofo_anchor_scales_plot, "ofo")
    #plt_things(car_anchor_ratios_plot,car_anchor_scales_plot, "car")
    #plt_things(anchor_ratios_plot, anchor_scales_plot, "all")
    print ratio_res
    print scale_res
    """
    human_ratio_res_sorted = []
    ofo_ratio_res_sorted = []
    car_ratio_res_sorted = []
    human_scale_res_sorted = []
    ofo_scale_res_sorted = []
    car_scale_res_sorted = []
    for ratio in human_ratio_res:
        ratio_res = ratio[0]
        human_ratio_res_sorted.append(ratio_res)
    for scale in human_scale_res:
        scale_res = scale[0]
        human_scale_res_sorted.append(scale_res)
    for ratio in ofo_ratio_res:
        ratio_res = ratio[0]
        ofo_ratio_res_sorted.append(ratio_res)
    for scale in ofo_scale_res:
        scale_res = scale[0]
        ofo_scale_res_sorted.append(scale_res)
    for ratio in car_ratio_res:
        ratio_res = ratio[0]
        car_ratio_res_sorted.append(ratio_res)
    for scale in car_scale_res:
        scale_res = scale[0]
        car_scale_res_sorted.append(scale_res)
    #print(ratio_res)
    #print(scale_res)
    print("---------human ratio-------------")
    print(human_ratio_res)
    print("---------human scale-------------")
    print(human_scale_res)
    print("#################################")
    print("---------ofo ratio-------------")
    print(ofo_ratio_res)
    print("---------ofo scale-------------")
    print(ofo_scale_res)
    print("#################################")
    print("---------car ratio-------------")
    print(car_ratio_res)
    print("---------car scale-------------")
    print(car_scale_res)
    print("#################################")
    print "human_ratio:"
    human_ratio_res_sorted.sort()
    print human_ratio_res_sorted
    print "ofo_ratio:"
    ofo_ratio_res_sorted.sort()
    print ofo_ratio_res_sorted
    print "car_ratio:"
    car_ratio_res_sorted.sort()
    print car_ratio_res_sorted
    print("#################################")
    print "human_scale:"
    human_scale_res_sorted.sort()
    print human_scale_res_sorted
    print "ofo_scale:"
    ofo_scale_res_sorted.sort()
    print ofo_scale_res_sorted
    print "car_scale:"
    car_scale_res_sorted.sort()
    print car_scale_res_sorted
    """




