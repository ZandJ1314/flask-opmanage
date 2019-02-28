# -*- coding: utf-8 -*-
import sys,time,random,json,traceback
reload(sys)
sys.setdefaultencoding('utf8')
import MySQLdb
import MySQLdb.cursors
from flask import current_app
from . import getmdsapi
from .. import db
from .. import cache
from ..models import *

def LoadMysqlSrcZtree():
    datasrcIP = current_app.config.get('DATASRCIP')
    datasrcPort = current_app.config.get('DATASRCPORT')
    datasrcUser = current_app.config.get('DATASRCUSER')
    datasrcPass = current_app.config.get('DATASRCPASS')
    datasrcZtree_nodes = []
    DBsList = []
    ResultMsg = {}
    datasrcZtree_nodes.append({"id":"0","pId":"-1","name":"%s:%s" %(datasrcIP,datasrcPort),"type":"instance"})
    try:
        conn = MySQLdb.connect(host=datasrcIP,port=int(datasrcPort),user=datasrcUser,passwd=datasrcPass,charset="utf8")
        cursor = conn.cursor()
        cursor.execute("show databases")
        AllDB = cursor.fetchall()
        for i in range(len(AllDB)):
            p = i + 1
            DBName = AllDB[i][0]
            if DBName == "information_schema":
                continue
            DBsList.append(DBName)
            conn.select_db(DBName)
            cursor = conn.cursor()
            cursor.execute("show tables")
            AllDBtables = cursor.fetchall()
            datasrcZtree_nodes.append({"id":str(p),"pId":"0","name":DBName,"type":"db","tablesTotal":str(len(AllDBtables))})
            for u in range(len(AllDBtables)):
                tableName = AllDBtables[u][0]
                datasrcZtree_nodes.append({"id":"9999","pId":str(p),"name":tableName,"type":"table","dbName":DBName})
            cursor.close()
        conn.close()
        ResultMsg['code'] = 0
        ResultMsg['tableTree'] = datasrcZtree_nodes
        ResultMsg['DbsList'] = DBsList
        return ResultMsg
    except:
        ResultMsg['code'] = 1
        return ResultMsg
        errorlog = traceback.format_exc()
        current_app.logger.error(errorlog)
    