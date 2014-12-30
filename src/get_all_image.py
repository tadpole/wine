import MySQLdb
import hashlib
import time
from urllib import urlretrieve
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FuncFormatter
import sys
import csv
import os
import getpass

def get_by_winery(cur, winery):
    count = cur.execute(
        'select name, source, wine_img\
        from tbl_wine\
        where winery = "{}"\
        and wine_img <> ""\
        and name <> "";'.format(winery))
    assert(count > 0)
    result = cur.fetchall();
    return result

def get_by_prefix(cur, winery, prefix_name):
    count = cur.execute(
        'select name, source, wine_img\
        from tbl_wine\
        where winery = "{}"\
        and name like "{}%"\
        and wine_img <> ""\
        and name <> "";'.format(winery, prefix_name))
    assert(count > 0)
    result = cur.fetchall();
    return result

def get_by_name(cur, winery, name):
    count = cur.execute(
        'select name, source, wine_img\
        from tbl_wine\
        where winery = "{}"\
        and name = "{}"\
        and wine_img <> ""\
        and name <> "";'.format(winery, name))
    assert(count > 0)
    result = cur.fetchall();
    return result

def check_img(f):
    try:
        pic = plt.imread(f)
        return True
    except IOError, e:
        return False

#http_head += 'wine-world/'
http_head = 'http://192.168.1.114/'
csv_file = 'synsets.csv'
data_path = '/home/tuke/raid/data/wine/'
data_dir = ""

def do(result):
    num = 0
    for name, source, wine_img in result:
        remote_file = http_head+source+'/'+wine_img
        local_file = '{}/{}.jpg'.format(data_dir, wine_img.split("/")[-1])
        if os.path.exists(local_file):
            continue
        urlretrieve(remote_file, local_file)
        if not check_img(local_file):
            os.remove(local_file)
        else:
            num += 1
    return num

try:
    password = getpass.getpass('Enter password: ')
    conn = MySQLdb.connect(host='192.168.1.114', 
            user='yunshitu', passwd=password, 
            db='imagedb', port=3306, charset='utf8')
    cur = conn.cursor()
    reader = csv.reader(open(csv_file))
    for id, winery, prefix_names, names, number  in reader:
        if id == 'id':
            continue
        data_dir = data_path+'w'+id
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        num = 0
        if prefix_names == "" and names == "":
            result = get_by_winery(cur, winery)
            num += do(result)
        if prefix_names != "":
            prefix_names = prefix_names.split(",")
            for prefix_name in prefix_names:
                prefix_name = prefix_name.strip()
                if prefix_name == "":
                    continue
                result = get_by_prefix(cur, winery, prefix_name)
                num += do(result)
        if names != "":
            names = names.split(",")
            for name in names:
                name = name.strip()
                if name == "":
                    continue
                result = get_by_name(cur, winery, name)
                num += do(result)
        print id, "\t", winery, "\t", num
    cur.close()
    conn.close()
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
