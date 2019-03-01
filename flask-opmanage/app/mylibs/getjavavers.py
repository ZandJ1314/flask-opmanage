#!/usr/bin/evn python
# coding:utf-8

import MySQLdb
from operator import itemgetter
from itertools import *

MDSHOST = 'molongdb.mysql.rds.aliyuncs.com'
MDSPORT = 3808
MDSUSER = 'rxfsmds_r'
MDSPASS = 'Ns4RshFTvX7wd'
MDSDBNAME = 'rxfs_mds'

def formatString(verList):
    resultValue = ""
    d = {}
    for i in  range(len(verList)):
        d.setdefault(verList[i]['agent'],[]).append(int(verList[i]['zone']))
    for key in d:
        d[key].sort()
        resultValue = resultValue + "%s:" %(key)
        for k, g in groupby(enumerate(d[key]), lambda (i, x): i - x):
            ret = map(itemgetter(1), g)
            if len(ret) > 1:
                resultValue = resultValue + "%s-%s," %(str(ret[0]), str(ret[-1]))
            elif len(ret) == 1:
                resultValue = resultValue + "%s," %(str(ret[0]))
        resultValue = resultValue.rstrip(',') + "<br>"
    return resultValue.rstrip("<br>")

def getinfo():
    verJson = {}
    ResultListVer = []
    try:
        conn = MySQLdb.connect(host=MDSHOST, port=MDSPORT, user=MDSUSER, passwd=MDSPASS, db=MDSDBNAME, charset="utf8")
        cursor = conn.cursor()
        sql = "SELECT platformAlias,serverId, javaver,javaversiontype FROM mds_server WHERE serverId=iszone and isDeleted=0 and isCombined=0 ORDER BY platformAlias,serverId;"
        cursor.execute(sql)
        sqlresult = cursor.fetchall()
    except:
        return ResultListVer
    cursor.close()
    conn.close()

    for i in sqlresult:
        versionString = i[3] + '_' + i[2]
        verJson[versionString] = []

    for i in sqlresult:
        versionString = i[3] + '_' + i[2]
        value = {'agent': i[0], 'zone': i[1]}
        verJson[versionString].append(value)

    allTotal = 0
    for key in verJson:
        allTotal = allTotal + len(verJson[key])
        formatStringResult = formatString(verJson[key])
        ResultListVer.append({"version": key, "zones": formatStringResult, "total": str(len(verJson[key]))})

    return ResultListVer