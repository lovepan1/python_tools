#!/usr/bin/python
import caffe
import numpy as np
import cv2
from caffe.proto import caffe_pb2
import lmdb
import sys
sys.path.append("/home/lk/caffe_dssd/python")
if len(sys.argv) <= 1:
	print "input dbname"
	sys.exit(0)
e1 = lmdb.open(sys.argv[1])
t1 = e1.begin()
d1 = t1.cursor()
datum = caffe_pb2.AnnotatedDatum()
lables=["bk","DiaoChe","TaDiao","ShiGongJiXie", "DaoXianYiWu", "YanHuo"]
colors=[(0,0,0), (255,255,0), (255,0,255), (0,255,255), (255,0,0), (0,255,0),(0,0,255), (255,255,255)]
i = 0
for (key, value) in d1:
	i=i+1
	datum.ParseFromString(value)
	group = datum.annotation_group
	data=datum.datum.data
	dd=np.fromstring(datum.datum.data, dtype=np.uint8)
	img = cv2.imdecode(dd,-1)
	h = img.shape[0]
	w = img.shape[1]
	find = 0
	for g in group:
		print g.group_label
		lable = lables[g.group_label]
		find = 1
		for anno in g.annotation:
			xmin=int(anno.bbox.xmin*w)
			xmax=int(anno.bbox.xmax*w)
			ymin=int(anno.bbox.ymin*h)
			ymax=int(anno.bbox.ymax*h)
			print (anno.bbox.xmin-anno.bbox.xmax)*(anno.bbox.ymin-anno.bbox.ymax)
	        	if g.group_label > 7:
       				g.group_label = 7
			cv2.rectangle(img, (xmin, ymin), (xmax,ymax), colors[g.group_label])
#			cv2.rectangle(img, (xmin, ymin), (xmax,ymax), colors[0])
                        cv2.putText(img, lable, (xmin, ymin), 0, 1, colors[g.group_label], 1,8)			
	if find == 1 :
		cv2.imshow('img', img)
		cv2.waitKey()
print i
