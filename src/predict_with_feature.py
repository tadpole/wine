from get_feature import *
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
def get_labels(val_file):
    re = []
    for lines in open(val_file, 'r'):
        ls = lines.split()
        index =  int(ls[1])
        if len(re) <= index:
            re.append([])
        re[index].append(ls[0])
    return re
train_features_file = 'data/train_features.npy'
val_features_file = 'data/features.npy'
data_path = '/home/tuke/raid/data/vaild_wine/'
train_features = np.load(train_features_file)
val_features = np.load(val_features_file)
val_label = []#np.array(map(lambda x: tuple(x.split()), open('val.txt', 'r').readlines()))
val_keys = []
for lines in open('val.txt', 'r'):
    ls = lines.split()
    val_label.append(int(ls[1]))
    val_keys.append(ls[0])
train_label = []#np.array(map(lambda x: tuple(x.split()), open('train.txt', 'r').readlines()))
train_keys = []
for lines in open('train.txt', 'r'):
    ls = lines.split()
    train_label.append(int(ls[1]))
    train_keys.append(ls[0])
train_label = np.array(train_label)
val_label = np.array(val_label)
train_keys = np.array(train_keys)
val_keys = np.array(val_keys)
re = {}
for i in range(len(val_keys)):
    label = int(val_label[i])
    if label not in re:
        re[label] = []
    indexs = knn(val_features[i], train_features, 10)
    nns = train_label[indexs].tolist()
    re[label].append(max(nns, key=nns.count))
total_category = 50
synset = map(lambda x: x.strip(), open('synsets.txt', 'r').readlines())
dnums = dict(zip(range(total_category), [0]*total_category))
accs = []
for i in range(total_category):
    predict_re = re[i]
    acc = len(filter(lambda x: x == i, predict_re))
    accs.append(acc)
    for j in predict_re: dnums[j] +=1
for i in range(total_category):
    recall = float(accs[i])/dnums[i]
    precission = float(accs[i])/len(re[i])
    print "{},{},{},{}".format(i, synset[i], precission, recall)

print "total precission: {}".format(float(sum(accs))/len(val_label))
