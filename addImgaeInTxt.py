## -*- coding:utf8 -*-
#import os
#import sys
#class addImage2Txt(object):
#    def __init__(self):
#        self.path = 'E:/PCLDataCompany/111/bird-ok'
#        #self.path = argv
#    allFileType = ["jpg", "png", "bmp", "jpeg"]
#    def add2Txt(self):
#        fileList = os.listdir(self.path)
#        try:
#            txtFile = open("E:/PCLDataCompany/111/bird-ok/jiGuangGaoSuTest.txt", "w")
#        except:
#            print("open file is failed")
#            return 0
#        for file in fileList:
#            totalFileNum = len(fileList)
#            fileType = file.split('.')[-1]
#            if fileType in self.allFileType:            
#                
#                print(file)
#                print(fileType)
#        
#if __name__ == '__main__':
#    #filePathList = sys.argv
#    #filePath = filePathList[1]
#    demo = addImage2Txt()
#    demo.add2Txt()
#   

import os
import sys
class addImage2Txt(object):
    fileType = ".jpg .png .bmp .jpeg"
    def __init__(self, argv):
#        self.path = 'E:/PCLDataCompany/111/bird-ok'
        self.path = argv
    def listFilesToTxt(self, dir,file,fileType,recursion):
        exts = fileType.split(" ")
        files = os.listdir(dir)
        for name in files:
            fullname=os.path.join(dir,name)
            if(os.path.isdir(fullname) & recursion):
                self.listFilesToTxt(fullname,file,fileType,recursion)
            else:
                for ext in exts:
                    if(name.endswith(ext)):
                        (filename,extension) = os.path.splitext(name)
                        file.write(dir + name + "\n")
                        break
    def add2Txt(self):
        dir = self.path
        outfile = self.path + "/jiGuangGaoSuTest.txt"
        try:               
            file = open(outfile,"w")
            self.listFilesToTxt(dir,file,self.fileType, 1)
            file.close()
        except:
            print("open file is failed")
#    def Test():
#      dir='E:/PCLDataCompany/111/bird-ok'
#      outfile="E:/PCLDataCompany/111/bird-ok/jiGuangGaoSuTest.txt"
#      fileType = ".jpg .png .bmp .jpeg"
#     
#      file = open(outfile,"w")
#      if not file:
#        print ("cannot open the file %s for writing" % outfile)
#      ListFilesToTxt(dir,file,fileType, 1)
#     
#      file.close()
#    Test()

if __name__ == '__main__':
    filePathList = sys.argv
    filePath = filePathList[1]
    demo = addImage2Txt(filePath)
    demo.add2Txt()