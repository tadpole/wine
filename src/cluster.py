from wine_utils import *
from sklearn.cluster import *
import numpy as np
import matplotlib.pyplot as plt
import itertools

def minmax_distance(centers):
    re = 100000000.0
    for a, b in itertools.product(centers, centers):
        dis = np.sqrt(sum((a-b)**2))
        if dis == 0.0: continue
        if re > dis:
            re = dis
    return re

def get_vars(feature, labels, n):
    group = get_group(labels, n)
    means = np.array([])
    dis = []
    for g in group:
        f = feature[g]
        means = np.append(means, np.var(f, axis=0).mean())
    dis = np.array(dis)
    return means.mean()

if __name__ == '__main__':
    data = json.loads(open('data/features_0.json', 'r').read())
    feature = np.array(data['feature'])
    data_store = 'data/kmeans/'
    ns = range(20, 101, 10)
    vars = []
    diss = []
    for n in ns:
        kmeans = KMeans(n_clusters=n)
        print "training k-means with {} clusters".format(n)
        kmeans.fit(feature)
        labels = kmeans.labels_
        centers = kmeans.cluster_centers_
        var = get_vars(feature, labels, n)
        dis = minmax_distance(centers)
        vars.append(var)
        diss.append(dis)
        save_object(kmeans, "{}kmeans_{}".format(data_store, n))
        print "end training k-means with {} clusters\n\tvar = {}\n\tminmax distance = {}".format(n, var, dis)
    f, (ax1, ax2) = plt.subplots(1, 2)
    ax1.plot(ns, vars)
    ax1.set_title('variance')
    ax2.plot(ns, diss)
    ax2.set_title('min distance')
    plt.show()
