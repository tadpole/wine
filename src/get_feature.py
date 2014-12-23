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

def knn(sample, features, k):
    feature_size = features.shape[0]
    diffMat = np.tile(sample,(feature_size,1))-features
    sqDiffMat = diffMat**2
    sqDistances= sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()
    return sortedDistIndicies[:k]

def draw_pic(files, titles, sample = False):
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
        except IOError, e:
            print "IOError"

def get_index_by(val_label, cate):
    re = []
    for index, label in enumerate(val_label):
        if cate == int(label[1]):
            re.append(index)
    return re


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "id")
    isWine = True
    isVal = True
    for opt, val in opts:
        if opt == '-i':
            isWine = False
        elif opt == '-d':
            isVal = False
    if isWine:
        net = init(caffe_root+'examples/wine/deploy_feature.prototxt', caffe_root+'examples/wine/wine_full_iter_80000.caffemodel', caffe_root+'examples/wine/wine_mean.npy')
        features_file = 'features.npy'
    else:
        net = init(caffe_root+'models/bvlc_reference_caffenet/deploy_feature.prototxt', caffe_root+'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel', caffe_root+'python/caffe/imagenet/ilsvrc_2014_mean.npy')
        features_file = 'features_imagenet.npy'
    if isVal:
        data_path = '/home/tuke/raid/data/vaild_wine/val/'
        train_val_file = 'val.txt'
    else:
        data_path = '/home/tuke/raid/data/vaild_wine/train/'
        train_val_file = 'train.txt'
        features_file = 'train_'+features_file
    data_label = map(lambda x: tuple(x.split()), open(train_val_file, 'r').readlines())
    keys = map(lambda x: x[0], data_label)
    val_label = map(lambda x: tuple(x.split()), open('val.txt', 'r').readlines())
    if not os.path.exists(features_file):
        features = get_feature(net, map(lambda x: data_path+x, keys))
        np.save(features_file, features)
    features = np.load(features_file)
    ##################################################
    cate_index = 48
    val_index = random.sample(get_index_by(val_label, cate_index), 1)[0]
    val_index = 1000
    ###############################################
    pic_path = data_path+'../val/'+val_label[val_index][0]
    plt.figure(1)
    plt.imshow(caffe.io.load_image(pic_path))
    plt.title(val_label[val_index][1])
    f = get_feature(net, [pic_path])
    print val_label[val_index][1]
    indexs = knn(f, features, 10)
    files = map(lambda x: data_path+keys[x], indexs)
    labels = map(lambda x: data_label[x][1], indexs)
    print labels
    draw_pic(files, labels)
    if not isVal:
        this_cate = filter(lambda x: x[1]==val_label[val_index][1], data_label)
        print map(lambda x: x[1], this_cate)[:10]
        draw_pic(map(lambda x: data_path+x[0], this_cate), [""]*10, True)
    plt.show()
