import numpy as np
# import seaborn as sns
import matplotlib
import json
matplotlib.use('agg')
import matplotlib.pyplot as plt
# import matplotlib.pyplot as plt
import pymongo,sys

def draw_bar(label, data, pic_name):
    plt.subplots(figsize=(10, 6))
    x_pos = np.arange(len(label))
    plt.bar(x_pos, data, align='center', alpha=1, facecolor='lightskyblue', edgecolor='white')
    plt.xticks(x_pos, label)
    plt.xlabel('height pixel')
    plt.ylabel('num')
    plt.savefig(pic_name)

gt_scale_map = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
gt_ignore_scale_map = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
scale_label = ['0-100','100-200','200-300','300-400','400-500','500-600','600-700','700-800','800-900','900-1000','1000+']
gt_box_count = 0
gt_ignore_box_count = 0
invalid_gt_box_count = 0


with open('/home/fangxin/Fisheye/train_annotations/fisheye_124529.data', 'r') as fp:
    data = {'data': []}
    lines = fp.readlines()
    length = len(lines)
    print length
    for idx, line in enumerate(lines):
        sys.stdout.write('\r%d' % (idx + 1))
        sys.stdout.flush()
        tmp = json.loads(line.rstrip('\n'))
        # print tmp
        if idx > 0: # The first line is the img_prefix
            data['data'].append(tmp)
    # print data

for idx, idata in enumerate(data['data']):
    sys.stdout.write('\r%d / %d, invalid_gt_boxes: %d' % (idx+1, length, invalid_gt_box_count))
    sys.stdout.flush()
    gt_boxes = idata['labels']['gt_boxes']
    gt_ignore_boxes = idata['labels']['gt_ignore_boxes']

    for gt_box in gt_boxes:
        x1, y1, x2, y2 = gt_box
        rect_height = min(int((y2-y1)/100), 10)
        gt_scale_map[rect_height] += 1
        gt_box_count += 1

    for gt_ignore_box in gt_ignore_boxes:
        x1, y1, x2, y2 = gt_ignore_box
        rect_height = min(int(y2-y1)/100, 10)
        gt_ignore_scale_map[rect_height] += 1
        gt_ignore_box_count += 1

draw_bar(scale_label, gt_scale_map, '/home/fangxin/Fisheye/train_annotations/mvp_12w_gt_data_distribution.png')
print "\n", gt_scale_map
draw_bar(scale_label, gt_ignore_scale_map, '/home/fangxin/Fisheye/train_annotations/mvp_12w_gt_ignore_distribution.png')
print('\n%d, %d' % (gt_box_count, gt_ignore_box_count))
