import csv
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FuncFormatter
def get_labels(val_file):
    re = []
    for lines in open(val_file, 'r'):
        ls = lines.split()
        index =  int(ls[1])
        if len(re) <= index:
            re.append([])
        re[index].append(ls[0])
    return re
def draw_pic(files):
    plt.figure(figsize=(18, 8))
    num = min(files, 10)
    fs = random.sample(files, num)
    for i in range(num):
        try:
            pic = plt.imread(fs[i])
            plt.subplot(2, 5, i+1)
            plt.imshow(pic)
            plt.gca().yaxis.set_major_locator(MultipleLocator(1000))
            plt.gca().xaxis.set_major_locator(MultipleLocator(1000))
        except IOError, e:
            print "IOError"
    plt.show()

data_path = '/home/tuke/raid/data/vaild_wine/val/'
synset_path = '/home/tuke/raid/wine/'
val_file = synset_path+'val.txt'
synset_file = synset_path+'synsets.txt'
synset = map(lambda x: x.strip(), open(synset_file, 'r').readlines())
reader = csv.reader(open('predict_result.txt'))
data = []
for i, w, p, r in reader:
    data.append((int(i), w, float(p), float(r)))
id = map(lambda x: x[0], data)
winery = map(lambda x: x[1], data)
precision = np.array(map(lambda x: x[2], data))
recall = np.array(map(lambda x: x[3], data))
'''
plt.figure(1)
plt.subplot(121)
plt.hist(precision)
plt.title('precision')
plt.subplot(122)
plt.hist(recall)
plt.title('recall')
plt.show()
'''
data_labels = get_labels(val_file)
index1 = precision.argmin()
index2 = recall.argmin()
index3 = precision.argmax()
index4 = recall.argmax()
print "min precision:\t{}\t{}".format(index1, precision[index1])
print "min recall:\t{}\t{}".format(index2, recall[index2])
print 'max precision:\t{}\t{}'.format(index3, precision[index3])
print "max recall:\t{}\t{}".format(index4, recall[index4])
'''
draw_pic(map(lambda x: data_path+x, data_labels[index1]))
draw_pic(map(lambda x: data_path+x, data_labels[index2]))
draw_pic(map(lambda x: data_path+x, data_labels[index3]))
draw_pic(map(lambda x: data_path+x, data_labels[index4]))
'''
index = precision.argsort()[-1:-21:-1]
print index
print precision[index]
