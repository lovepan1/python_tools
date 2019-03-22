import caffe
import numpy as np
import cv2
from caffe.proto import caffe_pb2
import lmdb
e1 = lmdb.open("st/st/lmdb/st_newtrain_lmdb")
e1.set_mapsize(1000L*1000L*1000L*16)
t1 = e1.begin(write=True)
d1 = t1.cursor()
datum = caffe_pb2.AnnotatedDatum()
i = 0
for (key, value) in d1:
	if (key.find("s1")!=0):
		print "del "+key
		t1.delete(key)
#		if (i%5 == 0):
#			t1.commit()
#			t1=e1.begin(write=True)
#			d1 = t1.cursor()
		i = i+1
		if (i > 4900):
			break;
t1.commit()
