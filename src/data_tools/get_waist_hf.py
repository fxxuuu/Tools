# -*- coding=utf-8 -*-
import numpy as np
import argparse, os
import itertools
import pymongo
from human_db_libs import get_human_db
from pprint import pprint
import sys
import tqdm

#function : produce md5 in hide
def mkdirs_if_missing(folder):
	if not os.path.exists(folder):
		os.makedirs(folder)
# 检查某个属性时get相关文档
def get_certain_doc(col):
	#return col.find({'$and':[{'result':{'$exists':True}},{'result.raw.Rects.properties':{'$exists':False}}]}).batch_size(10)
	return col.find({'result.raw.Rects.properties.human_hide.0':{'$ne':'others'}}).batch_size(10)


def get_buffer_db():
	SETTINGS = {
		'host': '172.16.10.9:27017',
		'port': 27017,
		'database': 'bufferdb',
		'username': 'buffer-db',
		'password': 'royvOGNDulYtRtFQD7tecgl+hZY='
	}
	try:
		client = pymongo.MongoClient(SETTINGS['host'], SETTINGS.get('port', 27017))
		if SETTINGS.get('username') and SETTINGS.get('password'):
			client[SETTINGS['database']].authenticate(SETTINGS['username'], SETTINGS['password'])
		db = client[SETTINGS['database']]
		return db
	except KeyError as e:
		raise Exception('config must have key %s' % (e.__str__()))
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
		exit('Failed to connect momenta db, terminating.')
	db = conn.dora
	return db

def get_db(server_name):
	return{'human':get_human_db(db_name),
		   'buffer':get_buffer_db(),
		   'momenta':get_momenta_db()}[server_name]

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('server_name',default='human',choices=['human','momenta','buffer'])
	parser.add_argument('db_name') #train
	parser.add_argument('col_name1') #human_hide
	parser.add_argument('save_folder') #iou
	args = parser.parse_args()
	server_name, db_name, col_name1, save_folder = \
		args.server_name, args.db_name, args.col_name1, args.save_folder

	db = get_db(server_name)
	col1 = db.get_collection(col_name1)

	mkdirs_if_missing(save_folder)

	f1 = open(save_folder+'/human_waist_17_upground.md5','w')
	f2 = open(save_folder+'/human_waist_17_upground.hf','w')
	#f3 = open(save_folder + '/human_waist_17_underground.md5', 'w')
	#f4 = open(save_folder + '/human_waist_17_underground.hf', 'w')

	docs1 = col1.find({'result.raw.Rects.properties.location':'upground'}).batch_size(10)

	max_steps = docs1.count()
	print(max_steps)
	p_bar = tqdm.tqdm(total=max_steps)  # 测试时去掉//10000+1


	for doc in docs1:
		md5 = doc.get('md5')
		# f1.write(md5)
		# f1.write('\n')
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
					waist_value = (rect.get('points_17')[11]['y'] + rect.get('points_17')[12]['y'])/2 if score ==  2 else -1
				# if 'new' in rect['properties']['rect_type'][0]:
				# 	hf_fw_new.write(
				# 		" {} {} {} {} {}".format(x1, y1, x2, y2, score))  # write to the human_format file
				# if 'fixed' in rect['properties']['rect_type'][0]:
				# 	hf_fw_fixed.write(
				# 		" {} {} {} {} {}".format(x1, y1, x2, y2, score))  # write to the human_format file
					f2.write(
						' {} {} {} {} {} {}'.format(x1, y1, x2, y2, waist_value, score)
					)
			# hf_fw_new.write('\n')
			# hf_fw_fixed.write('\n')
				f2.write('\n')
				f1.write(md5)
				f1.write('\n')
				p_bar.update(1)
	p_bar.close()
