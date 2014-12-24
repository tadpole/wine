import sys
import numpy as np
import matplotlib.pyplot as plt
caffe_root = '/home/tuke/raid/tools/caffe/'
sys.path.insert(0, caffe_root + 'python')
import caffe
import json
import os
from matplotlib.ticker import MultipleLocator, FuncFormatter
import getopt
import random
from wine_utils import *

if __name__ == '__main__':
    wine_dir = caffe_root+'examples/wine/'
    image_path = '/home/tuke/raid/data/vaild_wine/'
    image_val_path = image_path+'val/'
    image_train_path = image_path+'train/'
    data_path = '/home/tuke/raid/wine/data/'
    data_val = data_path+'val.txt'
    data_train = data_path+'train.txt'
    train_label = map(lambda x: tuple(x.split()), open(data_train, 'r').readlines())
    val_label = map(lambda x: tuple(x.split()), open(data_val, 'r').readlines())
    labels = map(lambda x: (image_train_path+x[0], x[1]), train_label)+map(lambda x: (image_val_path+x[0], x[1]), val_label)
    ###############################
    net = init(wine_dir+'deploy_feature.prototxt', wine_dir+'wine_full_iter_80000.caffemodel', wine_dir+'wine_mean.npy')
    num = len(labels)
    f = {}
    names = map(lambda x: x[0], labels)
    la = map(lambda x: int(x[1]), labels)
    features = get_feature(net, names)
    f['name'] = names
    f['label'] = la
    f['feature'] = features.tolist()
    with open(data_path+'features_0.json', 'w') as da:
        da.write(json.dumps(f))
    print "done!"
