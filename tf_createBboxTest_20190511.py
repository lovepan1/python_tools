'''
Created on 2018-12-26

@author: st003026
'''
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

#sets=[('2012', 'train'), ('2012', 'val'), ('2007', 'train'), ('2007', 'val'), ('2007', 'test')]
sets=[('2007', 'test')]
#classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
classes = ["DiaoChe", "TaDiao", "TuiTuJi", "BengChe", "WaJueJi", "ChanChe", "SuLiaoBu", "FengZheng", "Niao", "NiaoWo", "ShanHuo", "YanWu", "JianGeBang", "JueYuanZi", "FangZhenChui"]
img_dir = "/home/pcl/data/VOC2007/JPEGImagesTest/"
def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(year, image_id, geshi, out_file):
    try:
        #print("open xml file is %s" %image_id)
        in_file = open('AnnotationsTest/%s.xml'%(image_id.split(".")[0]))
    except:
        print(geshi)
        print("the remove file is%s" %image_id)
        return 0
   # out_file = open('labels/%s.txt'%(image_id), 'w')
    if not os.path.exists('labels/'+ image_id.split("/")[0]):
        os.makedirs("labels/" + image_id.split("/")[0])
    #out_file = open('labels/' + image_id + '.txt', 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    label_txt = ""
    for obj in root.iter('object'):
        #difficult = obj.find('difficult').text
        cls = obj.find('name').text
        #if cls not in classes or int(difficult) == 1:
        if cls not in classes :
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
       # bb = convert((w,h), b)
        label_txt = label_txt + str(b[0]) + " "+ str(b[2]) + " "+ str(b[1]) +" "+ str(b[3]) + " " + str(cls_id) + " "
        #label_txt = label_txt + " ".join([str(a) for a in bb]) + " " + str(cls_id) + " "
    label_txt.strip()
    out_file.append((img_dir + image_id + " " + label_txt).strip())

wd = getcwd()

for year, image_set in sets:
    if not os.path.exists('labels/'):
        os.makedirs('labels/')
    img_ids = []
    #image_ids = open('ImageSets/Main/train.txt').read().strip().split()

    img_list = os.listdir(img_dir)
    print("all of the image len is ", len(img_list))
    for img in img_list:
        ids = os.path.join(img_dir, img)
        img_ids.append(ids)
    print("the current img_ids len is ", len(img_ids))
    list_file = open('%s_%s.txt'%(year, image_set), 'w')
    out_file = []
    for image_id in img_ids:
        #print(image_id)
        imageName = image_id.split("/")[-2] + "/"+ image_id.split("/")[-1] 
        #print(imageName.split(".")[0])
       # list_file.write('%s/VOCdevkit/VOC%s/JPEGImages/%s.jpg\n'%(wd, year, image_id))
        convert_annotation(year, imageName.split('/')[-1], imageName.split(".")[1], out_file)
    for i in out_file:
        list_file.write(str(i) + '\n')
    list_file.close()
    print("sum img is ", len(out_file))
