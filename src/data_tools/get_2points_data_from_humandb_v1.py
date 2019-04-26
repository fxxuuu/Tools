# -*- coding=utf-8 -*-
import argparse
# from human_db_libs import get_human_db
import os, sys, tqdm
import numpy as np
import itertools
import pymongo
from pprint import pprint

def mkdirs_if_missing(folder):
	if not os.path.exists(folder):
		os.makedirs(folder)
# 检查某个属性时get相关文档
def get_certain_doc(col):
	#return col.find({'$and':[{'result':{'$exists':True}},{'result.raw.Rects.properties':{'$exists':False}}]}).batch_size(10)
	return col.find({'result.raw.Rects.properties.human_hide.0':{'$ne':'others'}}).batch_size(10)

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

def get_db(server_name):
	return{'human':get_human_db(db_name)}[server_name]

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('server_name', default='human', choices=['human', 'momenta', 'buffer'])
	parser.add_argument('db_name')  # train
	parser.add_argument('col_name')  # human_properties
	parser.add_argument('save_folder')
	args = parser.parse_args()
	server_name, db_name, col_name, save_folder = \
		args.server_name, args.db_name, args.col_name, args.save_folder

	db = get_db(server_name)
	col = db.get_collection(col_name)

	mkdirs_if_missing(save_folder)

	f1 = open(save_folder + '/human_2points_upground_v1.md5', 'w')
	f2 = open(save_folder + '/human_2points_upground_v1.hf', 'w')
	f3 = open(save_folder + '/human_2points_upground_v1.wh', 'w')
	# f3 = open(save_folder + '/human_waist_17_underground.md5', 'w')
	# f4 = open(save_folder + '/human_waist_17_underground.hf', 'w')
	print "1"

	docs = col.find({'result.raw.Rects.properties.location': 'upground'}).batch_size(10)
	print "2"
	# max_size = docs.count()
	# print max_size
	# p_bar = tqdm.tqdm(total=max_steps)  # 测试时去掉//10000+1

	point_num_0 = 0
	point_num_1 = 0
	point_num_2 = 0
	point_num = 0
	cnt = 0
	valid_cnt = 0
	ignore_cnt = 0

	for doc in docs:
		cnt += 1

		sys.stdout.write('\r{}, {}, {}, point_num: 0-{}, 1-{}, 2-{}'.format(cnt, valid_cnt, ignore_cnt, point_num_0, point_num_1, point_num_2))
		sys.stdout.flush()

		md5 = doc.get('md5')
		# f1.write(md5)
		# f1.write('\n')
		size = doc.get('size')
		width = size.get('width')
		height = size.get('height')
		result = doc['result']
		raw = result.get('raw')
		Rects = raw.get('Rects')
		# pprint.pprint(Rects)
		if (Rects):
			write_signal = 1

			for rect in Rects:
				if rect['v'] == 2 and ('points_17' not in rect.keys() or len(rect['points_17']) != 17):
					write_signal = 0
					break

			if write_signal:
				f2.write(str(len(Rects)))
				for rect in Rects:
					x1 = rect.get('x')
					y1 = rect.get('y')
					x2 = rect.get('w') + x1
					y2 = rect.get('h') + y1
					score = rect.get('v')

					if score == 0:
						ignore_cnt += 1
						nose_x = nose_y = nose_v = 0
						waist_x1 = waist_y1 = waist_v1 = 0
						waist_x2 = waist_y2 = waist_v2 = 0

					elif score == 2:
						valid_cnt += 1
						nose_x = rect.get('points_17')[0]['x']
						nose_y = rect.get('points_17')[0]['y']
						nose_v = rect.get('points_17')[0]['v']
						if nose_v == 0:
							point_num_0 += 1
						elif nose_v == 1:
							point_num_1 += 1
						elif nose_v == 2:
							point_num_2 += 1
						point_num += 1

						waist_x1 = rect.get('points_17')[11]['x']
						waist_y1 = rect.get('points_17')[11]['y']
						waist_v1 = rect.get('points_17')[11]['v']
						if waist_v1 == 0:
							point_num_0 += 1
						elif waist_v1 == 1:
							point_num_1 += 1
						elif waist_v1 == 2:
							point_num_2 += 1
						point_num += 1

						waist_x2 = rect.get('points_17')[12]['x']
						waist_y2 = rect.get('points_17')[12]['y']
						waist_v2 = rect.get('points_17')[12]['v']
						if waist_v2 == 0:
							point_num_0 += 1
						elif waist_v2 == 1:
							point_num_1 += 1
						elif waist_v2 == 2:
							point_num_2 += 1
						point_num += 1
					# if 'new' in rect['properties']['rect_type'][0]:
					# 	hf_fw_new.write(
					# 		" {} {} {} {} {}".format(x1, y1, x2, y2, score))  # write to the human_format file
					# if 'fixed' in rect['properties']['rect_type'][0]:
					# 	hf_fw_fixed.write(
					# 		" {} {} {} {} {}".format(x1, y1, x2, y2, score))  # write to the human_format file
					f2.write(
						' {} {} {} {} {} {}'.format(x1, y1, x2, y2, score, nose_x, nose_y, waist_x1, waist_y1, waist_x2, waist_y2, nose_v, waist_v1, waist_v2)
					)
				# hf_fw_new.write('\n')
				# hf_fw_fixed.write('\n')
				f2.write('\n')
				f1.write(md5)
				f1.write('\n')
				f3.write(str(width) + " " + str(height) + "\n")

	print 'The point number for value 0, 1, and 2 are {}, {} and {}'.format(point_num_0, point_num_1, point_num_2)
	