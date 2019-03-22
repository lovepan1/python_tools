import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import cv2
classes = ["bicycle", "bus", "car", "motorbike", "person", "truck", "minitruck"]
num=[0,0,0,0,0,0]
c={"bicycle":0, "bus":0, "car":0, "motorbike":0, "person":0, "truck":0, "suv":0, "minibus":0, "minitruck":0, "dangerouscar":0}
#w = cv2.VideoWriter("out.avi", cv2.VideoWriter_fourcc(*'XVID'), 20, (1920,1080))
for root,folders,files in os.walk("argv[1]"): 
	for f in files:
		if (f.find(".xml") != -1):
			in_file = open(root+"/"+f)
			tree=ET.parse(in_file)
			r = tree.getroot()
			for obj in r.iter('object'):
				cls = obj.find('name').text
				c[cls]=c[cls]+1
			#	if (cls == "truck" or cls == "minitruck"):
			#		ff=f.replace(".xml", ".png");
			#		img = cv2.imread(root+"/"+ff)
			#		w.write(img)
			in_file.close()
for key in c:
	print key+" ", c[key]
