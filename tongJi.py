#!/usr/bin/python
# -*- coding:utf-8 -*-
import xml.etree.ElementTree as ET
import os
import sys
#import cv2
c={}
if len(sys.argv) <= 1:
	#print "统计文件夹下xml文档所有类别的数目，并生成class.txt"
	path = raw_input("input tongji dir:")
else:
	path = sys.argv[1]
def xml2jpg1(xml):
	return xml.replace(".xml", ".jpg")

if not os.path.exists(path+"/class"):
    os.mkdir(path+"/class")
for root,folders,files in os.walk(path): 
	for f in files:
		if (f.find(".xml") != -1):
			in_file = open(root+"/"+f)
			tree=ET.parse(in_file)
			r = tree.getroot()
			for obj in r.iter('object'):
				cls = obj.find('name').text
				if cls is None:
					#print "panchenlgongNone"+ xml2jpg1(os.path.abspath(root+"/"+f))
					continue
				if len(cls) == 0:
                		 print("panchenlongLen0"+ xml2jpg1(os.path.abspath(root+"/"+f))  )
				if cls in c:
					c[cls][0].write(xml2jpg1(os.path.abspath(root+"/"+f))+"\n")
					c[cls][1]=c[cls][1]+1
				else:
					c[cls]=[]
					c[cls].append(open(path+"/class/c_"+cls+".txt","w"))
					c[cls][0].write(xml2jpg1(os.path.abspath(root+"/"+f))+"\n")
					c[cls].append(1)
			in_file.close()
for key in c:
	print(key, " ", c[key])






