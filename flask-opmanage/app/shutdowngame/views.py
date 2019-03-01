# -*- coding: utf-8 -*-
import sys,time,random
reload(sys)
sys.setdefaultencoding('utf8')
from flask import render_template, redirect, request, url_for, flash, session,jsonify,json,current_app
from flask.ext.login import login_user, logout_user,current_user
from . import shutdowngame
from .. import db
from .. import cache
from ..models import *
from ..decorators import permission_required,login_required
from ..mylibs import sendsocket,getmdsapi,loadztree,minitool


def WriteUpdateLog(sign,updateCmd,gameName,platformAlias,serverId,serverName,zoneSign,version):
    operationlogZone = Operationlog()
    operationlogZone.batchSign = sign
    operationlogZone.cmd = updateCmd
    operationlogZone.gameName = gameName
    operationlogZone.platformAlias = platformAlias
    operationlogZone.sendDate = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    operationlogZone.sendTime = int(time.time())
    operationlogZone.sendUser = current_user.username
    operationlogZone.serverId = int(serverId)
    operationlogZone.serverName = serverName
    operationlogZone.sign = zoneSign
    operationlogZone.version = version
    db.session.add(operationlogZone)
    db.session.commit()

@shutdowngame.route("/shutdownmanage",methods=['GET','POST'])
@login_required
@permission_required("closeserver")
def shutdowngameManage():
    AllplatInfo = []
    Allplat = json.loads(cache.get('all_plats'))
    Ztree_nodes = cache.get('Ztree_nodes')
    for i in range(len(Allplat)):
        AllplatInfo.append(Allplat[i]['platformAlias'])
    AllInfo = {"agent":AllplatInfo,"yxTreeNodes":Ztree_nodes.decode("unicode-escape")}
    return render_template('shutdowngame/shutdownmanage.html',AllInfo=AllInfo)


@shutdowngame.route("/shutdownByServers",methods=['GET','POST'])
@login_required
@permission_required("closeserver")
def shutdownByServers():
    serverInfo = json.loads(request.form['serverinfo'])
    shutdownTime = request.form['time']
    sign_md5 = minitool.GetMd5(json.dumps(serverInfo)+shutdownTime+current_user.username+minitool.GetRandomString()+"shutdownGame")
    sign = "%s-%s-%s" %(sign_md5,str(int(time.time())),minitool.GetRandomString())
    gameName = current_app.config.get('GAMENAME')
    updateKey = current_app.config.get('UPDATEKEY')
    server_info = []
    AllServerInfoDictMsg = getmdsapi.getallserverTodict()
    if int(AllServerInfoDictMsg['code']) == 0:
        AllServerInfoDict = AllServerInfoDictMsg['Msg']
        for u in range(len(serverInfo)):
            platformAlias = serverInfo[u]['agent']
            serverId = serverInfo[u]['zone']
            plat_id = "%s_%s" %(platformAlias,serverId)
            updateCmd = "shutdownGame"
            serverName = "%s %s服" %(platformAlias,serverId)
            zoneSign_md5 = minitool.GetMd5(platformAlias+serverId+current_user.username+minitool.GetRandomString()+"shutdownGame")
            zoneSign = "%s-%s-%s" %(zoneSign_md5,str(int(time.time())),minitool.GetRandomString())
            version = ""
            server_info.append({"platformAlias":platformAlias,"serverId":serverId,"platformId":AllServerInfoDict[plat_id]['platformId'],"countTime":shutdownTime,"serverIp":AllServerInfoDict[plat_id]['serverIp'],"worldPort":AllServerInfoDict[plat_id]['worldPort']})
            WriteUpdateLog(sign,updateCmd,gameName,platformAlias,serverId,serverName,zoneSign,version)
        currentTime = str(int(time.time()))
        remoteCmd = {"cmd":"shutdown_game","time":currentTime,"securitySign":minitool.GetMd5(updateKey+"shutdown_game"+currentTime),"server_info":server_info}
        checkResult = sendsocket.send_socket(json.dumps(remoteCmd)+"#zbcyh#")
        checkResultJson = json.loads(checkResult)
        returnList = []
        for i in range(len(checkResultJson)):
            servername = "%s %s服" %(checkResultJson[i]['platformAlias'],checkResultJson[i]['serverId'])
            if int(checkResultJson[i]['result']) == 1:
                result = "成功"
            else:
                result = "失败"
            returnList.append({"servername":servername,"result":result})
        return jsonify(result="true",resultsList=returnList)
    else:
        current_app.logger.error("获取mds区服表出错")
        return jsonify(result="true",resultsList=[])
        
            
