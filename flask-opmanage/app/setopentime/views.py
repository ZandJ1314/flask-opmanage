# -*- coding: utf-8 -*-
import sys, time, random

reload(sys)
sys.setdefaultencoding('utf8')
from flask import render_template, redirect, request, url_for, flash, session, jsonify, json, current_app
from flask.ext.login import login_user, logout_user, current_user
from . import setopentime
from .. import cache
from ..models import *
from ..decorators import permission_required,login_required
from ..mylibs import sendsocket, getmdsapi, loadztree, minitool


@setopentime.route("/resetdate", methods=['GET', 'POST'])
@login_required
@permission_required("resetdate")
def resetDateManage():
    serverIp = []
    Allplat = json.loads(cache.get('all_plats'))
    AllInfo = {"plats": Allplat}
    return render_template('setopentime/resettime.html', AllInfo=AllInfo)


@setopentime.route("/setOpenTimeSubmit", methods=['POST'])
@login_required
@permission_required("resetdate")
def setOpenTimeSubmit():
    Allser = json.loads(request.form['allserver'])
    updateKey = current_app.config.get('UPDATEKEY')
    phpDir = current_app.config.get('PHPWEBROOT')
    Allplats = json.loads(cache.get('all_plats'))
    AllplatsJson = {}
    for p in range(len(Allplats)):
        AllplatsJson[str(Allplats[p]['platformId'])] = Allplats[p]
    server_info = []
    AllServerInfoDictMsg = getmdsapi.getallserverTodict()
    if int(AllServerInfoDictMsg['code']) == 0:
        AllServerInfoDict = AllServerInfoDictMsg['Msg']
        for u in range(len(Allser)):
            serverId = Allser[u]['serverId']
            openTime = Allser[u]['openTime']
            platformId = Allser[u]['agent']
            platformAlias = AllplatsJson[platformId]['platformAlias']
            plat_id = "%s_%s" % (platformAlias, serverId)
            serverIp = AllServerInfoDict[plat_id]['serverIp']
            javaDir = AllServerInfoDict[plat_id]['javaDir']
            server_info.append(
                {"serverIp": serverIp, "Platform": platformAlias, "serverId": serverId, "openservertime": openTime,
                 "JavaDir": javaDir, "phpDir": phpDir})
        currentTime = str(int(time.time()))
        remoteCmd = {"cmd": "set_opentime", "time": currentTime,
                     "securitySign": minitool.GetMd5(updateKey + "set_opentime" + currentTime),
                     "server_info": server_info}
        excResult = sendsocket.send_socket(json.dumps(remoteCmd) + "#zbcyh#")
        current_app.logger.error(excResult)
        excResultJson = json.loads(excResult)
        current_app.logger.error(len(excResultJson))
        sucessList = []
        failList = []
        for i in range(len(excResultJson)):
            current_app.logger.error(excResultJson[i])
            if int(excResultJson[i]['code']) == 0:
                sucessList.append(
                    {"platformAlias": excResultJson[i]['platformAlias'], "serverId": excResultJson[i]['serverId'],
                     "resultString": "success"})
            else:
                failList.append(
                    {"platform": excResultJson[i]['platformAlias'], "serverId": excResultJson[i]['serverId'],
                     "resultString": excResultJson[i]['codemessage']})
        return jsonify(result="true", resultMap={"success": sucessList, "fail": failList})
    else:
        current_app.logger.error("获取mds区服表出错")
        return jsonify(result="true", resultMap={})
