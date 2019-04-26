import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pymongo,sys


def get_human_db(db_name):  #readonly
    SETTINGS = {
        'host': '172.16.10.200:8888',
        'username': 'human',
        'password': 'human',
    }
    try:
        conn = pymongo.MongoClient(
            "mongodb://{username}:{password}@{host}".format(**SETTINGS))
    except Exception as ex:
        print("Error:", ex)
        exit('Failed to connect, terminating.')
    db = conn[db_name]
    return db

db_hdl=get_human_db('train')
ds = db_hdl['human_mpilot'].find(no_cursor_timeout=True)
dt_map = np.zeros([130,230])
scale_map = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
scale_label = ['0-100','100-200','200-300','300-400','400-500','500-600','600-700','700-800','800-900','900-1000','1000+']
box_count = 0

for idx, idata in enumerate(ds):
    sys.stdout.write('\rgetdb: %d/%d' % (idx, 2000000))
    sys.stdout.flush()
    try:
        if 'size' in idata:
            if idata['size']['height'] > 0 and idata['size']['width'] > 0:
                if 'result' in idata:
                    if 'Rects' in idata['result']['raw']:
                        rects = idata['result']['raw']['Rects']
                        for index, rect in enumerate(rects):
                            center_point_x = rect['x'] + rect['w'] / 2
                            center_point_y = rect['y'] + rect['h'] / 2
                            trans_x = center_point_x * 230 / idata['size']['width']
                            trans_y = center_point_y * 130 / idata['size']['height']
                            trans_x = min(trans_x, 229)
                            trans_x = max(trans_x,0)
                            trans_y = min(trans_y, 129)
                            trans_y = max(trans_y, 0)
                            dt_map[int(trans_y)][int(trans_x)] += 1
                            rect_height = min(int(rect['h']/100), 10)
                            scale_map[rect_height] += 1
                            box_count += 1

    except Exception as e:
        print(e)


def draw_bar(label,data):
    plt.subplots(figsize=(10, 6))
    x_pos = np.arange(len(label))
    plt.bar(x_pos, data, align='center', alpha=1, facecolor='lightskyblue',edgecolor='white')
    plt.xticks(x_pos, label)
    plt.xlabel("height pixel")
    plt.ylabel("num")
    plt.savefig('rect_count.png')


def draw_heatmap(data):
    sns.set()
    plt.subplots(figsize=(23, 13))
    sns.heatmap(data)
    plt.savefig('data_distibution.png')


draw_heatmap(dt_map)
draw_bar(scale_label,scale_map)
print('\n%d'%box_count)
