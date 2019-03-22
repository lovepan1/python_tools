import lmdb
e1 = lmdb.open("st/st/lmdb/st_newtrain_lmdb")
e2 = lmdb.open("st/st/lmdb/st_bktrain_lmdb")
e1.set_mapsize(1000L*1000L*1000L*16)
print e1.stat()
print e2.stat()
t1 = e1.begin(write=True)
t2 = e2.begin()
d1 = t1.cursor()
d2 = t2.cursor()
i = 0
while (i < 5000):
	for (key, value) in d2:
		newkey = key + "%d"%(i)
		t1.put(newkey,value)
		if (i%5 == 0):
			t1.commit()
			t1 = e1.begin(write=True)
		i+=1
print i
