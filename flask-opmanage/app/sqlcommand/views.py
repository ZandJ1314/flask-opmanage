# -*- coding: utf-8 -*-
import sys,time,random
reload(sys)
sys.setdefaultencoding('utf8')
from flask import render_template, redirect, request, url_for, flash, session,jsonify,json,current_app
from flask.ext.login import login_user, logout_user, current_user
from . import sqlcommand
from .. import db
from .. import cache
from ..models import *
from ..decorators import permission_required,login_required
from ..mylibs import sendsocket,getmdsapi,loadztree,minitool


def WriteUpdateLog(sign,updateCmd,cmdString,gameName,platformAlias,serverId,code,codemsg):
    operationlogZone = Operationlog()
    operationlogZone.batchSign = sign
    operationlogZone.cmd = updateCmd
    operationlogZone.cmdString = cmdString
    operationlogZone.gameName = gameName
    operationlogZone.platformAlias = platformAlias
    operationlogZone.sendDate = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    operationlogZone.sendTime = int(time.time())
    operationlogZone.sendUser = current_user.username
    operationlogZone.serverId = int(serverId)
    operationlogZone.serverName = "%s %s服" %(platformAlias,str(serverId))
    operationlogZone.result = int(code)
    operationlogZone.resultString = codemsg
    db.session.add(operationlogZone)
    db.session.commit()

@sqlcommand.route("/sqlcommand",methods=['GET','POST'])
@login_required
@permission_required("sqlcommand")
def SQLCmdManage():
    AllplatInfo = []
    Allplat = json.loads(cache.get('all_plats'))
    Ztree_nodes = cache.get('Ztree_nodes')
    for i in range(len(Allplat)):
        AllplatInfo.append(Allplat[i]['platformAlias'])
    AllInfo = {"agent":AllplatInfo,"yxTreeNodes":Ztree_nodes.decode("unicode-escape")}
    return render_template('sqlcommand/sqlcommand.html',AllInfo=AllInfo)

@sqlcommand.route("/dosqlcmd",methods=['POST'])
@login_required
@permission_required("sqlcommand")
def DoSqlCmd():
    dbList = []
    try:
        gamedb = request.form['game']
        dbList.append(gamedb)
    except:
        pass
    try:
        game_backdb = request.form['game_back']
        dbList.append(game_backdb)
    except:
        pass
    try:
        gamelogdb = request.form['gamelog']
        dbList.append(gamelogdb)
    except:
        pass
    updateCmd = "execSQLcmd"
    sqlCmd = request.form['sqlcommand']
    serverInfo = json.loads(request.form['serverinfo'])
    sign_md5 = minitool.GetMd5(json.dumps(serverInfo)+updateCmd+current_user.username+minitool.GetRandomString())
    sign = "%s-%s-%s" %(sign_md5,str(int(time.time())),minitool.GetRandomString())
    updateKey = current_app.config.get('UPDATEKEY')
    gameName = current_app.config.get('GAMENAME')
    server_info = []
    AllServerInfoDictMsg = getmdsapi.getallserverTodict()
    if int(AllServerInfoDictMsg['code']) == 0:
        AllServerInfoDict = AllServerInfoDictMsg['Msg']
        for u in range(len(serverInfo)):
            platformAlias = serverInfo[u]['agent']
            serverId = serverInfo[u]['zone']
            plat_id = "%s_%s" %(platformAlias,serverId)
            server_info.append({"dbList":dbList,"sqlcmd":sqlCmd,"platformAlias":platformAlias,"serverId":serverId,"dbIp":AllServerInfoDict[plat_id]['dbIp'],"dbPort":AllServerInfoDict[plat_id]['dbPort'],"gameDBName":AllServerInfoDict[plat_id]['gameDBName'],"gameLogDBName":AllServerInfoDict[plat_id]['gameLogDBName']})
        currentTime = str(int(time.time()))
        remoteCmd = {"cmd":"exc_sqlcmd","time":currentTime,"securitySign":minitool.GetMd5(updateKey+"exc_sqlcmd"+currentTime),"server_info":server_info}
        excResult = sendsocket.send_socket(json.dumps(remoteCmd)+"#zbcyh#")
        excResultJson = json.loads(excResult)
        sucessList = []
        failList = []
        for i in range(len(excResultJson)):
            if int(excResultJson[i]['code']) == 0:
                sucessList.append({"platform":excResultJson[i]['platformAlias'],"serverId":excResultJson[i]['serverId'],"resultString":"成功"})
                WriteUpdateLog(sign,updateCmd,sqlCmd,gameName,excResultJson[i]['platformAlias'],excResultJson[i]['serverId'],excResultJson[i]['code'],json.dumps(excResultJson[i]['msg']))
            else:
                failList.append({"platform":excResultJson[i]['platformAlias'],"serverId":excResultJson[i]['serverId'],"resultString":excResultJson[i]['msg']})
                WriteUpdateLog(sign,updateCmd,sqlCmd,gameName,excResultJson[i]['platformAlias'],excResultJson[i]['serverId'],excResultJson[i]['code'],json.dumps(excResultJson[i]['msg']))
        return jsonify(result="true",resultMap={"success":sucessList,"fail":failList})
    else:
        current_app.logger.error("获取mds区服表出错")
        return jsonify(result="true",resultMap={})
    


