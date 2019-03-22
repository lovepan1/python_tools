## -*- coding:utf8 -*-
import os
import sys
class addImage2Txt(object):
    fileType = ".jpg .png .bmp .jpeg"
    def __init__(self, argv):
        #self.path = 'G:/datasets/Train/DaoXianYiWu'
        self.path = argv
    def listFilesToTxt(self, dir,file,fileType,recursion):
        exts = fileType.split(" ")
        files = os.listdir(dir)
        files.sort()
	for name in files:
	    print name
            fullname=os.path.join(dir,name)
            if(os.path.isdir(fullname) & recursion):
                self.listFilesToTxt(fullname,file,fileType,recursion)
            else:
                #for ext in exts:
                if(name.endswith('.jpg')):
                    (filename,extension) = os.path.splitext(name)
                    file.write(dir + name + "\n")
                    #break
    def add2Txt(self):
        dir = self.path
        outfile = self.path + "/jiGuangGaoSuTest.txt"
        try:               
            file = open(outfile,"w")
            self.listFilesToTxt(dir,file,self.fileType, 1)
            file.close()
        except:
            print("open file is failed")


if __name__ == '__main__':
    filePathList = sys.argv
    filePath = filePathList[1]
    #filePath = sys.argv
    demo = addImage2Txt(filePath)
    demo.add2Txt()
