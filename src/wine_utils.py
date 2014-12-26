import sys
import numpy as np
import matplotlib.pyplot as plt
caffe_root = '/home/tuke/raid/tools/caffe/'
sys.path.insert(0, caffe_root + 'python')
import caffe
import json
import os
from matplotlib.ticker import MultipleLocator, FuncFormatter
import random
import pickle

def init(deploy, caffemodel, mean):
    net = caffe.Net(deploy, caffemodel)
    net.set_phase_test()
    net.set_mean('data', np.load(mean))
    net.set_channel_swap('data', (2,1,0))
    net.set_raw_scale('data', 255.0)
    return net

def get_feature(net, pics):
    ims = map(lambda pic: caffe.io.load_image(pic), pics)
    out = net.forward_all(data=np.asarray(map(lambda im: net.preprocess('data', im), ims)))
    # return map(lambda d: map(lambda x: float(x[0][0]), d), out['ip1'])
    return np.squeeze(out[net.outputs[0]])

def draw_pic(files, titles = [""]*10, sample = False):
    plt.figure(figsize=(18, 8))
    num = min(files, 10)
    if sample:
        fs = random.sample(files, num)
    else:
        fs = files
    for i in range(num):
        try:
            pic = plt.imread(fs[i])
            plt.subplot(2, 5, i+1)
            plt.imshow(pic)
            plt.title(titles[i])
            plt.gca().yaxis.set_major_locator(MultipleLocator(1000))
            plt.gca().xaxis.set_major_locator(MultipleLocator(1000))
            plt.setp(plt.gca().get_xticklabels(), visible=False)
            plt.setp(plt.gca().get_yticklabels(), visible=False)
        except IOError, e:
            print "IOError"

def save_object(obj, name):
    with open(name, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def load_object(name):
    with open(name, 'rb') as input:
        return pickle.load(input)
