import pymongo
import argparse
import numpy as np
import cStringIO as StringIO
import cv2
import os,sys
import hashlib
green = (0, 255, 0)
blue = (255, 0, 0)
red = (0, 0, 255)
def draw_box(im_data, pre_bbox, _color):

    # draw bbox
    if _color == "red":
        cv2.rectangle(img=im_data, pt1=(int(pre_bbox[0]), int(pre_bbox[1])), pt2=(int(pre_bbox[2]), int(pre_bbox[3])),
                      color=red, thickness=2)
    elif _color == "blue":
        cv2.rectangle(img=im_data, pt1=(int(pre_bbox[0]), int(pre_bbox[1])), pt2=(int(pre_bbox[2]), int(pre_bbox[3])),
                      color=blue, thickness=2)
    elif _color == "green":
        cv2.rectangle(img=im_data, pt1=(int(pre_bbox[0]), int(pre_bbox[1])), pt2=(int(pre_bbox[2]), int(pre_bbox[3])),
                      color=green, thickness=2)


    return im_data


wd_folder = '/share10/public/fangxin/mvp_data/for_check/final_data/neg/'
human_folder = '/share10/public/fangxin/mvp_data/for_check/final_data/true_human'
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

def get_momenta_db():
    SETTINGS = {
        'host': 'mumbai.momenta.works:8025',
        'database': 'dora',
        'username': 'research',
        'password': 'vrl1r0oLbsKht262eybX',
        'options': 'ssl=false'
    }
    try:
        conn = pymongo.MongoClient(
            "mongodb://{username}:{password}@{host}/{database}?{options}".format(**SETTINGS))
    except Exception as ex:
        print("Error:", ex)
        exit('Failed to connect, terminating.')
    db = conn.dora
    return db

db_hdl = get_momenta_db()
# ds = db_hdl['human_box_testset'].find()
ds = db_hdl['human_wrong_detection_mvp'].find(no_cursor_timeout=True)
f_out = open('/share10/public/fangxin/mvp_data/for_check/final_data/0730_neg.md5','w')
wrong_detec = 0
human_count = 0
for idx,i in enumerate(ds):
    sys.stdout.write('\rgetdb: %d/%d' % (idx, ds.count()))
    sys.stdout.flush()

    path = i['origin_path']

    try:
        if 'result' in i:
            if 'Rects' in i['result'][0]['raw']:
                in_img = cv2.imread('/share10/public/momenta_train_images/'+path)
                for idx,rect in enumerate(i['result'][0]['raw']['Rects']):
                    bbox = [rect['x'],rect['y'],rect['x']+rect['w'],rect['y']+rect['h']]
                    trans_width = bbox[2] - bbox[0]
                    trans_height = bbox[3] - bbox[1]
                    dst = np.float32([119, 305])
                    trans_rate = min((dst[1] - dst[0]) / trans_width, (dst[1] - dst[0]) / trans_height)
                    M = np.float32(
                        [[trans_rate, 0, (dst[1] + dst[0]) / 2 - trans_rate * (bbox[2] + bbox[0]) / 2],
                         [0, trans_rate, (dst[1] + dst[0]) / 2 - trans_rate * (bbox[3] + bbox[1]) / 2]])
                    patch = cv2.warpAffine(in_img, M, (424, 424))
                    x1 = bbox[0]*M[0][0] +M[0][2]
                    x2 = bbox[2] * M[0][0] + M[0][2]
                    y1 = bbox[1]*M[1][1] + M[1][2]
                    y2 = bbox[3] * M[1][1] + M[1][2]


                    if rect['properties']['detection_type'][0] == 'wrong_detection':
                        patch = draw_box(patch, [x1, y1, x2, y2],"red")
                        ori_path = path.replace('/','%').replace('.','_%d.'%(idx))
                        save_path = os.path.join(wd_folder,
                                             ori_path)

                        # cv2.imwrite(save_path, patch)
                        wrong_detec += 1

                        with open(os.path.join('/share10/public/momenta_train_images/', path.strip()), 'r') as fd:
                            fcont = fd.read()
                            fmd5 = hashlib.md5(fcont).hexdigest().strip()


                        f_out.write(fmd5 + '\n')

                    elif rect['properties']['detection_type'][0] == "is_human":
                        patch = draw_box(patch, [x1, y1, x2, y2],"green")
                        ori_path = path.replace('/','%').replace('.','_%d.'%(idx))
                        save_path = os.path.join(human_folder,
                                             ori_path)

                        # cv2.imwrite(save_path, patch)
                        human_count += 1


        else:
            print('\tno results')
    except Exception as e:
        print(e)
print('wrong_detection:%d\n'%(wrong_detec))
print('human:%d'%(human_count))

f_out.close()


