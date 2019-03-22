#!/usr/bin/python
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join


#classes={"bicycle":10, "bus":1, "car":2, "motorbike":3, "person":4, "truck":5, "suv":6, "minibus":7, "minitruck":8, "dangerouscar":9}
classes={"car":1,"minicar":1, "truck":2,"minitruck":2, "motorbike":6, "person":3, "truck":2, "suv":1,"bus":5, "minibus":5, "dangerouscar":7}
def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)
def mklabel(xml_file):
    in_file = open(xml_file)
    txt_file=xml_file.replace(".xml",".txt")
    out_file = open(txt_file, 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes[cls]
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

listfile = open("train.txt",'w')
for root,dirs,files in os.walk("."):
    for file in files:
	    if (file.find(".xml") != -1):
		mklabel(root+"/"+file)
	    if (file.find(".png") != -1):
		listfile.write(os.path.abspath(root+"/"+file)+'\n')
listfile.close()


