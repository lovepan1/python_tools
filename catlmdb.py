import lmdb
#combine two lmdb
e1 = lmdb.open("st/st/lmdb/st_sttrain_lmdb")
e2 = lmdb.open("coco/mycoco/lmdb/mycoco_train2014_lmdb")
e1.set_mapsize(1000L*1000L*1000L*16)
print e1.stat()
print e2.stat()
t1 = e1.begin(write=True)
t2 = e2.begin()
d1 = t1.cursor()
d2 = t2.cursor()
i = 0
for (key, value) in d2:
	print key
	t1.put(key,value)
	if (i%5 == 0):
		t1.commit()
		t1 = e1.begin(write=True)
	i+=1
print i
