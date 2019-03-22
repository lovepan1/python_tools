#!/usr/bin/python
import lmdb
import random
from caffe.proto import caffe_pb2
e = lmdb.open("/home/lk/dataShiYan/lmdb/shanDongCombine")
e.set_mapsize(1000L*1000L*1000L*16)
t=e.begin(write=True)
idbs = ["/home/lk/dataShiYan/lmdb/data/SHDLFirstTrainEvalAll/DaoXianZengQiang", "/home/lk/dataShiYan/lmdb/data/SHDLFirstTrainEvalAll/evalZengQiang/"]
idx = 0
nos=[]
id=[]
datum=caffe_pb2.AnnotatedDatum()
for idb in idbs:
	te=lmdb.open(idb)
	tt=te.begin()
	td=tt.cursor()
	while td.next():
		nos.append(idx)
	td.first()
	idx=idx+1
	id.append(td)
random.shuffle(nos)
i=0
for no in nos:
	print id[no].key()
	t.put(id[no].key(),id[no].value())
	id[no].next()
	if(i%100==0):
		t.commit()
		t=e.begin(write=True)
	i=i+1;
t.commit()
