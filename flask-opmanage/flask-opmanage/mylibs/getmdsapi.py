import urllib,urllib2,time,json,random,traceback,StringIO,gzip,base64
from hashlib import md5
from flask import current_app
from .. import cache

@cache.cached(timeout=31536000,key_prefix='all_plats')
def cache_plats(allplats):
    return allplats

@cache.cached(timeout=31536000,key_prefix='Ztree_nodes')
def cache_ztree(ztreeNode):
    return ztreeNode

@cache.cached(timeout=31536000,key_prefix='all_servers')
def cache_allservers(allservers):
    return allservers



def getagent():
    interface = "http://mgoas.mlwanwan.com/mgoas/interface/platformList.action"
    sign = current_app.config.get('MDSSIGN')
    gameId = current_app.config.get('GAMEID')
    systemId = current_app.config.get('SYSTEMID')
    local_time = int(time.time()) * 1000
    m = md5()
    m.update(sign+str(local_time))
    securSign = m.hexdigest()
    postDict = {"gameId":gameId,"systemId":systemId,"time":local_time,"sign":securSign.upper()}
    postData = urllib.urlencode(postDict)
    try:
        AllPlat = []
        req = urllib2.Request(interface,postData)
	print interface,postData
        #req.add_header('Host','mds.mlwanwan.com')
        resp = urllib2.urlopen(req)
        respJson = json.loads(resp.read())
        if respJson['result'] == "true":
            platformList = respJson['platformList']
            for i in range(len(platformList)):
                platform_id =  platformList[i]['id']
                platform_alias = platformList[i]['platformAlias']
                platform_configid = platformList[i]['configId']
                platform_gamealias = platformList[i]['gameAlias']
                platform_gameid = platformList[i]['gameId']
                platform_name = platformList[i]['platformName']
                AllPlat.append({"platformId":platform_id,"platformAlias":platform_alias,"configId":platform_configid,"gameAlias":platform_gamealias,"gameId":platform_gameid,"platformName":platform_name})
            return {"code":"0","Msg":AllPlat}
        else:
            current_app.logger.error(json.dumps(respJson))
            return {"code":"6"}
    except:
        errorlog = traceback.format_exc()
        current_app.logger.error(errorlog)
        return {"code":"5"}

def getallserver():
    interface = "http://mgoas.mlwanwan.com/mgoas/interface/allServerByGameId.action"
    sign = current_app.config.get('MDSSIGN')
    gameId = current_app.config.get('GAMEID')
    systemId = current_app.config.get('SYSTEMID')
    local_time = int(time.time()) * 1000
    m = md5()
    m.update(sign+str(local_time))
    securSign = m.hexdigest()
    postDict = {"gameId":gameId,"systemId":systemId,"time":local_time,"sign":securSign.upper()}
    postData = urllib.urlencode(postDict)
    try:
        req = urllib2.Request(interface,postData)
        #req.add_header('Host','mds.mlwanwan.com')
        resp = urllib2.urlopen(req)
        respJson = json.loads(resp.read())
        if respJson['result'] == "true":
            decodeResult = base64.decodestring(respJson['serverListStr'])
            buf = StringIO.StringIO(decodeResult.encode("ISO-8859-1"))
            f = gzip.GzipFile(fileobj=buf)
            serverData = f.read().decode("utf-8")
            f.close()
            return {"code":"0","Msg":json.loads(serverData)}
        else:
            current_app.logger.error(json.dumps(respJson))
            return {"code":"6"}
    except:
        errorlog = traceback.format_exc()
        current_app.logger.error(errorlog)
        return {"code":"5"}


def getallserverTodict():
    AllServerInfoMsg = getallserver()
    serversTodict = {}
    openingNum = 0
    if int(AllServerInfoMsg['code']) == 0:
        AllServerInfo = AllServerInfoMsg['Msg']
        for i in range(len(AllServerInfo)):
            DictKey = "%s_%s" %(AllServerInfo[i]['platformAlias'],AllServerInfo[i]['serverId'])
            serversTodict[DictKey] = AllServerInfo[i]
            try:
                dbName = AllServerInfo[i]['gameDBName']
            except:
                openingNum = openingNum + 1
        return {"code":"0","Msg":serversTodict,"openingNum":openingNum}
    else:
        return {"code":"7","Msg":"get server error"}



def insertMds(serverInfo):
    interface = "http://mgoas.mlwanwan.com/mgoas/interface/openServers.action"
    sign = current_app.config.get('MDSSIGN')
    gameId = current_app.config.get('GAMEID')
    systemId = current_app.config.get('SYSTEMID')
    local_time = int(time.time()) * 1000
    m = md5()
    m.update(sign+str(local_time))
    securSign = m.hexdigest()
    postDict = {"gameId":gameId,"systemId":systemId,"time":local_time,"sign":securSign.upper(),"serverListStr":json.dumps(serverInfo)}
    current_app.logger.error(json.dumps(postDict))
    postData = urllib.urlencode(postDict)
    #current_app.logger.error(interface, postData)
    try:
        req = urllib2.Request(interface,postData)
        #req.add_header('Host','mds.mlwanwan.com')
        resp = urllib2.urlopen(req)
        respStr = resp.read()
        current_app.logger.error("insert mds result : %s" %(respStr))
    except:
        errorlog = traceback.format_exc()
        current_app.logger.error(errorlog)



