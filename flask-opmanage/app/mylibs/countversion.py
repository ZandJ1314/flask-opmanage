#!/bin/env python
# -*- coding: utf-8 -*-
import sys,time,random,json,traceback
reload(sys)
sys.setdefaultencoding('utf8')
from flask import current_app
from flask.ext.login import current_user
from . import getmdsapi
from . import minitool
from .. import db
from ..models import *

def CountVer(serversList,countType):
    gameName = current_app.config.get('GAMENAME')
    ResultMsg = {}
    verJson = {}
    try:
        AllServerinfoMsg = getmdsapi.getallserverTodict()
        if int(AllServerinfoMsg['code']) == 0:
            AllServerInfoDict = AllServerinfoMsg['Msg']
            if int(AllServerinfoMsg['openingNum']) == 0:
                for i in range(len(serversList)):
                    platformAlias = serversList[i]['agent']
                    serverId = serversList[i]['zone']
                    plat_id = "%s_%s" %(platformAlias,serverId)
                    if str(AllServerInfoDict[plat_id]['isCombined']).upper() == "FALSE":
                        if countType == "datares":
                            if (platformAlias == "37" and int(serverId) < 14000) or (platformAlias != "37" and int(serverId) < 10000):
                                zoneSign_md5 = minitool.GetMd5(platformAlias+serverId+current_user.username+minitool.GetRandomString()+"planResUpdate")
                                zoneSign = "%s-%s-%s" %(zoneSign_md5,str(int(time.time())),minitool.GetRandomString())
                                versionString = AllServerInfoDict[plat_id]['rESVER']
                                verJson.setdefault(versionString,[]).append({
                                    "platformAlias":platformAlias,
                                    "serverId":serverId,
                                    "serverIp":AllServerInfoDict[plat_id]['serverIp'],
                                    "javaDir":AllServerInfoDict[plat_id]['javaDir'],
                                    "sign":zoneSign,
                                    "gameAlias":gameName,
                                    "from":"backend"
                                    })
                        elif countType == "javares":
                            versionString = AllServerInfoDict[plat_id]['javaversiontype']
                            verJson.setdefault(versionString,[]).append({
                                "platformAlias":platformAlias,
                                "serverId":serverId,
                                "serverIp":AllServerInfoDict[plat_id]['serverIp'],
                                "javaDir":AllServerInfoDict[plat_id]['javaDir']
                                })
                ResultMsg['code'] = 0
                ResultMsg['Msg'] = verJson
            else:
                ResultMsg['code'] = 5
        else:
            ResultMsg['code'] = 2
    except:
        ResultMsg['code'] = 3
        errorlog = traceback.format_exc()
        current_app.logger.error(errorlog)
    return ResultMsg
            
                        
                    
                
        
    
    
