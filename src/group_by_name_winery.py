import MySQLdb
import sys
import getpass
def get_all(cur):
    print "waiting to exec sql;"
    count = cur.execute(
        'select name, winery, source, wine_img\
        from wine2;')
    print 'exec sql finished!'
    assert(count > 0)
    result = cur.fetchall();
    return result

def group(re):
    d = {}
    for r in re:
        if (r[0], r[1]) not in d:
            d[(r[0], r[1])] = 0
        d[(r[0], r[1])] += 1
    return d

def insert_to_db(cur, d):
    print "insert to db"
    for key in d:
        sql =  'insert into name_winery_count (name, winery, num)\
            values (%s, %s, %s);'
        #.format(key[0].encode('utf8').replace("'", "\\'").replace('"', '\\"'), key[1].encode('utf8').replace("'", "\\'").replace('"', '\\"'), d[key])
        # print sql
        cur.execute(sql, [key[0], key[1], d[key]])
    print "finish inserting to db"

try:
    password = getpass.getpass('Enter password: ')
    conn = MySQLdb.connect(host='127.0.0.1', 
            user='root', passwd=password,
            db='imagedb', port=3306, charset='utf8')
    cur = conn.cursor()
    result = get_all(cur)
    d = group(result)
    insert_to_db(cur, d)
    conn.commit()
    cur.close()
    conn.close()
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
