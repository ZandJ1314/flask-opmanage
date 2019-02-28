# -*- coding: utf-8 -*-
import sys, time, random

reload(sys)
sys.setdefaultencoding('utf8')
from flask import render_template, redirect, request, url_for, flash, session, jsonify, json, current_app
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import openserver
from .. import db
from .. import cache
from ..models import *
from ..decorators import permission_required
from ..mylibs import sendsocket, getmdsapi, loadztree, minitool


@openserver.route("/openServerManage", methods=['GET', 'POST'])
@login_required
@permission_required("openserver")
def openServerManage():
    serverIp = []
    Allplat = json.loads(cache.get('all_plats'))
    AllIp = db.session.query(Physerverlist.dip).filter_by(function="gameservers", isdeleted=0).group_by(
        Physerverlist.dip).all()
    for b in range(len(AllIp)):
        serverIp.append(AllIp[b].dip)
    AllInfo = {"ips": serverIp, "plats": Allplat}
    return render_template('openserver/openCombine.html', AllInfo=AllInfo)


@openserver.route("/openserverSubmit", methods=['GET', 'POST'])
@login_required
@permission_required("openserver")
def openserverSubmit():
    Allser = json.loads(request.form['allserver'])
    sign_md5 = minitool.GetMd5(json.dumps(Allser) + current_user.username + minitool.GetRandomString() + "OpenServer")
    sign = "%s-%s-%s" % (sign_md5, str(int(time.time())), minitool.GetRandomString())
    gameName = current_app.config.get('GAMENAME')
    updateKey = current_app.config.get('UPDATEKEY')
    Allplats = json.loads(cache.get('all_plats'))
    AllplatsJson = {}
    for p in range(len(Allplats)):
        AllplatsJson[str(Allplats[p]['platformId'])] = Allplats[p]
    server_info = []
    inserMdsList = []
    for u in range(len(Allser)):
        serverId = Allser[u]['serverId']
        serverIp = Allser[u]['serverIp']
        openTime = Allser[u]['openTime']
        iszone = Allser[u]['totalNum']
        totalNum = 3
        platformId = Allser[u]['agent']
        platformAlias = AllplatsJson[platformId]['platformAlias']
        configId = AllplatsJson[platformId]['configId']
        gameAlias = AllplatsJson[platformId]['gameAlias']
        gameId = AllplatsJson[platformId]['gameId']
        platformName = AllplatsJson[platformId]['platformName']
        serverName = "%s %s服" % (platformName, serverId)
        zoneSign_md5 = minitool.GetMd5(
            platformAlias + serverId + openTime + current_user.username + minitool.GetRandomString() + "OpenServer")
        zoneSign = "%s-%s-%s" % (zoneSign_md5, str(int(time.time())), minitool.GetRandomString())
        uniconIp = db.session.query(Physerverlist.cip).filter_by(dip=serverIp).first()

        inserMdsList.append([{"configId": configId, "gameAlias": gameAlias, "gameId": gameId, "platformId": platformId,
                              "platformName": platformName, "platformAlias": platformAlias, "serverId": serverId,
                              "serverName": serverName, "serverIp": serverIp, "unicomIp": uniconIp[0],
                              "isCombined": "false", "isDeleted": "false", "iszone": iszone, "serverOrder": "0",
                              "sumzone": totalNum}])
        server_info.append(
            {"configId": configId, "gameAlias": gameAlias, "openDate": openTime, "platformAlias": platformAlias,
             "platformId": platformId, "serverId": serverId, "serverIp": serverIp, "sign": zoneSign, "iszone": iszone,
             "sumzone": totalNum})
        # 操作日志写入数据库
        operationlogZone = Operationlog()
        operationlogZone.batchSign = sign
        operationlogZone.cmd = "OpenServer"
        operationlogZone.gameName = gameName
        operationlogZone.platformAlias = platformAlias
        operationlogZone.sendDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        operationlogZone.sendTime = int(time.time())
        operationlogZone.sendUser = current_user.username
        operationlogZone.serverId = int(serverId)
        operationlogZone.serverName = "%s %s服" % (platformAlias, serverId)
        operationlogZone.sign = zoneSign
        db.session.add(operationlogZone)
        db.session.commit()

    for insermdsList in inserMdsList:
        getmdsapi.insertMds(insermdsList)
    currentTime = str(int(time.time()))
    remoteCmd = {"cmd": "open_server", "time": currentTime,
                 "securitySign": minitool.GetMd5(updateKey + "open_server" + currentTime), "server_info": server_info}
    sendsocket.NoResultSocket(json.dumps(remoteCmd))

    return jsonify(result="true", batchSign=sign)
