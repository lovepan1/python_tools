#encoding=utf8
import os
import sys
import argparse
import numpy as np
from PIL import Image, ImageDraw
import cv2
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
        return result

def getRightBbox(resultBboxList, currentBbox, width, height):
    import numpy as np
    flag = True
    currentBboxXmin = int(round(currentBbox[0] * width))
    currentBboYmin = int(round(currentBbox[1] * height))
    currentBboxXmax = int(round(currentBbox[2] * width))
    currentBboxYmax = int(round(currentBbox[3] * height)) 
    currentBboxCon =  round(currentBbox[5])
    currentArea = (currentBboxXmax - currentBboxXmin) * (currentBboxYmax - currentBboYmin)
    for item in resultBboxList:
        xmin = int(round(item[0] * width))
        ymin = int(round(item[1] * height))
        xmax = int(round(item[2] * width))
        ymax = int(round(item[3] * height))
        area = (xmax - xmin)*(ymax - ymin)
        w = np.maximum(0.0, xmax - currentBboxXmin + 1) 
        h = np.maximum(0.0, currentBboxYmax - ymin + 1) 
        inter = w * h
        JaccardOverlap = inter / (currentArea + area - inter)
        if JaccardOverlap > 0.2:
            flag = False
            break
        else:
            continue
    return flag
   
def main(args):
    '''main '''
    detection = CaffeDetection(args.gpu_id,
                               args.model_def, args.model_weights,
                               args.image_resize, args.labelmap_file)
    imageFiles = open(args.image_file)    
    size = 0.3
    lastResult = []
    for line in imageFiles:
        line1 = line.replace('\n', '')
        filePath = line1.replace(' ', '')
        print "the last path is " + filePath
        imageName = filePath.split('/')[-1] 
        srcImg = cv2.imread(filePath)
        shape = srcImg.shape
        newXMin = int(shape[1] * 0.3)
        newYMin = int(shape[0] * 0.3)
        xMax = shape[1]
        yMax = shape[0]
        cropImg1 = srcImg[0:yMax - newYMin, newXMin:xMax]
        cropImg2 = srcImg[0:yMax - newYMin - newYMin, newXMin + newXMin:xMax]
        cv2.imwrite("examples/images/crop1_"+imageName, cropImg1)
        cv2.imwrite("examples/images/crop2_"+imageName, cropImg2)
        filePath2 = filePath.replace(imageName, 'crop1_' + imageName)
        filePath3 = filePath.replace(imageName, 'crop2_' + imageName)
        result = detection.detect(filePath)
        result2 = detection.detect(filePath2)
        result3 = detection.detect(filePath3)
        print 'result1 is'
        print result        
        print 'result2 is'
        print result2
        print 'result3 is'
        print result3
        img = Image.open(filePath)
        width, height = img.size
        print width, height
        draw = ImageDraw.Draw(img)
        for item in result:
            xmin = int(round(item[0] * width))
            ymin = int(round(item[1] * height))
            xmax = int(round(item[2] * width))
            ymax = int(round(item[3] * height))
            label = int(round(item[4]))
            conf = round(item[5])
            lastResult.append([xmin, ymin, xmax, ymax, label, conf])
            draw.rectangle([xmin, ymin, xmax, ymax], outline=(255, 0, 0))
            draw.text([xmin, ymin], item[-1] + str(item[-2]), (0, 0, 255))  
        for item2 in result2:
            xmin = int(round(item2[0] * width * 0.7)+ newXMin )
            ymin = int(round(item2[1] * height * 0.7))
            xmax = int(round(item2[2] * width * 0.7)+ newXMin )
            ymax = int(round(item2[3] * height * 0.7))
            label = int(round(item2[4]))
            conf = round(item2[5])
            if getRightBbox(lastResult, [xmin, ymin, xmax, ymax, label, conf], width, height):
                print 'result2'
                lastResult.append([xmin, ymin, xmax, ymax, label, conf])
                draw.rectangle([xmin, ymin, xmax, ymax], outline=(255, 0, 0))
                draw.text([xmin, ymin], item[-1] + str(item[-2]), (0, 0, 255))
        for item3 in result3:
            xmin = int(round(item3[0] * width * 0.4) + newXMin + newXMin)
            ymin = int(round(item3[1] * height * 0.4))
            xmax = int(round(item3[2] * width * 0.4) + newXMin + newXMin)
            ymax = int(round(item3[3] * height * 0.4))
            label = int(round(item3[4]))
            conf = round(item3[5])
            if getRightBbox(lastResult, [xmin, ymin, xmax, ymax, label, conf], width, height):
                print 'result3'
                lastResult.append([xmin, ymin, xmax, ymax, label, conf])
                draw.rectangle([xmin, ymin, xmax, ymax], outline=(255, 0, 0))
                draw.text([xmin, ymin], item[-1] + str(item[-2]), (0, 0, 255))
        os.remove(filePath2)
        os.remove(filePath3)
        img.save("resultImages/" + imageName)



def parse_args():
    '''parse args'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--gpu_id', type=int, default=0, help='gpu id')
    parser.add_argument('--labelmap_file',
                        default='labelmapst2.prototxt')
    parser.add_argument('--model_def',
                        default='models/huangMeiGaoSuModel/deploy.prototxt')
    parser.add_argument('--image_resize', default=512, type=int)
    parser.add_argument('--model_weights',
                        default='models/huangMeiGaoSuModel/huangMeiGaoSu_iter_2400.caffemodel')
    parser.add_argument('--image_file', default='examples/images/jiGuangGaoSuTest.txt')
    return parser.parse_args()

if __name__ == '__main__':
    main(parse_args())
