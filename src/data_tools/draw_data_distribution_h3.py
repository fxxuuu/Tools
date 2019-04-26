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
# scale_label = ['0-100','100-200','200-300','300-400','400-500','500-600','600-700','700-800','800-900','900-1000','1000+']
# scale_label = ['0-26','26-52','52-78','78-104','104-130','130-156','156-182','182-208','208-234','234-260','260+']
scale_label = ['0-50','50-100','100-150','150-200','200-250','250-300','300-350','350-400','400-450','450-500','500+']
gt_box_count = 0
gt_ignore_box_count = 0
invalid_gt_box_count = 0


with open('/home/fangxin/h3_workspace/train_annotations/total_709081/h3_fov180_70w.data', 'r') as fp:
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
        rect_height = min(int((y2-y1)/50), 10)
        gt_scale_map[rect_height] += 1
        gt_box_count += 1

    for gt_ignore_box in gt_ignore_boxes:
        x1, y1, x2, y2 = gt_ignore_box
        rect_height = min(int(y2-y1)/50, 10)
        gt_ignore_scale_map[rect_height] += 1
        gt_ignore_box_count += 1


sum = sum(gt_scale_map)
print "\nsum =", sum
for i in range(len(gt_scale_map)):
    percent = float(float(gt_scale_map[i]) / sum)
    print percent
    scale_label[i] += "\n" + str('%.2f%%' % (float(percent) * 100))

draw_bar(scale_label, gt_scale_map, '/home/fangxin/h3.png')
print "\n", gt_scale_map
# draw_bar(scale_label, gt_ignore_scale_map, '/home/fangxin/Fisheye/train_annotations/mvp_12w_gt_ignore_distribution.png')
print('\n%d, %d' % (gt_box_count, gt_ignore_box_count))
