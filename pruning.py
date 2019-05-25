import tensorflow as tf
from tensorflow.python.framework import graph_util
from tensorflow.python import pywrap_tensorflow
import os
import numpy as np
model_dir = '/home/pcl/tensorflow1.12/YOLOv3_TensorFlow/checkpoint/'
checkpoint_path = os.path.join(model_dir, "pure_model")
f = open('node.txt', 'w')
w = open("weights.txt", "w")
w2 = open("spase_we.txt", "w")
tensor_name = "yolov3/yolov3_head/Conv_7/weights:0"
node_name = "yolov3/yolov3_head/Conv_7/weights"
# pb =
# checkpoint_path = os.path.join(model_dir, "resnet50_csv_18.pb")
reader = pywrap_tensorflow.NewCheckpointReader(checkpoint_path)
var_to_shape_map = reader.get_variable_to_shape_map()
graph = tf.get_default_graph()  # 获得默认的图
input_graph_def = graph.as_graph_def()  # 返回一个序列化的图代表当前的图
saver = tf.train.import_meta_graph(checkpoint_path + '.meta', clear_devices=True)
with tf.Session() as sess:
    # saver = tf.train.Saver()
    saver.restore(sess, checkpoint_path)
    # sess.run(tf.assign(tf.get_default_graph().get_tensor_by_name(node_name), prune_weight)
    print(sess.run(tf.get_default_graph().get_tensor_by_name(tensor_name)))
    def get_th(weight, pencentage=0.8):
        flat = np.reshape(weight, [-1])
        flat_list = sorted(map(abs, flat))
        return flat_list[int(len(flat_list) * pencentage)]


    def prune(weights, th):
        '''
        :param weights: weight Variable
        :param th: float value, weight under th will be pruned
        :return: sparse_weight
        '''
        shape = weights.shape
        # weight_arr = sess.run(weights)
        under_threshold = abs(weights) < th
        weights[under_threshold] = 0
        # tmp = weights
        # for i in range(len(shape) - 1):
        #     tmp = tmp[-1]
        # if tmp[-1] == 0:
        #     tmp[-1] == 0.01
        count = np.sum(under_threshold)
        print(count)
        return weights, ~under_threshold

    def change_weights(orignal_weight, prune_weight, node_name):
        '''
        because this weight only one layer ,so use weight not weights
        '''
        sess.run(tf.assign(orignal_weight, prune_weight))
        return orignal_weight

    sess.run([tf.global_variables_initializer(), tf.local_variables_initializer()])
    # saver = tf.train.Saver()
    # saver.restore(sess, checkpoint_path)
    # saver_to_restore.restore(sess, checkpoint_path)
    # weight = reader.get_tensor(node_name)
    weight = sess.run(tf.get_default_graph().get_tensor_by_name(tensor_name))
    # print("orignal weights is ",weight)
    # shape = weight.shape
    # print("orignal weights shape is",shape)
    yiwei_weight = sess.run(tf.reshape(weight, [-1]))
    # yiwei_weight = np.reshape(weight, [-1])
    print("yiwei_weights is ", yiwei_weight)
    # # # print("yiwei_weights is ", sess.run(yiwei_weights))
    # yiwei_shape = yiwei_weight.shape
    # # print("len yiwei_weights shape is ", len(yiwei_weight))
    # # print("orignal yiwei_weights shape is ", yiwei_shape)
    # for i in range(int(len(yiwei_weight) / 100)):
    #     w.write(str(yiwei_weight[i]) + ' ,')
    # under_threshold = abs(weights) < th
    # th = get_th(weight)
    # print("th is ", th)
    # #
    prune_weight, prune_counts = prune(weight, th)
    # prune_yiwei_weights = np.reshape(prune_weight, [-1])
    # for i in range(int(len(prune_yiwei_weights) / 100)):
    #     w2.write(str(prune_yiwei_weights[i]) + ' ,')
    # print(prune_counts)
    # sess.run(tf.assign(reader.get_tensor(node_name), prune_weight))
    # change_weights(reader.get_tensor(node_name), prune_weight, node_name)
    # for i in range(int(len(yiwei_weight) / 100)):
    #     w2.write(str(weight[i]) + ' ,')
    sess.run(tf.assign(tf.get_default_graph().get_tensor_by_name(tensor_name), prune_weight))
    for i in range(int(len(yiwei_weight) / 100)):
        w.write(str(yiwei_weight[i]) + ' ,')
