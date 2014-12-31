import MySQLdb
import sys
import getpass
from wine_utils import *

def get_vaild(cur):
    sql = 'select name, winery, num from name_winery_count where num > 10';
    count = cur.execute(sql)
    assert(count > 0)
    result = cur.fetchall();
    return result

def get_by_name_winery(cur, name, winery):
    sql = 'select name, winery, source, wine_img\
        from wine2\
        where name = %s\
        and winery = %s;'
    count = cur.execute(sql, [name, winery])
    assert(count > 0)
    result = cur.fetchall();
    return result

try:
    password = getpass.getpass('Enter password: ')
    conn = MySQLdb.connect(host='127.0.0.1', 
            user='root', passwd=password,
            db='imagedb', port=3306, charset='utf8')
    cur = conn.cursor()
    vaild = get_vaild(cur)
    data_path = '/home/tuke/raid/data/wine_deepid'
    for name, winery, num in vaild:
        data = get_by_name_winery(cur, name, winery)
        download_from_data_server(data, "{}/{}_{}".format(data_path, name.replace('/', '\\').encode('utf8'), winery.encode('utf8')))
    cur.close()
    conn.close()
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
