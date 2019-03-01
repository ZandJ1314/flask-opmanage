#!/usr/bin/evn python
# coding:utf-8

import MySQLdb

MDSHOST = 'molongdb.mysql.rds.aliyuncs.com'
MDSPORT = 3808
MDSUSER = 'ywlhfsmds'
MDSPASS = '5akbI3fpHVo1u0HUXHzL'
MDSDBNAME = 'lhfs_mds'


def getinfo():
    verJson = {}
    ResultListVer = []
    try:
        conn = MySQLdb.connect(host=MDSHOST, port=MDSPORT, user=MDSUSER, passwd=MDSPASS, db=MDSDBNAME, charset="utf8")
        cursor = conn.cursor()
        sql = "SELECT CONCAT(platformAlias,':',serverId) as updateList, javaver,javaversiontype FROM mds_server WHERE serverId=iszone and isDeleted=0 and isCombined=0 ORDER BY platformAlias,serverId;"
        cursor.execute(sql)
        sqlresult = cursor.fetchall()
    except:
        return ResultListVer
    cursor.close()
    conn.close()

    for i in sqlresult:
        versionString = i[1] + '_' + i[2]
        verJson[versionString] = []

    for i in sqlresult:
        versionString = i[1] + '_' + i[2]
        verJson[versionString].append(i[0])

    for key in verJson:
        zones = ''
        for zone in verJson[key]:
            zones = zones + zone + '<br>'
        ResultListVer.append({'zones': zones, 'total': len(verJson[key]), 'version': key})

    return ResultListVer