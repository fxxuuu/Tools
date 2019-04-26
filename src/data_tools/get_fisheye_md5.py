import os
import pprint
import pymongo
import sys
import boto3

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
collection = db['human_box_h3_upground_v5']

print "here"

# with open('/home/fangxin/Fisheye/test_annotations/19916_Fisheye_test.md5', 'r') as fp:
#     testset_md5 = [l.strip() for l in fp.readlines()]
#
# with open('/home/fangxin/Fisheye/img_320684.md5', 'r') as fp:
#     cur_md5 = [l.strip() for l in fp.readlines()]

print "read over"

# Get md5 && Download

cnt = 0
demos = collection.find({},no_cursor_timeout = True).batch_size(1)
fp = open('/home/fangxin/h3_workspace/cur_img.md5', 'w')
fp2 = open('/home/fangxin/h3_workspace/cur_img.list', 'w')

try:
    for item in demos:
        if item.get('result') is not None:
            if cnt % 100 == 0:
                sys.stdout.write('\rcnt={}'.format(cnt))
                sys.stdout.flush()

            md5_str = item.get('md5')
            origin_path = item.get('origin_path')
            # if md5_str in testset_md5:
            #     all_cnt += 1
            #     continue
            # if md5_str in cur_md5:
            #     all_cnt += 1
            #     continue
            cnt += 1
            fp.write(md5_str + '\n')
            fp.flush()
            fp2.write(origin_path + '\n')
            fp2.flush()
except Exception, e:
    print e




