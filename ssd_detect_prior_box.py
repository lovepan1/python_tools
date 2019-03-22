import numpy as np
import matplotlib.pyplot as plt
import time
import matplotlib 

plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

# Make sure that caffe is on the python path:
caffe_root = '/home/lk/caffe_ssd/'  # this file is expected to be in {caffe_root}/examples
import os
os.chdir(caffe_root)
import sys
sys.path.insert(0, 'python')

import caffe
caffe.set_mode_cpu() 

from google.protobuf import text_format
from caffe.proto import caffe_pb2

# load PASCAL VOC labels
labelmap_file = 'labelmapDianLi.prototxt'
file = open(labelmap_file, 'r')
labelmap = caffe_pb2.LabelMap()
text_format.Merge(str(file.read()), labelmap)

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

model_def = 'models/dianLiSsdModel/deploy.prototxt'
model_weights = 'models/dianLiSsdModel/dianLi_iter__iter_12000.caffemodel'
net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)     # use test mode (e.g., don't perform dropout)

# input preprocessing: 'data' is the name of the input blob == net.inputs[0]
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2, 0, 1))
transformer.set_mean('data', np.array([104,117,123])) # mean pixel
transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

# set net to batch size of 1
image_resize = 512
net.blobs['data'].reshape(1,3,image_resize,image_resize)
image = caffe.io.load_image('/home/lk/caffe_ssd/examples/images/000034.jpg')
transformed_image = transformer.preprocess('data', image)
net.blobs['data'].data[...] = transformed_image
detections = net.forward()['detection_out'] 


det_label = detections[0,0,:,1]
det_conf = detections[0,0,:,2]
det_xmin = detections[0,0,:,3]
det_ymin = detections[0,0,:,4]
det_xmax = detections[0,0,:,5]
det_ymax = detections[0,0,:,6]
det_prior_idx = detections[0,0,:,7]

# Get detections with confidence higher than 0.6.
top_indices = [i for i, conf in enumerate(det_conf) if conf >= 0.3]# and conf <=0.5]

top_conf = det_conf[top_indices]
top_label_indices = det_label[top_indices].tolist()
top_labels = get_labelname(labelmap, top_label_indices)
top_xmin = det_xmin[top_indices]
top_ymin = det_ymin[top_indices]
top_xmax = det_xmax[top_indices]
top_ymax = det_ymax[top_indices]
top_prior_idx = det_prior_idx[top_indices] 

plt.imshow(image)
colors = plt.cm.hsv(np.linspace(0, 1, 21)).tolist()
currentAxis = plt.gca()
for i in xrange(2):
    xmin = int(round(top_xmin[i] * 300))
    ymin = int(round(top_ymin[i] * 300))
    xmax = int(round(top_xmax[i] * 300))
    ymax = int(round(top_ymax[i] * 300))
    score = top_conf[i]
    label = int(top_label_indices[i])
    label_name = top_labels[i]
    if label_name=='person' :
        prior_idx = int(top_prior_idx[i])
        display_txt = '%s: %.8f prior=%d (%d %d %d %d)'%(label_name,score,prior_idx,xmin,ymin,xmax,ymax)
        coords = (xmin, ymin), xmax-xmin+1, ymax-ymin+1
        color = colors[label]
        currentAxis.add_patch(plt.Rectangle(*coords, fill=False, edgecolor='g', linewidth=2))
        currentAxis.text(xmin, ymin, display_txt, bbox={'facecolor':'g', 'alpha':0.8})

idx = 2307 
img_width = 512
img_height = 512
priorbox = net.blobs['mbox_priorbox'].data[0,0,:] 
prior_bbox = priorbox[idx*4:(idx+1)*4] 
xmin = prior_bbox[0] * img_width
ymin = prior_bbox[1] * img_height
xmax = prior_bbox[2] * img_width
ymax = prior_bbox[3] * img_height
coords = (xmin, ymin), xmax - xmin + 1, ymax - ymin + 1
display_txt = 'prior=%d (%d %d %d %d) '%(idx,xmin,ymin,xmax,ymax)
currentAxis.add_patch(plt.Rectangle(*coords, fill=False, edgecolor='m', linewidth=2))
currentAxis.text(xmax, ymax+10, display_txt, bbox={'facecolor':'m', 'alpha':0.8})
