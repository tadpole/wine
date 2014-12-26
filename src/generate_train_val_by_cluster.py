from wine_utils import *
import os
import numpy as np
import sys
import random

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python {} total_num_clusters [cluster_num]".format(sys.argv[0])
        exit()
    n = int(sys.argv[1])
    kmeans_path = 'data/kmeans/kmeans_{}'.format(n)
    kmeans = load_object(kmeans_path)
    kmeans_labels = kmeans.labels_
    data = json.loads(open('data/features_0.json', 'r').read())
    name = np.array(data['name'])
    label_group = get_group(kmeans_labels, n)
    if len(sys.argv) == 3:
        cluster_num = int(sys.argv[2])
        draw_pic(name[label_group[cluster_num]], sample = True)
        plt.show()
        exit()
    data_path = 'data/cluster_caffe/cluster_{}'.format(n)
    if not os.path.exists(data_path):
        os.mkdir(data_path)
    train_path = data_path+'/train.txt'
    val_path = data_path+'/val.txt'
    train = open(train_path, 'w')
    val = open(val_path, 'w')
    p = 0.9
    for i in range(n):
        name_label = map(lambda x: "{} {}".format(x, i) , name[label_group[i]])
        random.shuffle(name_label)
        sl = int(len(name_label)*p)
        for l in name_label[:sl]:
            print >> train, l
        for l in name_label[sl:]:
            print >> val, l
    train.close()
    val.close()
