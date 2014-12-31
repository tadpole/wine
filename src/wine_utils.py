import sys
import numpy as np
import matplotlib.pyplot as plt
caffe_root = '/home/tuke/raid/tools/caffe/'
sys.path.insert(0, caffe_root + 'python')
import caffe
import json
import os
from matplotlib.ticker import MultipleLocator, FuncFormatter
from urllib import urlretrieve
import random
import pickle

def init(deploy, caffemodel, mean):
    '''init caffe'''
    net = caffe.Net(deploy, caffemodel)
    net.set_phase_test()
    net.set_mean('data', np.load(mean))
    net.set_channel_swap('data', (2,1,0))
    net.set_raw_scale('data', 255.0)
    return net

def get_feature(net, pics):
    '''get output of caffe'''
    ims = map(lambda pic: caffe.io.load_image(pic), pics)
    out = net.forward_all(data=np.asarray(map(lambda im: net.preprocess('data', im), ims)))
    # return map(lambda d: map(lambda x: float(x[0][0]), d), out['ip1'])
    return np.squeeze(out[net.outputs[0]])

def draw_pic(files, titles = [""]*10, sample = False):
    '''draw 10 pictures in one screen'''
    plt.figure(figsize=(18, 8))
    num = min(len(files), 10)
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
    '''save python object'''
    with open(name, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def load_object(name):
    '''load python object'''
    with open(name, 'rb') as input:
        return pickle.load(input)

def get_group(labels, n):
    '''get group by same element'''
    group = [[] for i in range(n)]
    for i, l in enumerate(labels):
        group[l].append(i)
    return group

def check_img(f):
    '''check whether an image is vaild'''
    try:
        pic = plt.imread(f)
        return True
    except IOError, e:
        return False
    except RuntimeError, e:
        return False

def download_from_data_server(result, data_dir):
    '''download data from data-server'''
    http_head = 'http://192.168.1.115/'
    num = 0
    for name, winery, source, wine_img in result:
        remote_file = http_head+source+'/'+wine_img
        # data_dir = '{}/{}_{}'.format(data_path, name, winery)
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        local_file = '{}/{}'.format(data_dir, wine_img.split("/")[-1])
        if os.path.exists(local_file):
            continue
        urlretrieve(remote_file, local_file)
        if not check_img(local_file):
            os.remove(local_file)
        else:
            num += 1
    return num

