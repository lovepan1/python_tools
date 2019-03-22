#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import cv2
import xml.etree.ElementTree as ET
class dataDel(object):
    def __init__(self):
       # self.delSpacePath = spacePath
     #   self.delnoneLabelPath = noneLabelPath
        self.numSpaceFile = 0
        self.numNoneLabelFile = 0
    def delSpace(self, spacePath):
        filelist=os.listdir(spacePath)
        for files in filelist:
            delSpaceOlddir=os.path.join(spacePath,files) 
            if os.path.isdir(delSpaceOlddir): 
                self.delSpace(delSpaceOlddir)
            filename=os.path.splitext(files)[0];
            delSpaceNewDir=os.path.join(spacePath,filename.replace(' ', '')+filetype); 
            self.numSpaceFiles = self.numSpaceFiles + 1
            print "the del space file is " + Newdir
            os.rename(delSpaceOlddir,delSpaceNewDir)
    def delNoneLabel(self, noneLabelPath):
        filelist=os.listdir(path2)
        for files in filelist:
            noneLabelOldDir=os.path.join(path,files)               
            if os.path.isdir(noneLabelOldDir):
                self.delNoneLabel(noneLabelOldDir)
            fileType = os.path.splitext(files)[1];    
            if fileType == '.xml':      
                with open(oldDir, "r") as f:
                    data = f.read()  
                    if data.find('None') >= 0:
                        self.numNoneLabelFile = self.numNoneLabelFile + 1
                        print "del noneLabel dir is " + noneLabelOldDir
                        os.remove(noneLabelOldDir)    
    def printNum(self):
        print "the current delSpace file is %d" % self.numSpaceFile
        print "the current delNoneLabel file is %d" % self.numNoneLabelFile

if __name__ =='__main__':
    path1 = "/home/lk/caffe_ssd/data"
    path2 = "/home/lk/dataBeiFen/"
    dealData = dataDel()
    dealData.delSpace(path1)
    dealData.delNoneLabel(path2)
    print "the function is over"
                          
        