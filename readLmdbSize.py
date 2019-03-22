import lmdb
env = lmdb.open("/home/lk/caffe_ssd/combine_panchenglong_lmdb/")
txn = env.begin()
print txn.stat()['entries']
