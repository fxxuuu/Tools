# -*- coding: utf-8 -*-
import sys
import os

print "hi"
if len(sys.argv) != 5:
    print('Usage: img_list hf_file cut_list save_file')
    sys.exit(-1)

iml = [i.rstrip('\n') for i in open(sys.argv[1]).readlines()]
pds = open(sys.argv[2]).readlines()
cut = [i.rstrip('\n') for i in open(sys.argv[3]).readlines()]
save = sys.argv[4]

fd = os.path.dirname(save)
if len(fd) and not os.path.isdir(fd):
    os.makedirs(fd)

info = {i: p for i,p in zip(iml, pds)}
assert len(info) == len(iml) == len(pds)
print('load %d'%len(info))

res = [info[c] for c in cut]

with open(save, 'w') as ft:
    ft.writelines(res)

print('saved %d to %s'%(len(cut), save))
