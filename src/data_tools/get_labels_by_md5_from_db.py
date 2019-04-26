import argparse
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

def get_labels_by_md5(md5_list_file, save_folder):
    db = get_db()
    collection = db['human_box_h3_upground_v5']

    with open(md5_list_file, 'r') as fp:
        md5_lines = [l.strip() for l in fp.readlines()]
    total_cnt = len(md5_lines)

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    wh_fw = open(save_folder + '/' + str(total_cnt) + '_minibatch_h3_.wh', 'w')
    hf_fw = open(save_folder + '/' + str(total_cnt) + '_minibatch_h3_.hf', 'w')

    for idx, md5 in enumerate(md5_lines):
        sys.stdout.write('\r[%d/%d]' % (idx, total_cnt))
        sys.stdout.flush()
        if collection.find_one({'md5': md5}) is not None:
            new_doc = collection.find_one({'md5': md5})
            wh = new_doc.get('size')
            wh_fw.write(str(wh['width']) + ' ' + str(wh['height']) + "\n")
            if new_doc.get('result') is not None:
                result = new_doc.get('result')
                raw = result[-1].get('raw')
                Rects = raw.get('Rects')
                if(Rects):
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
                    hf_fw.write('0\n')
    wh_fw.close()
    hf_fw.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('md5_list')
    parser.add_argument('savefolder')
    args = parser.parse_args()

    get_labels_by_md5(args.md5_list, args.savefolder)
