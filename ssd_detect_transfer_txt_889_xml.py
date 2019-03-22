#encoding=utf8
import os
import sys
import argparse
import numpy as np
from PIL import Image, ImageDraw
# Make sure that caffe is on the python path:
caffe_root = './'
os.chdir(caffe_root)
sys.path.insert(0, os.path.join(caffe_root, 'python'))
import caffe

from google.protobuf import text_format
from caffe.proto import caffe_pb2


def get_labelname(labelmap, labels):
    num_labels = len(labelmap.item)
    labelnames = []
    if type(labels) is not list:
        labels = [labels]
    for label in labels:
        found = False
        for i in xrange(0, num_labels):
            if label == labelmap.item[i].label:
                found = True
                labelnames.append(labelmap.item[i].display_name)
                break
        assert found == True
    return labelnames

def getMax(n1, n2, n3, n4):
    max_num = 0
    listNum = []
    listNum.append(n1)
    listNum.append(n2)
    listNum.append(n3)
    listNum.append(n4)
    max_num = max(listNum)
    print('max num is %d'%(max_num))
    return max_num
        
class CaffeDetection:
    def __init__(self, gpu_id, model_def, model_weights, image_resize, labelmap_file):
        caffe.set_device(gpu_id)
        caffe.set_mode_gpu()

        self.image_resize = image_resize
        # Load the net in the test phase for inference, and configure input preprocessing.
        self.net = caffe.Net(model_def,      # defines the structure of the model
                             model_weights,  # contains the trained weights
                             caffe.TEST)     # use test mode (e.g., don't perform dropout)
         # input preprocessing: 'data' is the name of the input blob == net.inputs[0]
        self.transformer = caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})
        self.transformer.set_transpose('data', (2, 0, 1))
        self.transformer.set_mean('data', np.array([104, 117, 123])) # mean pixel
        # the reference model operates on images in [0,255] range instead of [0,1]
        self.transformer.set_raw_scale('data', 255)
        # the reference model has channels in BGR order instead of RGB
        self.transformer.set_channel_swap('data', (2, 1, 0))

        # load PASCAL VOC labels
        file = open(labelmap_file, 'r')
        self.labelmap = caffe_pb2.LabelMap()
        text_format.Merge(str(file.read()), self.labelmap)

    def detect(self, image_file, conf_thresh=0.5, topn=5):
        '''
        SSD detection
        '''
        # set net to batch size of 1
        # image_resize = 300
        self.net.blobs['data'].reshape(1, 3, self.image_resize, self.image_resize)
        print image_file
        image = caffe.io.load_image(image_file)
        #Run the net and examine the top_k results
        transformed_image = self.transformer.preprocess('data', image)
        self.net.blobs['data'].data[...] = transformed_image

        # Forward pass.
        detections = self.net.forward()['detection_out']

        # Parse the outputs.
        det_label = detections[0,0,:,1]
        det_conf = detections[0,0,:,2]
        det_xmin = detections[0,0,:,3]
        det_ymin = detections[0,0,:,4]
        det_xmax = detections[0,0,:,5]
        det_ymax = detections[0,0,:,6]

        # Get detections with confidence higher than 0.6.
        top_indices = [i for i, conf in enumerate(det_conf) if conf >= conf_thresh]

        top_conf = det_conf[top_indices]
        top_label_indices = det_label[top_indices].tolist()
        top_labels = get_labelname(self.labelmap, top_label_indices)
        top_xmin = det_xmin[top_indices]
        top_ymin = det_ymin[top_indices]
        top_xmax = det_xmax[top_indices]
        top_ymax = det_ymax[top_indices]

        result = []
        for i in xrange(min(topn, top_conf.shape[0])):
            xmin = top_xmin[i] # xmin = int(round(top_xmin[i] * image.shape[1]))
            ymin = top_ymin[i] # ymin = int(round(top_ymin[i] * image.shape[0]))
            xmax = top_xmax[i] # xmax = int(round(top_xmax[i] * image.shape[1]))
            ymax = top_ymax[i] # ymax = int(round(top_ymax[i] * image.shape[0]))
            score = top_conf[i]
            label = int(top_label_indices[i])
            label_name = top_labels[i]
            result.append([xmin, ymin, xmax, ymax, label, score, label_name])
            #print("panchenglongNum is %" %i)
        return result

def main(args):
    '''main '''
    detection = CaffeDetection(args.gpu_id,
                               args.model_def, args.model_weights,
                               args.image_resize, args.labelmap_file)
    imageFiles = open(args.image_file)    
    txtFile = open('xml4.txt' , 'w')
    for line in imageFiles:
        line1 = line.replace('\n', '')
        filePath = line1.replace(' ', '')
        print "the last path is " + filePath
        result = detection.detect(filePath)
        #print result
        try:
          img = Image.open(filePath)
        except:
          continue
        #draw = ImageDraw.Draw(img)
        width, height = img.size
        txtFileLine = filePath + ' '
        objectNum = 0
        print width, height
        locationInfo = []
        for item in result:
            objectNum += 1
            if item[1] == float('inf') or item[1] == float('-inf'):
                objectNum = 0
                break
            xmin = int(round(item[0] * width))
            ymin = int(round(item[1] * height))
            xmax = int(round(item[2] * width))
            ymax = int(round(item[3] * height))
            #draw.rectangle([xmin, ymin, xmax, ymax], outline=(255, 0, 0))
            #draw.text([xmin, ymin], item[-1] + str(item[-2]), (0, 0, 255))
            locationInfo.append(' '+ str(item[4])+ ' ' +  str(xmin) + ' ' + str(ymin) + ' ' + str(xmax)+ ' ' + str(ymax))
            print item
            print [xmin, ymin, xmax, ymax]
            print [xmin, ymin], item[-1]     
        imageName = filePath.split('/')[-1] 
        txtFileLine = imageName + ' ' + str(width) + ' ' + str(height) +' ' +bytes(objectNum)
        if objectNum > 0:
            for a in locationInfo:
                txtFileLine += a
        txtFileLine = txtFileLine + '\n'
        txtFile.write(txtFileLine)
        #img.save("resultImages/" + imageName)
    txtFile.close()
    
    f1 = open('xml1.txt')
    f2 = open('xml2.txt')
    f3 = open('xml3.txt')
    f4 = open('xml4.txt')
    #f5 = open('xml5.txt')
    #f6 = open('xml6.txt')
    xml_file = open(('jinsanli.xml'), 'w')
    labelName = ['bk', 'DiaoChe', 'TaDiao', 'ShiGongJiXie', 'DaoXianYiWu', 'ShanHuo', 'YanWu']
    #xml_file.write('<?xml version="1.0" encoding="utf-8"?>\n')
    xml_file.write('<annotation>\n')
    f1List = f1.readlines()
    f2List = f2.readlines()
    f3List = f3.readlines()
    f4List = f4.readlines()
    #f5List = f5.readlines()
    #f6List = f6.readlines()
    if(len(f1List) != len(f2List) or len(f2List) != len(f3List)):
         print('shape is error')
    maxIter = getMax(len(f1List), len(f2List), len(f3List), len(f4List))
    for idx in range(maxIter):
        try:
            line1 = f1List[idx].replace('\n', '')
        except:
            line1 = 'error1.jpg 1200 900 0'
        try:       
            line2 = f2List[idx].replace('\n', '')
        except:
            line2 = 'error2.jpg 1200 900 0'
        try:
            line3 = f3List[idx].replace('\n', '')
        except:
            line3 = 'error3.jpg 1200 900 0'
        try:
            line4 = f4List[idx].replace('\n', '')
        except:
            line4 = 'error4.jpg 1200 900 0'
        objectNum1 = int(line1.split(' ')[3]) 
        print('line1 name is %s' %line1.split(' ')[0])
        objectNum2 = int(line2.split(' ')[3]) 
        print('line2 name is %s' %line2.split(' ')[0])
        objectNum3 = int(line3.split(' ')[3]) 
        print('line3 name is %s' %line3.split(' ')[0])
        objectNum4 = int(line4.split(' ')[3]) 
        print('line4 name is %s' %line3.split(' ')[0])
        bestObject = getMax(objectNum1, objectNum2, objectNum3, objectNum4)
        print(objectNum1)
        print(objectNum2)
        print(objectNum3)
        print(objectNum4)
        bestxml = ''
        if bestObject == objectNum1:
            useLine = line1
            bestxml = 'xml1'
        if bestObject == objectNum2:
            useLine = line2
            bestxml = 'xml2'
        if bestObject == objectNum3:
            useLine = line3
            bestxml = 'xml3'
        if bestObject == objectNum4:
            useLine = line4
            bestxml = 'xml4'
        print('best line is %s' % bestxml)
        imageName = useLine.split(' ')[0]
        width = useLine.split(' ')[1]
        height = useLine.split(' ')[2]
        objectNum = useLine.split(' ')[3] 
        if int(objectNum) == 0:
            flag = 'False'
        else:
            flag = 'True'
        xml_file.write('    <result filename=' + '"' + str(imageName.split('.')[0]) + '" ' + 'flag="' + flag + '">\n')
        xml_file.write('        <size>\n')
        xml_file.write('            <width>' + str(width) + '</width>\n')
        xml_file.write('            <height>' + str(height) + '</height>\n')
        xml_file.write('            <depth>3</depth>\n')
        xml_file.write('        </size>\n')
        if flag == 'True':
            for number in range(0, int(objectNum)):
                labelType = useLine.split(' ')[4 + number*5]
                xml_file.write('        <object name="'+ labelName[int(labelType)] + '">\n')
                xml_file.write('            <bndbox>\n')
                xml_file.write('                <xmin>' + str(useLine.split(' ')[number*5+5]) + '</xmin>\n')
                xml_file.write('                <ymin>' + str(useLine.split(' ')[number*5+6]) + '</ymin>\n')
                xml_file.write('                <xmax>' + str(useLine.split(' ')[number*5+7]) + '</xmax>\n')
                xml_file.write('                <ymax>' + str(useLine.split(' ')[number*5+8].replace('\n', '')) + '</ymax>\n')
                xml_file.write('            </bndbox>\n')
                xml_file.write('        </object>\n')
        xml_file.write('    </result>\n')
    xml_file.write('</annotation>\n')   
    f1.close()
    f2.close()
    f3.close()
    f4.close()



def parse_args():
    '''parse args'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--gpu_id', type=int, default=1, help='gpu id')
    parser.add_argument('--labelmap_file',
                        default='labelmapSDDLTrain.prototxt')
    parser.add_argument('--model_def',
                        default='models/SDDLModel/deploy889.prototxt')
    parser.add_argument('--image_resize', default=889, type=int)
    parser.add_argument('--model_weights',
                        default='models/SDDLModel/ssd_512_vgg__iter_14000.caffemodel')
    parser.add_argument('--image_file', default='examples/images/jiGuangGaoSuTest.txt')
    return parser.parse_args()

if __name__ == '__main__':
    main(parse_args())
