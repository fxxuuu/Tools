import os
import pprint
import pymongo
import sys
import boto3

session = boto3.session.Session()
s3 = session.client(endpoint_url='http://s3.momenta.works', aws_access_key_id='ZXIBS6QZ6J4VA0FBDNCS',
                    aws_secret_access_key='F4iCPNSGGCV7AglUc7s5TsSgns1hjZ9LAOKPoFBr', service_name='s3')

with open('/home/fangxin/Fisheye/cur_img.md5', 'r') as fp:
# with open('/home/fangxin/Fisheye/tobetransfered.md5', 'r') as fp:
    md5_lines = [l.strip() for l in fp.readlines()]
with open('/home/fangxin/Fisheye/cur_img.list', 'r') as fp:
# with open('/home/fangxin/Fisheye/tobetransfered.list', 'r') as fp:
    path_lines = [l.strip() for l in fp.readlines()]

with open('/home/fangxin/Fisheye/test_annotations/5613_Fisheye_test.md5', 'r') as fp:
    test_md5_lines = [l.strip() for l in fp.readlines()]


assert len(md5_lines) == len(path_lines)

cnt = 0
all_cnt = 0
skip_cnt = 0
for idx in range(len(md5_lines)):
    all_cnt += 1
    # print all_cnt
    md5_str = md5_lines[idx]

    if md5_str in test_md5_lines:
        skip_cnt += 1
        continue

    origin_path = path_lines[idx]
    target_file = os.path.join('/home/fangxin/Fisheye/cpu_decode_train/', origin_path)
    if not os.path.isdir(os.path.dirname(target_file)):
        os.makedirs(os.path.dirname(target_file))
    if not os.path.isfile(target_file):
    # if True:
        try:
            s3.download_file('momenta-images', md5_str, target_file)
            cnt += 1
            # print cnt
        except Exception, e:
            print e
    sys.stdout.write('\rall_cnt={}, done_cnt={}, skip_test={}'.format(all_cnt, cnt, skip_cnt))
    sys.stdout.flush()
