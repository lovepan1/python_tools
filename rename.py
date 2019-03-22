# -*- coding:utf8 -*-
import os
import sys
class renameBatch(object):
    def __init__(self, argv):
        #self.path = 'E:/潘成龙公司数据集/111/birdNest-ok'
        self.path = argv
    fileType = [".jpg", ".png", ".bmp", ".jpeg"]
    def rename(self):
        filelist = os.listdir(self.path)
        total_num = len(filelist)
        i = 0
        for type in self.fileType:  
            for item in filelist:            
                if item.endswith(type):
                    src = os.path.join(os.path.abspath(self.path), item)
                    dst = os.path.join(os.path.abspath(self.path), str(("%06d" % i)) + type)
                    try:
                        os.rename(src, dst)
                        print ('converting %s to %s ...' % (src, dst))
                        i = i + 1
                    except:
                        continue     
        print ('total %d to rename & converted %d'  % (total_num, i))
if __name__ == '__main__':
    filePathList = sys.argv
    filePath = filePathList[1]
    demo = renameBatch(filePath)
    demo.rename()