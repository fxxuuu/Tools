import os
import pprint
import pymongo
import boto3
import sys
import os
session = boto3.session.Session()
s3 = session.client(endpoint_url='http://s3.momenta.works', aws_access_key_id='ZXIBS6QZ6J4VA0FBDNCS',
                    aws_secret_access_key='F4iCPNSGGCV7AglUc7s5TsSgns1hjZ9LAOKPoFBr', service_name='s3')


def get_db():
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
        print ("Error:", ex)
        exit('Failed to connect, terminating.')
    return conn.dora


db = get_db()
# collection = db['human_box_trainset_fisheye_v3']
collection = db['human_box_h3_special_v5']

# path_list = []
# with open('/home/fangxin/Fisheye/img.list','r')as f:
with open('/home/fangxin/h3_workspace/special_img.list','r')as f:
# with open('/home/fangxin/Fisheye/test_annotations/testset_0830_2w.list', 'r') as f:
    path_list = f.readlines()
    path_list = [x.strip() for x in path_list]

valid_path_list = []
print(len(path_list))
# Get md5 && Download
md5_list = []
cnt = 0
hardscene = 0
for list_item in path_list:
    if collection.find_one({'origin_path':list_item}) is not None:
        new_doc = collection.find_one({'origin_path': list_item})
        if new_doc.get('result') is not None:
            result = new_doc.get('result')
            Hardscene = result[-1]['raw']['Hardscene']
            if Hardscene == False:
                md5_str = new_doc.get('md5')
                md5_list.append(md5_str)
                valid_path_list.append(list_item)
            else:
                hardscene += 1
            # here target_file
            # target_file = '/share10/public/fangxin/Fisheye/' + item.get('origin_path')
            # if not os.path.isdir(os.path.dirname(target_file)):
            #     os.makedirs(os.path.dirname(target_file))
            # if not os.path.isfile(target_file):
            #     try:
            #         s3.download_file('momenta-images', md5_str, target_file)
            #         cnt += 1
            #         sys.stdout.write('\r{}'.format(cnt))
            #         sys.stdout.flush()
            #     except Exception as e:
            #         print(e)
print "hardscene: ", hardscene

# Save Folder
save_folder = '/home/fangxin/h3_workspace/train_annotations'
if not os.path.exists(save_folder):
    os.makedirs(save_folder)
total_cnt = len(md5_list)

wh_fw = open(save_folder + '/' + str(total_cnt) + '_special_Fisheye_.wh', 'w')
hf_fw = open(save_folder + '/' + str(total_cnt) + '_special_Fisheye_.hf', 'w')
path_fw = open(save_folder + '/' + str(total_cnt) + '_special_Fisheye_.list', 'w')

for item in valid_path_list:
    path_fw.write(item + '\n')
path_fw.close()

batch_size = total_cnt / 100
wh_cnt = 0
hf_cnt = 0
path_cnt = 0

for md5 in md5_list:
    document = collection.find_one({'md5': md5})
    # wh
    wh_cnt += 1
    wh = document.get('size')
    wh_fw.write(str(wh['width']) + ' ' + str(wh['height']) + "\n")
    # hf
    hf_cnt += 1
    if (document.get('result')):
        raw = document.get('result')[-1].get('raw')
        Rects = raw.get('Rects')
        # pprint.pprint(Rects)
        if (Rects):
            hf_fw.write(str(len(Rects)))
            for rect in Rects:
                x1 = rect.get('x')
                y1 = rect.get('y')
                x2 = rect.get('w') + x1
                y2 = rect.get('h') + y1
                score = rect.get('v')
                hf_fw.write(
                    " {} {} {} {} {}".format(x1, y1, x2, y2, score))  # write to the human_format file
            hf_fw.write('\n')
        else:
            hf_fw.write("0\n")
    # path
        path_cnt += 1
    # path = document.get('origin_path')
    # path_fw.write(path + "\n")

    if path_cnt % batch_size == 0:
        print('---{}%---'.format(path_cnt / batch_size))

