#!/usr/bin/python
import lmdb
from caffe.proto import caffe_pb2
#cls = [1,2,4,5,6,7]
cls = [2]
datum=caffe_pb2.AnnotatedDatum()
outdb = lmdb.open("onlytruck_lmdb")
indb =lmdb.open("combine_sdgc_lmdb")
outdb.set_mapsize(1000L*1000L*1000L*16)
t=outdb.begin(write=True)
tt=indb.begin()
td=tt.cursor()
i=0
for (key,value) in td:
	find = 0
	datum.ParseFromString(value)
       	groups = datum.annotation_group
	for group in groups:
		if (group.group_label in cls):
			find = 1
			break
	if find == 1:
		t.put(key,value)
		if(i%100==0):
			t.commit()
			t=outdb.begin(write=True)
		i=i+1;
t.commit()
print "total:"+i
