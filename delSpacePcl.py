import os;
def rename(path):
    i=0
# 	path = unicode(oldPath, "utf-8")
    filelist=os.listdir(path)
    #for root, dirs, files in os.walk(path):
    for files in filelist:
        i=i+1
        Olddir=os.path.join(path,files)   
        print "olddir is " + Olddir
        if os.path.isdir(Olddir):
            print "panchenglong1"
            rename(Olddir)
        print "panchenglong2"
        filename=os.path.splitext(files)[0];
        filetype=os.path.splitext(files)[1];
        Newdir=os.path.join(path,filename.replace(' ', '')+filetype);
        print Newdir
        os.rename(Olddir,Newdir)
#path="\home\lk\caffe_ssd\data\yunnan20180915"
#path="/home/lk/caffe_ssd/data/yunnan20180915/youren-oyq-ok"
path1="/home/lk/caffe_ssd/data/shouFeiZhanSuiDao/"
rename(path1)
