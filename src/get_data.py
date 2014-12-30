import MySQLdb
import hashlib
import time
from urllib import urlretrieve
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FuncFormatter
import sys
import getpass

def get_one_pic(cur, winery_name, prefix_name):
    count = cur.execute(
        "select name, wine_img from tbl_wine \
        where winery = '%s'\
        and wine_img <> ''\
        and name like '%s%%'\
        and id >= (select floor(RAND()*(select max(id) from tbl_wine)))\
        limit 1;" % (winery_name, prefix_name.replace("'", "\\'")));
    result = cur.fetchone();
    return result

def get_one_pic_by_name(cur, winery_name, name):
    count = cur.execute(
        "select name, wine_img from tbl_wine \
        where winery = '%s'\
        and wine_img <> ''\
        and name = '%s'\
        and id >= (select floor(RAND()*(select max(id) from tbl_wine)))\
        limit 1;" % (winery_name, name.encode('utf8').replace("'", "\\'")));
    result = cur.fetchone();
    return result

def get_prefix_pic(cur, winery_name, prefix_name):
    count = cur.execute(
        "select count(*), name \
        from tbl_wine \
        where winery = '%s'\
        and wine_img <> ''\
        and name like '%s%%'\
        group by name \
        order by count(*) desc \
        limit 10;" % (winery_name, prefix_name));
    result = cur.fetchall()
    for num, name in result:
        print num, name
    return [get_one_pic_by_name(cur, winery_name, name) for num, name in result]

def get_mut_prefix(cur, winery_name):
    count = cur.execute(
        "select name \
        from tbl_wine \
        where winery = '%s'\
        and name <> ''\
        and wine_img <> ''\
        order by name;" % winery_name);
    result = cur.fetchall();
    prefix =  result[0][0].encode('utf8')
    num = 1
    prefixs = []
    for i in range(1, len(result)):
        s = result[i][0].encode('utf8')
        if s.startswith(prefix):
            num += 1
        else:
            prefixs.append((num, prefix))
            prefix = s
            num = 1
    prefixs.sort(lambda x, y: y[0]-x[0])
    return prefixs[:10]

def get_by_winery(cur, winery_name):
    count=cur.execute(
        "select count(*), substring(name, 1, length(SUBSTRING_INDEX(name,' ',1))) \
        from tbl_wine \
        where winery = '%s'\
        and wine_img <> ''\
        group by substring(name, 1, length(SUBSTRING_INDEX(name,' ',1))) \
        order by count(*) desc \
        limit 10;" % winery_name);
    result = cur.fetchall()
    return result

http_head = 'http://192.168.1.114/'
http_head += 'vivino/'
#http_head += 'wine-world/'
try:
    m = hashlib.md5()
    plt.figure(figsize=(18, 8))
    password = getpass.getpass('Enter password: ')
    conn = MySQLdb.connect(host='192.168.1.114', 
            user='yunshitu', passwd=password, 
            db='imagedb', port=3306, charset='utf8')
    cur = conn.cursor()

    if len(sys.argv) < 2:
        print "Usage: python get_data.py winery_name [prefix_name]"
        exit(1)
    elif len(sys.argv) == 2:
        winery_name = sys.argv[1]#'Louis Jadot'
        result = get_mut_prefix(cur, winery_name)
        for num, prefix_name in result:
            print num, prefix_name
        print ", ".join(map(lambda x: x[1], result))
        for i in range(len(result)):
            prefix_name = result[i][1]
            wine_img = get_one_pic(cur, winery_name, prefix_name)
            wine_img = wine_img[1]
            print wine_img
            m.update(wine_img)
            local_file = '/tmp/get_data_'+m.hexdigest()+'.jpg'
            urlretrieve(http_head+wine_img, local_file)
            try:
                pic = plt.imread(local_file)
                plt.subplot(2, 5, i+1)
                plt.imshow(pic)
                plt.gca().xaxis.set_major_locator(MultipleLocator(1000))
                plt.gca().yaxis.set_major_locator(MultipleLocator(1000))
                plt.title(prefix_name.decode('utf8'))
            except IOError, e:
                print "IOError"
    elif len(sys.argv) == 3:
        winery_name = sys.argv[1]#'Louis Jadot'
        prefix_name = sys.argv[2]
        result = get_prefix_pic(cur, winery_name, prefix_name)
        for i in range(len(result)):
            if result[i] is None:
                continue
            wine_img = result[i][1]
            print wine_img
            name = result[i][0].encode('utf8')
            m.update(wine_img)
            local_file = '/tmp/get_data_'+m.hexdigest()+'.jpg'
            urlretrieve(http_head+wine_img, local_file)
            try:
                pic = plt.imread(local_file)
                plt.subplot(2, 5, i+1)
                plt.imshow(pic)
                plt.gca().xaxis.set_major_locator(MultipleLocator(1000))
                plt.gca().yaxis.set_major_locator(MultipleLocator(1000))
            except IOError, e:
                print "IOError"
    plt.show()
    cur.close()
    conn.close()
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
