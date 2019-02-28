# -*- coding: utf-8 -*-
import sys,time,random,json,re
reload(sys)
sys.setdefaultencoding('utf8')
from flask import current_app
from . import getmdsapi
from .. import db
from .. import cache
from ..models import *

def LoadyxZtree():
    RootName = current_app.config.get('GAMECHINESENAME')
    yxZtree_nodes = []
    yxZtree_nodes.append({"id":"g_0","pId":"-1","name":RootName})
    AllAgent = json.loads(cache.get('all_plats'))
    AllPlatAlias = {}
    for u in range(len(AllAgent)):
        platId = "p_%s" %(str(AllAgent[u]['platformId']))
        platAlias = AllAgent[u]['platformAlias']
        AllPlatAlias[platAlias] = []
        yxZtree_nodes.append({"id":platId,"pId":"g_0","name":platAlias})
    AllServerMsg = getmdsapi.getallserver()
    if int(AllServerMsg['code']) == 0:
        AllServer = AllServerMsg['Msg']
        cache.delete('all_servers')
        getmdsapi.cache_allservers(json.dumps(AllServer))
        for u in range(len(AllServer)):
            #合服的区服
            if True:#str(AllServer[u]['isCombined']).upper() == "FALSE":
                serverId = str(AllServer[u]['serverId'])
                platfromAlias = AllServer[u]['platformAlias']
                platformId = str(AllServer[u]['platformId'])
                ispublic = re.match(".*public$",platfromAlias)
                if ispublic:
                    AllPlatAlias['pubserver'].append({"serverId":int(serverId),"platformId":platformId,"platformAlias2":platfromAlias})
                else:
                    AllPlatAlias[platfromAlias].append({"serverId":int(serverId),"platformId":platformId,"platformAlias2":platfromAlias})
        for key in AllPlatAlias:
            for p in range(len(AllPlatAlias[key])):
                AllPlatAlias[key].sort()
                serverId = AllPlatAlias[key][p]['serverId']
                platfromAlias = AllPlatAlias[key][p]['platformAlias2']
                pId = "p_%s" %(AllPlatAlias[key][p]['platformId'])
                name = "%s %s服" %(platfromAlias,serverId)
                yxZtree_nodes.append({"id":"9999","serverId":str(serverId),"pId":pId,"platformAlias":platfromAlias,"name":name})
                
        cache.delete('Ztree_nodes')
        getmdsapi.cache_ztree(json.dumps(yxZtree_nodes))