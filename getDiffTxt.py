'''
Created on 2018-12-26

@author: st003026
'''
# encoding: utf-8
import os
import sys
import random
#trainval_percent = 0.66
trainPercent = 0.9
testPercent = 0.1
path = sys.path[0]
currenrPath = path.replace('getDiffTxt.py', '')    
xmlfilepath = 'JPEGImages'                      
listDirs = os.listdir(xmlfilepath) 
fileDir = []
xmlNum = []
picNum = []
#ftrainval = open('ImageSets/Main/trainval.txt', 'w')
ftest = open('ImageSets/Main/test.txt', 'w')
ftrain = open('ImageSets/Main/train.txt', 'w')
#fval = open('ImageSets/Main/val.txt', 'w')
for dir in listDirs:   
   # print(currenrPath + xmlfilepath + dir) 
    fileDir.append(currenrPath + "/" + xmlfilepath + "/" + dir) 
    #print(fileDir)
#for xmlList in fileDir:
  #  xmlFile = os.listdir(xmlList)
  #  for xml in xmlFile:
   #     if xml.split('.')[-1] == "xml":
    #        xmlNum.append(str(xmlList) + "\\" + xml)
#print(xmlNum)
#xmlNum1 = len(xmlNum)
#list=range(xmlNum1)
#tr=int(xmlNum1*trainPercent)
#tr=int(tv*train_percent)
#trainval= random.sample(list,tv)
#train=random.sample(list,tr)
for picList in fileDir:
    print(picList)
    picFile = os.listdir(picList)
    for pic in picFile:
        if pic.split('.')[-1] == "jpeg" or pic.split('.')[-1] == "bmp" or pic.split('.')[-1] == "jpg":
            picNum.append(str(picList) + "/" + pic)
    print(picNum)
picNum1 = len(picNum)
list=range(picNum1)
tr=int(picNum1*trainPercent)
train = random.sample(list, tr)
for i  in list:
    name=picNum[i]+'\n'
    print(name)
   # if i in trainval:
      #  ftrainval.write(name)
    if i in train:
        ftrain.write( name)
    else:
        ftest.write( name)
#ftrainval.close()
ftrain.close()
ftest.close()
#fval.close()