import os;
def delNoneLabel(path):
    i=0
# 	path = unicode(oldPath, "utf-8")
    filelist=os.listdir(path)
    #for root, dirs, files in os.walk(path):
    for files in filelist:
        i=i+1
        oldDir=os.path.join(path,files)   
        if os.path.isdir(oldDir):
            delNoneLabel(oldDir)        
        fileName = os.path.splitext(files)[0];
        fileType = os.path.splitext(files)[1];
        if fileType == '.xml':        
            with open(oldDir, "r") as f:
                data = f.read()
                if data.find('None') >= 0 :
                    print "del dir is " + oldDir
                    os.remove(oldDir)    
path1="/home/lk/dataBeiFen/"
delNoneLabel(path1)