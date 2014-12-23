import matplotlib.pyplot as plt
import os
import shutil
import random

train_path = '/home/tuke/raid/data/vaild_wine/train/'
val_path = '/home/tuke/raid/data/vaild_wine/val/'
origin_data_path = '/home/tuke/raid/data/wine/'
synset = open('synsets.txt', 'w')
train = open('train.txt', 'w')
val = open('val.txt', 'w')
p = 0.9
f = open('pic_num.txt', 'r')
data = []
for line in f:
    l = line.split("\t")
    data.append((int(l[0].strip()), l[1].strip(), int(l[2].strip())))
#plt.hist(map(lambda x: x[2], data), 40, range=[0, 2000])
#plt.show()
data.sort(lambda x, y: y[2]-x[2])
d = data[:50]
i = 0
for id, name, num in d:
    train_dir = train_path+'w'+str(i)
    os.mkdir(train_dir)
    origin_data_dir = origin_data_path+'w'+str(id)
    files = os.listdir(origin_data_dir)
    random.shuffle(files)
    print >> synset, name
    if len(files) >= 400:
        files = files[:400]
    sl = int(len(files)*p)
    for file in files[:sl]:
        f_path = origin_data_dir+'/'+file
        shutil.copy(f_path, train_dir)
        print >> train, "{}/{} {}".format('w'+str(i), file, i)
    for file in files[sl:]:
        f_path = origin_data_dir+'/'+file
        shutil.copy(f_path, val_path)
        print >> val, "{} {}".format(file, i)
    i += 1
