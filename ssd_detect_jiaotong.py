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

class CaffeDetection:
    def __init__(self, gpu_id, model_def, model_weights, image_resize, labelmap_file):
        #caffe.set_device(gpu_id)
        
        caffe.set_mode_gpu()
        #print(caffe.mode)
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
       # print image_file
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
    labelName = ['bk', 'car', 'truck', 'person', 'bicycle', 'bus', 'motorbike', 'dangerouscar', 'NNN', 'MMM', 'KKK']
    detection = CaffeDetection(args.gpu_id,
                               args.model_def, args.model_weights,
                               args.image_resize, args.labelmap_file)
    imageFiles = open(args.image_file) 
    txtFile = open('xml1.txt' , 'w')   
    for line in imageFiles:
        line1 = line.replace('\n', '')
        filePath = line1.replace(' ', '')
        #print "the last path is " + filePath
        result = detection.detect(filePath)
        #print result 
        try:
          img = Image.open(filePath)
        except:
          continue
        draw = ImageDraw.Draw(img)
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
            draw.rectangle([xmin, ymin, xmax, ymax], outline=(255, 0, 0))
            draw.text([xmin, ymin], item[-1] + str(item[-2]), (0, 0, 255))
            locationInfo.append(' '+ str(item[4])+ ' ' +  str(xmin) + ' ' + str(ymin) + ' ' + str(xmax)+ ' ' + str(ymax))
            #print item
            print [xmin, ymin, xmax, ymax]
            print [xmin, ymin], item[-1]     
        imageName = filePath.split('/')[-1] 
        txtFileLine = imageName + ' ' + str(width) + ' ' + str(height) +' ' +bytes(objectNum)
        if objectNum > 0:
            for a in locationInfo:
                txtFileLine += a
        txtFileLine = txtFileLine + '\n'
        txtFile.write(txtFileLine)
        img.save("resultImages/" + imageName)
    txtFile.close()
    
    xml_file = open('xml1.txt')
    xml_file_list = xml_file.readlines()
    maxIter = len(xml_file_list)
    for idx in range(maxIter):
        #line1 = xml_file_list[idx].replace('\n', '')
 #       objectNum4 = int(line1.split(' ')[3]) 
        line1 = xml_file_list[idx].replace('\n', '')
        useLine = line1
        imageName = useLine.split(' ')[0]
        width = useLine.split(' ')[1]
        height = useLine.split(' ')[2]
        objectNum = useLine.split(' ')[3] 
        xml_file = open(('Annotations/' + imageName.split('.')[0]+ '.xml'), 'w')
        xml_file.write('<annotation>\n')
        #im = Image.open((src_img_dir+'/'+imageName))
        #im = Image.open((src_img_dir+'/'+'1.jpg'))
        #width, height = im.size
        if int(objectNum) == 0:
            flag = 'False'
        else:
            flag = 'True'
        xml_file.write('    <filename>' + str(imageName) + '</filename>\n')
        xml_file.write('    <source>\n')
        xml_file.write('        <database>Unknown</database>\n')
        xml_file.write('    </source>\n')
        xml_file.write('    <size>\n')
        xml_file.write('        <width>' + str(width) + '</width>\n')
        xml_file.write('        <height>' + str(height) + '</height>\n')
        xml_file.write('        <depth>3</depth>\n')
        xml_file.write('    </size>\n')
        xml_file.write('    <segmented>0</segmented>\n')
        if flag == 'True':
            for number in range(0, int(objectNum)):
                labelType = useLine.split(' ')[4 + number*5]
                xml_file.write('    <object>\n')
                xml_file.write('        <name>' + labelName[int(labelType)] + '</name>\n')
                xml_file.write('        <pose>Unspecified</pose>\n')
                xml_file.write('        <truncated>0</truncated>\n')
                xml_file.write('        <difficult>0</difficult>\n')
                xml_file.write('        <bndbox>\n')
                xml_file.write('            <xmin>' + str(useLine.split(' ')[number*5+5]) + '</xmin>\n')
                xml_file.write('            <ymin>' + str(useLine.split(' ')[number*5+6]) + '</ymin>\n')
                xml_file.write('            <xmax>' + str(useLine.split(' ')[number*5+7]) + '</xmax>\n')
                xml_file.write('            <ymax>' + str(useLine.split(' ')[number*5+8].replace('\n', '')) + '</ymax>\n')
                xml_file.write('        </bndbox>\n')
                xml_file.write('    </object>\n')
    #            xml_file.write('    </result>\n')
    #    else:
        xml_file.write('</annotation>\n') 
        xml_file.close()      



def parse_args():
    '''parse args'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--gpu_id', type=int, default=1, help='gpu id')
    parser.add_argument('--labelmap_file',
                        default='labelmapst2.prototxt')
    parser.add_argument('--model_def',
                        default='models/jiaoTongDeploy.prototxt')
    parser.add_argument('--image_resize', default=1000, type=int)
    parser.add_argument('--model_weights',
                        default='models/jiGUangGaoSuJiaoChaYanZheng/jiGuangGaoSuJCYZ_iter_3100_lost1718.caffemodel')
    parser.add_argument('--image_file', default='examples/images/jiGuangGaoSuTest.txt')
    return parser.parse_args()

if __name__ == '__main__':
    main(parse_args())
