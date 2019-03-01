# -*- coding: utf-8 -*-
import sys,time,random
reload(sys)
sys.setdefaultencoding('utf8')
from flask import render_template, redirect, request, url_for, flash, session,jsonify,json,current_app
from flask.ext.login import login_user, logout_user, current_user
from . import gmcommand
from .. import db
from .. import cache
from ..models import *
from ..decorators import permission_required,login_required
from ..mylibs import sendsocket,getmdsapi,loadztree,minitool


def WriteGmLog(sign,updateCmd,platformAlias,serverId,result):
    operationlogZone = Gmcommandlog()
    operationlogZone.batchsign = sign
    operationlogZone.senddate = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    operationlogZone.sendtime = int(time.time())
    operationlogZone.command = updateCmd
    operationlogZone.senduser = current_user.username
    operationlogZone.platform = platformAlias
    operationlogZone.serverid = int(serverId)
    operationlogZone.result = int(result)
    db.session.add(operationlogZone)
    db.session.commit()

@gmcommand.route("/gmcommand",methods=['GET','POST'])
@login_required
@permission_required("gmcommand")
def gmcommandManage():
    AllplatInfo = []
    Allplat = json.loads(cache.get('all_plats'))
    Ztree_nodes = cache.get('Ztree_nodes')
    for i in range(len(Allplat)):
        AllplatInfo.append(Allplat[i]['platformAlias'])
    AllInfo = {"agent":AllplatInfo,"yxTreeNodes":Ztree_nodes.decode("unicode-escape")}
    return render_template('gmcommand/GMCommandManage.html',AllInfo=AllInfo)

@gmcommand.route("/actionGMCommand",methods=['POST'])
@login_required
@permission_required("gmcommand")
def actionGmcommand():
    gmcmd = request.form['command']
    serverInfo = json.loads(request.form['serverinfo'])
    sign_md5 = minitool.GetMd5(json.dumps(serverInfo)+gmcmd+current_user.username+minitool.GetRandomString())
    sign = "%s-%s-%s" %(sign_md5,str(int(time.time())),minitool.GetRandomString())
    updateKey = current_app.config.get('UPDATEKEY')
    server_info = []
    AllServerInfoDictMsg = getmdsapi.getallserverTodict()
    if int(AllServerInfoDictMsg['code']) == 0:
        AllServerInfoDict = AllServerInfoDictMsg['Msg']
        for u in range(len(serverInfo)):
            platformAlias = serverInfo[u]['agent']
            serverId = serverInfo[u]['zone']
            plat_id = "%s_%s" %(platformAlias,serverId)
            server_info.append({"platformAlias":platformAlias,"serverId":serverId,"excCmd":gmcmd,"serverIp":AllServerInfoDict[plat_id]['serverIp'],"worldPort":AllServerInfoDict[plat_id]['worldPort']})
        currentTime = str(int(time.time()))
        remoteCmd = {"cmd":"exc_gmcmd","time":currentTime,"securitySign":minitool.GetMd5(updateKey+"exc_gmcmd"+currentTime),"server_info":server_info}
        excResult = sendsocket.send_socket(json.dumps(remoteCmd)+"#zbcyh#")
        excResultJson = json.loads(excResult)
        sucessList = []
        failList = []
        for i in range(len(excResultJson)):
            if int(excResultJson[i]['result']) == 1:
                resultString = excResultJson[i]['message'] + "," + excResultJson[i]['data']
                sucessList.append({"platform":excResultJson[i]['platformAlias'],"serverId":excResultJson[i]['serverId'],"resultString":resultString,"state":"0"})
                WriteGmLog(sign,gmcmd,excResultJson[i]['platformAlias'],excResultJson[i]['serverId'],0)
            else:
                failList.append({"platform":excResultJson[i]['platformAlias'],"serverId":excResultJson[i]['serverId'],"resultString":excResultJson[i]['message'],"state":"1"})
                WriteGmLog(sign,gmcmd,excResultJson[i]['platformAlias'],excResultJson[i]['serverId'],1)
        return jsonify(result="true",sign=sign,resultMap={"success":sucessList,"fail":failList})
    else:
        current_app.logger.error("获取mds区服表出错")
        return jsonify(result="true",resultMap={})

@gmcommand.route("/actionAgainGm",methods=['POST'])
@login_required
@permission_required("gmcommand")
def actionAgainGm():
    batchSign = request.args['sign']
    serverInfo = []
    fail = db.session.query(Gmcommandlog.platform,Gmcommandlog.serverid,Gmcommandlog.command).filter_by(batchsign=batchSign,result=1).all()
    if len(fail) == 0:
        return jsonify(result="serversnull")
    for i in range(len(fail)):
        serverInfo.append({"agent":fail[i].platform,"zone":fail[i].serverid})
        gmcmd = fail[i].command
    sign_md5 = minitool.GetMd5(json.dumps(serverInfo)+gmcmd+current_user.username+minitool.GetRandomString())
    sign = "%s-%s-%s" %(sign_md5,str(int(time.time())),minitool.GetRandomString())
    updateKey = current_app.config.get('UPDATEKEY')
    server_info = []
    
    AllServerInfoDictMsg = getmdsapi.getallserverTodict()
    if int(AllServerInfoDictMsg['code']) == 0:
        AllServerInfoDict = AllServerInfoDictMsg['Msg']
        for u in range(len(serverInfo)):
            platformAlias = serverInfo[u]['agent']
            serverId = serverInfo[u]['zone']
            plat_id = "%s_%s" %(platformAlias,serverId)
            server_info.append({"platformAlias":platformAlias,"serverId":serverId,"excCmd":gmcmd,"serverIp":AllServerInfoDict[plat_id]['serverIp'],"worldPort":AllServerInfoDict[plat_id]['worldPort']})
        
        currentTime = str(int(time.time()))
        remoteCmd = {"cmd":"exc_gmcmd","time":currentTime,"securitySign":minitool.GetMd5(updateKey+"exc_gmcmd"+currentTime),"server_info":server_info}
        excResult = sendsocket.send_socket(json.dumps(remoteCmd)+"#zbcyh#")
        excResultJson = json.loads(excResult)
        sucessList = []
        failList = []
        for i in range(len(excResultJson)):
            if int(excResultJson[i]['result']) == 1:
                sucessList.append({"platform":excResultJson[i]['platformAlias'],"serverId":excResultJson[i]['serverId'],"resultString":"成功","state":"0"})
                WriteGmLog(sign,gmcmd,excResultJson[i]['platformAlias'],excResultJson[i]['serverId'],0)
            else:
                failList.append({"platform":excResultJson[i]['platformAlias'],"serverId":excResultJson[i]['serverId'],"resultString":excResultJson[i]['message'],"state":"1"})
                WriteGmLog(sign,gmcmd,excResultJson[i]['platformAlias'],excResultJson[i]['serverId'],1)
        return jsonify(result="true",sign=sign,resultMap={"success":sucessList,"fail":failList})
    else:
        current_app.logger.error("获取mds区服表出错")
        return jsonify(result="true",resultMap={})

@gmcommand.route("/actionOnline",methods=['POST'])
@login_required
@permission_required("gmcommand")
def ActionOnline():
    checkType = request.form['scheck1']
    serverInfo = json.loads(request.form['serverinfo'])
    updateKey = current_app.config.get('UPDATEKEY')
    server_info = []
    AllServerInfoDictMsg = getmdsapi.getallserverTodict()
    if int(AllServerInfoDictMsg['code']) == 0:
        AllServerInfoDict = AllServerInfoDictMsg['Msg']
        for u in range(len(serverInfo)):
            platformAlias = serverInfo[u]['agent']
            serverId = serverInfo[u]['zone']
            plat_id = "%s_%s" %(platformAlias,serverId)
            configId = AllServerInfoDict[plat_id]['configId']
            serverkey = ((int(configId)&0x00FF)<<14)+(int(serverId)&0xFFFF)
            if checkType == "checkonline":
                gmcmd = "&online %s" %(str(serverkey))
            elif checkType == "checkopentime":
                gmcmd = "&backdate %s" %(str(serverkey))
            server_info.append({"platformAlias":platformAlias,"serverId":serverId,"excCmd":gmcmd,"serverIp":AllServerInfoDict[plat_id]['serverIp'],"worldPort":AllServerInfoDict[plat_id]['worldPort']})
        currentTime = str(int(time.time()))
        remoteCmd = {"cmd":"exc_gmcmd","time":currentTime,"securitySign":minitool.GetMd5(updateKey+"exc_gmcmd"+currentTime),"server_info":server_info}
        excResult = sendsocket.send_socket(json.dumps(remoteCmd)+"#zbcyh#")
        excResultJson = json.loads(excResult)
        sucessList = []
        failList = []
        for i in range(len(excResultJson)):
            if int(excResultJson[i]['result']) == 1:
                sucessList.append({"platform":excResultJson[i]['platformAlias'],"serverId":excResultJson[i]['serverId'],"online":str(excResultJson[i]['data'])})
            else:
                failList.append({"platform":excResultJson[i]['platformAlias'],"serverId":excResultJson[i]['serverId'],"online":"0"})
        return jsonify(result="true",resultMap={"success":sucessList,"fail":failList})
    else:
        current_app.logger.error("获取mds区服表出错")
        return jsonify(result="true",resultMap={})
                
            



@gmcommand.route("/gmActionHistory",methods=['POST'])
@login_required
@permission_required("gmcommand")
def gmActionHistory():
    startTime = request.form['start'] + " 00:00:00"
    endTime = request.form['end'] + " 23:59:59"
    startTime_linux = int(time.mktime(time.strptime(startTime,'%Y-%m-%d %H:%M:%S')))
    endTime_linux = int(time.mktime(time.strptime(endTime,'%Y-%m-%d %H:%M:%S')))
    total_batchSign = db.session.query(Gmcommandlog.command,Gmcommandlog.senddate,Gmcommandlog.senduser).filter(Gmcommandlog.sendtime>=startTime_linux,Gmcommandlog.sendtime<=endTime_linux).group_by(Gmcommandlog.batchsign).order_by(Gmcommandlog.sendtime.desc()).all()
    resultList = []
    for x in range(len(total_batchSign)):
        singleBatch_cmd = total_batchSign[x].command
        singleBatch_date = total_batchSign[x].senddate
        singleBatch_user = total_batchSign[x].senduser
        resultList.append({"sendDate":singleBatch_date,"sendUser":singleBatch_user,"command":singleBatch_cmd})
    return jsonify(result="true",resultList=resultList)




