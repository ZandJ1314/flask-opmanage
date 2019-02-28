# -*- coding: utf-8 -*-
import sys, time, random

reload(sys)
sys.setdefaultencoding('utf8')
from flask import render_template, redirect, request, url_for, flash, session, jsonify, json, current_app
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import ywtools
from .. import db
from .. import cache
from ..models import *
from ..decorators import permission_required
from ..mylibs import sendsocket, getmdsapi, loadztree, minitool, mysqlsrcztree, svncommit, countversion


def WriteUpdateLog(sign, updateCmd, gameName, platformAlias, serverId, serverName, zoneSign, version, cmdString="null"):
    operationlogZone = Operationlog()
    operationlogZone.batchSign = sign
    operationlogZone.cmd = updateCmd
    operationlogZone.cmdString = cmdString
    operationlogZone.gameName = gameName
    operationlogZone.platformAlias = platformAlias
    operationlogZone.sendDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    operationlogZone.sendTime = int(time.time())
    operationlogZone.sendUser = current_user.username
    operationlogZone.serverId = int(serverId)
    operationlogZone.serverName = serverName
    operationlogZone.sign = zoneSign
    operationlogZone.version = version
    db.session.add(operationlogZone)
    db.session.commit()


@ywtools.route("/ywUpdateManage", methods=['GET', 'POST'])
@login_required
@permission_required("ywupdate")
def ywUpdateManage():
    AllplatInfo = []
    Allplat = json.loads(cache.get('all_plats'))
    Ztree_nodes = cache.get('Ztree_nodes')
    for i in range(len(Allplat)):
        AllplatInfo.append(Allplat[i]['platformAlias'])
    AllInfo = {"agent": AllplatInfo, "yxTreeNodes": Ztree_nodes.decode("unicode-escape"),
               "permissionList": session['permissons']}
    return render_template('ywtools/ywUpdateManage.html', AllInfo=AllInfo)


@ywtools.route("/selectTables", methods=['GET'])
@login_required
def selectTables():
    SrcDBinfo = mysqlsrcztree.LoadMysqlSrcZtree()
    if SrcDBinfo['code'] == 0:
        AllMysqlTables = json.dumps(SrcDBinfo['tableTree'])
        DBsList = SrcDBinfo['DbsList']
        AllInfo = {"MysqlTreeNodes": AllMysqlTables.decode("unicode-escape"), "DBsList": DBsList}
        return render_template('ywtools/selectTables.html', AllInfo=AllInfo)
    else:
        current_app.logger.error("get mysql src info error")
        return render_template('ywtools/selectTables.html', AllInfo=[])


@ywtools.route("/actionAgainUpdate", methods=['POST'])
@login_required
def actionAgainUpdate():
    batchSign = request.args['sign']
    fail = db.session.query(Operationlog.platformAlias, Operationlog.serverId, Operationlog.cmd, Operationlog.cmdString,
                            Operationlog.version).filter(Operationlog.batchSign == batchSign,
                                                         Operationlog.result != 0).all()
    if len(fail) == 0:
        return jsonify(result="serversnull")
    cmd = fail[0].cmd
    if cmd == "updateGameDate":
        version = fail[0].version
        GameDataMd5 = fail[0].cmdString.split('|')[0]
        isReset = fail[0].cmdString.split('|')[1]
        cmdString = fail[0].cmdString
        sign_md5 = minitool.GetMd5(json.dumps(
            fail) + version + current_user.username + isReset + minitool.GetRandomString() + "gameDataUpdate")
        sign = "%s-%s-%s" % (sign_md5, str(int(time.time())), minitool.GetRandomString())
        gameName = current_app.config.get('GAMENAME')
        updateKey = current_app.config.get('UPDATEKEY')
        server_info = []
        AllServerInfoDictMsg = getmdsapi.getallserverTodict()
        if int(AllServerInfoDictMsg['code']) == 0:
            AllServerInfoDict = AllServerInfoDictMsg['Msg']
            for u in range(len(fail)):
                platformAlias = fail[u].platformAlias
                serverId = fail[u].serverId
                zoneSign_md5 = minitool.GetMd5(platformAlias + str(
                    serverId) + version + current_user.username + isReset + minitool.GetRandomString() + "gameDataUpdate")
                zoneSign = "%s-%s-%s" % (zoneSign_md5, str(int(time.time())), minitool.GetRandomString())
                updateCmd = "updateGameDate"
                serverName = "%s %s服" % (platformAlias, serverId)
                plat_id = "%s_%s" % (platformAlias, serverId)
                server_info.append({"dbIp": AllServerInfoDict[plat_id]['dbIp'],
                                    "dbPort": AllServerInfoDict[plat_id]['dbPort'],
                                    "gameDataDBName": AllServerInfoDict[plat_id]['gameDataDBName'],
                                    "javaDir": AllServerInfoDict[plat_id]['javaDir'],
                                    "from": "backend",
                                    "gameAlias": gameName,
                                    "platformAlias": platformAlias,
                                    "resetver": isReset,
                                    "serverId": serverId,
                                    "sign": zoneSign})
                # 操作日志写入数据库
                WriteUpdateLog(sign, updateCmd, gameName, platformAlias, serverId, serverName, zoneSign, version,
                               cmdString)
            currentTime = str(int(time.time()))
            remoteCmd = {"UpdateSvnDir": version,
                         "GameDataMd5": GameDataMd5,
                         "cmd": "update_gamedata",
                         "time": currentTime,
                         "securitySign": minitool.GetMd5(updateKey + "update_gamedata" + currentTime),
                         "server_info": server_info}
            current_app.logger.error(json.dumps(remoteCmd))
            sendsocket.NoResultSocket(json.dumps(remoteCmd))
            msg = current_user.username + " " + time.strftime("%Y-%m-%d %H:%M:%S",
                                                              time.localtime()) + " 执行gameDataUpdate"
        else:
            msg = current_user.username + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "  获取区服信息失败"
            sign = "null"
        return jsonify(result="true", msg=msg, sign=sign)


@ywtools.route("/gameDataUpdate", methods=['GET', 'POST'])
@login_required
@permission_required("update_gamedata")
def gameDataUpdate():
    serverInfo = json.loads(request.form['serverinfo'])
    isReset = request.form['isReset']
    dbName = request.form['dbtext']
    tablesName = request.form['tablestext']
    commitMsg = svncommit.CommitGameData(dbName, tablesName)
    if commitMsg['code'] == 0:
        version = commitMsg['svnDir']
        GameDataMd5 = commitMsg['GameDataMd5']
        cmdString = "%s|%s" % (GameDataMd5, isReset)
        sign_md5 = minitool.GetMd5(json.dumps(
            serverInfo) + version + current_user.username + isReset + minitool.GetRandomString() + "gameDataUpdate")
        sign = "%s-%s-%s" % (sign_md5, str(int(time.time())), minitool.GetRandomString())
        gameName = current_app.config.get('GAMENAME')
        updateKey = current_app.config.get('UPDATEKEY')
        server_info = []
        AllServerInfoDictMsg = getmdsapi.getallserverTodict()
        if int(AllServerInfoDictMsg['code']) == 0:
            AllServerInfoDict = AllServerInfoDictMsg['Msg']
            if int(AllServerInfoDictMsg['openingNum']) == 0:
                for u in range(len(serverInfo)):
                    platformAlias = serverInfo[u]['agent']
                    serverId = serverInfo[u]['zone']
                    zoneSign_md5 = minitool.GetMd5(
                        platformAlias + serverId + version + current_user.username + isReset + minitool.GetRandomString() + "gameDataUpdate")
                    zoneSign = "%s-%s-%s" % (zoneSign_md5, str(int(time.time())), minitool.GetRandomString())
                    updateCmd = "updateGameDate"
                    serverName = "%s %s服" % (platformAlias, serverId)
                    plat_id = "%s_%s" % (platformAlias, serverId)
                    server_info.append(
                        {"dbIp": AllServerInfoDict[plat_id]['dbIp'], "dbPort": AllServerInfoDict[plat_id]['dbPort'],
                         "gameDataDBName": AllServerInfoDict[plat_id]['gameDataDBName'],
                         "javaDir": AllServerInfoDict[plat_id]['javaDir'], "from": "backend", "gameAlias": gameName,
                         "platformAlias": platformAlias, "resetver": isReset, "serverId": serverId, "sign": zoneSign})
                    # 操作日志写入数据库
                    WriteUpdateLog(sign, updateCmd, gameName, platformAlias, serverId, serverName, zoneSign, version,
                                   cmdString)

                currentTime = str(int(time.time()))
                remoteCmd = {"UpdateSvnDir": version, "GameDataMd5": GameDataMd5, "cmd": "update_gamedata",
                             "time": currentTime,
                             "securitySign": minitool.GetMd5(updateKey + "update_gamedata" + currentTime),
                             "server_info": server_info}
                current_app.logger.error(json.dumps(remoteCmd))
                sendsocket.NoResultSocket(json.dumps(remoteCmd))
                msg = current_user.username + " " + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                  time.localtime()) + " 执行gameDataUpdate"
            else:
                msg = current_user.username + " " + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                  time.localtime()) + "  运维正在开服，请稍等！！"
                sign = "null"
        else:
            msg = current_user.username + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "  获取区服信息失败"
            sign = "null"
    else:
        msg = current_user.username + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "  提交SVN出错"
        sign = "null"

    return jsonify(result="true", msg=msg, sign=sign)


@ywtools.route("/javaUpdate", methods=['GET', 'POST'])
@login_required
@permission_required("update_java")
def javaUpdate():
    serverInfo = json.loads(request.form['serverinfo'])
    version = request.form['version']
    sign_md5 = minitool.GetMd5(
        json.dumps(serverInfo) + version + current_user.username + minitool.GetRandomString() + "javaUpdate")
    sign = "%s-%s-%s" % (sign_md5, str(int(time.time())), minitool.GetRandomString())
    gameName = current_app.config.get('GAMENAME')
    updateKey = current_app.config.get('UPDATEKEY')
    server_info = []
    AllServerInfoDictMsg = getmdsapi.getallserverTodict()
    if int(AllServerInfoDictMsg['code']) == 0:
        AllServerInfoDict = AllServerInfoDictMsg['Msg']
        for u in range(len(serverInfo)):
            platformAlias = serverInfo[u]['agent']
            serverId = serverInfo[u]['zone']
            zoneSign_md5 = minitool.GetMd5(
                platformAlias + serverId + version + current_user.username + minitool.GetRandomString() + "javaUpdate")
            zoneSign = "%s-%s-%s" % (zoneSign_md5, str(int(time.time())), minitool.GetRandomString())
            updateCmd = "updateJava"
            serverName = "%s %s服" % (platformAlias, serverId)
            plat_id = "%s_%s" % (platformAlias, serverId)
            server_info.append(
                {"serverIp": AllServerInfoDict[plat_id]['serverIp'], "javaDir": AllServerInfoDict[plat_id]['javaDir'],
                 "from": "backend", "gameAlias": gameName, "platformAlias": platformAlias, "serverId": serverId,
                 "sign": zoneSign})
            # 操作日志写入数据库
            WriteUpdateLog(sign, updateCmd, gameName, platformAlias, serverId, serverName, zoneSign, version)

        currentTime = str(int(time.time()))
        remoteCmd = {"UpdateSvnDir": version, "cmd": "update_java", "time": currentTime,
                     "securitySign": minitool.GetMd5(updateKey + "update_java" + currentTime),
                     "server_info": server_info}
        sendsocket.NoResultSocket(json.dumps(remoteCmd))
        msg = current_user.username + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 执行javaUpdate"
    else:
        msg = current_user.username + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "  获取区服信息失败"
        sign = "null"
    return jsonify(result="true", msg=msg, sign=sign)


@ywtools.route("/javascriptUpdate", methods=['GET', 'POST'])
@login_required
@permission_required("update_javascripts")
def javascriptUpdate():
    serverInfo = json.loads(request.form['serverinfo'])
    version = request.form['version']
    sign_md5 = minitool.GetMd5(
        json.dumps(serverInfo) + version + current_user.username + minitool.GetRandomString() + "javascriptUpdate")
    sign = "%s-%s-%s" % (sign_md5, str(int(time.time())), minitool.GetRandomString())
    gameName = current_app.config.get('GAMENAME')
    updateKey = current_app.config.get('UPDATEKEY')
    server_info = []
    AllServerInfoDictMsg = getmdsapi.getallserverTodict()
    if int(AllServerInfoDictMsg['code']) == 0:
        AllServerInfoDict = AllServerInfoDictMsg['Msg']
        if int(AllServerInfoDictMsg['openingNum']) == 0:
            for u in range(len(serverInfo)):
                platformAlias = serverInfo[u]['agent']
                serverId = serverInfo[u]['zone']
                zoneSign_md5 = minitool.GetMd5(
                    platformAlias + serverId + version + current_user.username + minitool.GetRandomString() + "javascriptUpdate")
                zoneSign = "%s-%s-%s" % (zoneSign_md5, str(int(time.time())), minitool.GetRandomString())
                updateCmd = "updateJavascripts"
                serverName = "%s %s服" % (platformAlias, serverId)
                plat_id = "%s_%s" % (platformAlias, serverId)
                server_info.append({"serverIp": AllServerInfoDict[plat_id]['serverIp'],
                                    "javaDir": AllServerInfoDict[plat_id]['javaDir'], "from": "backend",
                                    "gameAlias": gameName, "platformAlias": platformAlias, "serverId": serverId,
                                    "sign": zoneSign})

                # 操作日志写入数据库
                WriteUpdateLog(sign, updateCmd, gameName, platformAlias, serverId, serverName, zoneSign, version)

            currentTime = str(int(time.time()))
            remoteCmd = {"UpdateSvnDir": version, "cmd": "update_javascripts", "time": currentTime,
                         "securitySign": minitool.GetMd5(updateKey + "update_javascripts" + currentTime),
                         "server_info": server_info}
            sendsocket.NoResultSocket(json.dumps(remoteCmd))
            msg = current_user.username + " " + time.strftime("%Y-%m-%d %H:%M:%S",
                                                              time.localtime()) + " 执行updateJavascripts"
        else:
            msg = current_user.username + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "  运维正在开服，请稍等！！"
            sign = "null"
    else:
        msg = current_user.username + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "  获取区服信息失败"
        sign = "null"
    return jsonify(result="true", msg=msg, sign=sign)


@ywtools.route("/frontUpdate", methods=['GET', 'POST'])
@login_required
@permission_required("update_front")
def frontUpdate():
    serverInfo = json.loads(request.form['serverinfo'])
    gameclientversion = request.form['client_gameclient']
    proversion = request.form['pro']
    mainuiversion = request.form['gif_mainUI']
    clientcfgversion = request.form['gif_clientCfg']
    resversion = request.form['res']
    gameloginversion = request.form['client_gamelogin']
    gameloadversion = request.form['client_gameload']
    sign_md5 = minitool.GetMd5(
        json.dumps(serverInfo) + gameclientversion + current_user.username + minitool.GetRandomString() + "frontUpdate")
    sign = "%s-%s-%s" % (sign_md5, str(int(time.time())), minitool.GetRandomString())
    gameName = current_app.config.get('GAMENAME')
    updateKey = current_app.config.get('UPDATEKEY')
    server_info = []
    AllServerInfoDictMsg = getmdsapi.getallserverTodict()
    if int(AllServerInfoDictMsg['code']) == 0:
        AllServerInfoDict = AllServerInfoDictMsg['Msg']
        for u in range(len(serverInfo)):
            platformAlias = serverInfo[u]['agent']
            serverId = serverInfo[u]['zone']
            zoneSign_md5 = minitool.GetMd5(
                platformAlias + serverId + gameclientversion + current_user.username + minitool.GetRandomString() + "frontUpdate")
            zoneSign = "%s-%s-%s" % (zoneSign_md5, str(int(time.time())), minitool.GetRandomString())
            updateCmd = "updateFront"
            serverName = "%s %s服" % (platformAlias, serverId)
            plat_id = "%s_%s" % (platformAlias, serverId)
            server_info.append(
                {"serverIp": AllServerInfoDict[plat_id]['serverIp'], "javaDir": AllServerInfoDict[plat_id]['javaDir'],
                 "from": "backend", "gameAlias": gameName, "platformAlias": platformAlias, "serverId": serverId,
                 "sign": zoneSign})
            # 操作日志写入数据库
            WriteUpdateLog(sign, updateCmd, gameName, platformAlias, serverId, serverName, zoneSign, gameclientversion)

        currentTime = str(int(time.time()))
        remoteCmd = {"gameclientversion": gameclientversion, "proversion": proversion, "mainuiversion": mainuiversion,
                     "clientcfgversion": clientcfgversion, "resversion": resversion,
                     "gameloginversion": gameloginversion,"gameloadversion": gameloadversion, "cmd": "update_frontversion", "time": currentTime,
                     "securitySign": minitool.GetMd5(updateKey + "update_frontversion" + currentTime),
                     "server_info": server_info}
        sendsocket.NoResultSocket(json.dumps(remoteCmd))
        msg = current_user.username + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 执行updateFront"
    else:
        msg = current_user.username + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "  获取区服信息失败"
        sign = "null"
    return jsonify(result="true", msg=msg, sign=sign)


@ywtools.route("/planResUpdate", methods=['POST'])
@login_required
@permission_required("update_planres")
def planResUpdate():
    serverInfo = json.loads(request.form['serverinfo'])
    fileMd5 = request.form['fileMd5']
    sign_md5 = minitool.GetMd5(
        json.dumps(serverInfo) + current_user.username + minitool.GetRandomString() + "planresupdate")
    sign = "%s-%s-%s" % (sign_md5, str(int(time.time())), minitool.GetRandomString())
    gameName = current_app.config.get('GAMENAME')
    updateKey = current_app.config.get('UPDATEKEY')
    commitMsg = svncommit.CommitPlanRes()
    if commitMsg['code'] == 0:
        currentVerMsg = countversion.CountVer(serverInfo, "datares")
        if int(currentVerMsg['code']) == 0:
            currentVer = currentVerMsg['Msg']
            for key, value in currentVer.items():
                for w in range(len(value)):
                    updateCmd = "updatePlanRes"
                    platformAlias = value[w]['platformAlias']
                    serverId = value[w]['serverId']
                    zoneSign = value[w]['sign']
                    serverName = "%s %s服" % (platformAlias, serverId)
                    version = ""
                    # 操作日志写入数据库
                    WriteUpdateLog(sign, updateCmd, gameName, platformAlias, serverId, serverName, zoneSign, version)
            currentTime = str(int(time.time()))
            remoteCmd = {
                "cmd": "update_planres",
                "time": currentTime,
                "securitySign": minitool.GetMd5(updateKey + "update_planres" + currentTime),
                "fileMd5": fileMd5,
                "server_info": currentVer
            }
            sendsocket.NoResultSocket(json.dumps(remoteCmd))
            msg = current_user.username + " " + time.strftime("%Y-%m-%d %H:%M:%S",
                                                              time.localtime()) + " 执行updatePlanRes"
        elif int(currentVerMsg['code']) == 5:
            msg = current_user.username + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 运维正在开服，请稍等！！"
            sign = "null"
        else:
            msg = current_user.username + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "统计版本失败"
            sign = "null"
    else:
        msg = current_user.username + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "svn提交res失败"
        sign = "null"
    return jsonify(result="true", msg=msg, sign=sign)


@ywtools.route("/phpUpdate", methods=['GET', 'POST'])
@login_required
@permission_required("update_php")
def phpUpdate():
    version = ""
    serverInfo = json.loads(request.form['serverinfo'])
    sign_md5 = minitool.GetMd5(
        json.dumps(serverInfo) + current_user.username + minitool.GetRandomString() + "phpUpdate")
    sign = "%s-%s-%s" % (sign_md5, str(int(time.time())), minitool.GetRandomString())
    gameName = current_app.config.get('GAMENAME')
    updateKey = current_app.config.get('UPDATEKEY')
    server_info = []
    AllServerInfoDictMsg = getmdsapi.getallserverTodict()
    if int(AllServerInfoDictMsg['code']) == 0:
        AllServerInfoDict = AllServerInfoDictMsg['Msg']
        for u in range(len(serverInfo)):
            platformAlias = serverInfo[u]['agent']
            serverId = serverInfo[u]['zone']
            zoneSign_md5 = minitool.GetMd5(
                platformAlias + serverId + current_user.username + minitool.GetRandomString() + "phpUpdate")
            zoneSign = "%s-%s-%s" % (zoneSign_md5, str(int(time.time())), minitool.GetRandomString())
            updateCmd = "updatePhp"
            serverName = "%s %s服" % (platformAlias, serverId)
            plat_id = "%s_%s" % (platformAlias, serverId)
            server_info.append(
                {"serverIp": AllServerInfoDict[plat_id]['serverIp'], "from": "backend", "gameAlias": gameName,
                 "platformAlias": platformAlias, "serverId": serverId, "sign": zoneSign})
            # 操作日志写入数据库
            WriteUpdateLog(sign, updateCmd, gameName, platformAlias, serverId, serverName, zoneSign, version)
        currentTime = str(int(time.time()))
        remoteCmd = {"cmd": "update_php", "time": currentTime,
                     "securitySign": minitool.GetMd5(updateKey + "update_php" + currentTime),
                     "server_info": server_info}
        sendsocket.NoResultSocket(json.dumps(remoteCmd))
        msg = current_user.username + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 执行updatePhp"
    else:
        msg = current_user.username + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "  获取区服信息失败"
        sign = "null"

    return jsonify(result="true", msg=msg, sign=sign)


# 启动游戏没有返回结果
@ywtools.route("/bootGame", methods=['GET', 'POST'])
@login_required
@permission_required("bootgame")
def bootGame():
    version = ""
    zoneSign = ""
    serverInfo = json.loads(request.form['serverinfo'])
    sign_md5 = minitool.GetMd5(
        json.dumps(serverInfo) + current_user.username + minitool.GetRandomString() + "startGame")
    sign = "%s-%s-%s" % (sign_md5, str(int(time.time())), minitool.GetRandomString())
    gameName = current_app.config.get('GAMENAME')
    updateKey = current_app.config.get('UPDATEKEY')
    server_info = []
    AllServerInfoDictMsg = getmdsapi.getallserverTodict()
    if int(AllServerInfoDictMsg['code']) == 0:
        AllServerInfoDict = AllServerInfoDictMsg['Msg']
        for u in range(len(serverInfo)):
            platformAlias = serverInfo[u]['agent']
            serverId = serverInfo[u]['zone']
            updateCmd = "startGame"
            serverName = "%s %s服" % (platformAlias, serverId)
            plat_id = "%s_%s" % (platformAlias, serverId)
            server_info.append(
                {"serverIp": AllServerInfoDict[plat_id]['serverIp'], "javaDir": AllServerInfoDict[plat_id]['javaDir'],
                 "from": "backend", "gameAlias": gameName, "platformAlias": platformAlias, "serverId": serverId})
            # 操作日志写入数据库
            WriteUpdateLog(sign, updateCmd, gameName, platformAlias, serverId, serverName, zoneSign, version)
        currentTime = str(int(time.time()))
        remoteCmd = {"UpdateSvnDir": "", "cmd": "start_game", "time": currentTime,
                     "securitySign": minitool.GetMd5(updateKey + "start_game" + currentTime),
                     "server_info": server_info}
        sendsocket.NoResultSocket(json.dumps(remoteCmd))
    return jsonify(result="true")


# 检查启动状态实时返回结果
@ywtools.route("/checkState", methods=['GET', 'POST'])
@login_required
@permission_required("checkserverstat")
def checkState():
    serverInfo = json.loads(request.form['serverinfo'])
    checkType = request.form['version']
    gameName = current_app.config.get('GAMENAME')
    updateKey = current_app.config.get('UPDATEKEY')
    server_info = []
    sucessList = []
    failList = []
    AllServerInfoDictMsg = getmdsapi.getallserverTodict()
    if int(AllServerInfoDictMsg['code']) == 0:
        AllServerInfoDict = AllServerInfoDictMsg['Msg']
        for u in range(len(serverInfo)):
            platformAlias = serverInfo[u]['agent']
            serverId = serverInfo[u]['zone']
            plat_id = "%s_%s" % (platformAlias, serverId)
            server_info.append(
                {"serverIp": AllServerInfoDict[plat_id]['serverIp'], "javaDir": AllServerInfoDict[plat_id]['javaDir'],
                 "from": "backend", "gameAlias": gameName, "platformAlias": platformAlias, "serverId": serverId})
        currentTime = str(int(time.time()))
        remoteCmd = {"checkType": checkType, "cmd": "check_state", "time": currentTime,
                     "securitySign": minitool.GetMd5(updateKey + "check_state" + currentTime),
                     "server_info": server_info}
        checkResult = sendsocket.send_socket(json.dumps(remoteCmd) + "#zbcyh#")
        checkResultJson = json.loads(checkResult)
        for xi in range(len(checkResultJson)):
            if checkType == "start":
                if int(checkResultJson[xi]['code']) == 0:
                    sucessList.append({"platformAlias": checkResultJson[xi]['platformAlias'],
                                       "serverId": checkResultJson[xi]['serverId'], "code": checkResultJson[xi]['code'],
                                       "codemessage": checkResultJson[xi]['codemessage']})
                else:
                    failList.append({"platformAlias": checkResultJson[xi]['platformAlias'],
                                     "serverId": checkResultJson[xi]['serverId'], "code": checkResultJson[xi]['code'],
                                     "codemessage": checkResultJson[xi]['codemessage']})
            else:
                if int(checkResultJson[xi]['code']) == 2:
                    sucessList.append({"platformAlias": checkResultJson[xi]['platformAlias'],
                                       "serverId": checkResultJson[xi]['serverId'], "code": checkResultJson[xi]['code'],
                                       "codemessage": checkResultJson[xi]['codemessage']})
                else:
                    failList.append({"platformAlias": checkResultJson[xi]['platformAlias'],
                                     "serverId": checkResultJson[xi]['serverId'], "code": checkResultJson[xi]['code'],
                                     "codemessage": checkResultJson[xi]['codemessage']})

    return jsonify(result="true", map={"fail": failList, "success": sucessList})


@ywtools.route("/queryResult", methods=['GET', 'POST'])
@login_required
def queryResult():
    batchSign = request.args['sign']
    sucess = db.session.query(Operationlog.platformAlias, Operationlog.serverId, Operationlog.resultString).filter_by(
        batchSign=batchSign, result=0).all()
    fail = db.session.query(Operationlog.platformAlias, Operationlog.serverId, Operationlog.resultString).filter(
        Operationlog.batchSign == batchSign, Operationlog.result != 0).all()
    unknow = db.session.query(Operationlog.platformAlias, Operationlog.serverId, Operationlog.resultString).filter_by(
        batchSign=batchSign, result=None).all()
    sucessList = []
    failList = []
    unknowList = []
    for i in range(len(sucess)):
        sucessList.append({"platformAlias": sucess[i].platformAlias, "serverId": sucess[i].serverId,
                           "resultString": sucess[i].resultString})
    for i in range(len(fail)):
        failList.append({"platformAlias": fail[i].platformAlias, "serverId": fail[i].serverId,
                         "resultString": fail[i].resultString})
    for i in range(len(unknow)):
        unknowList.append({"platformAlias": unknow[i].platformAlias, "serverId": unknow[i].serverId,
                           "resultString": unknow[i].resultString})
    resultMap = {"success": sucessList, "fail": failList, "unknow": unknowList}
    return jsonify(result="true", resultMap=resultMap)


@ywtools.route("/historyQuery", methods=['GET', 'POST'])
@login_required
def historyQuery():
    startTime = request.form['start'] + " 00:00:00"
    endTime = request.form['end'] + " 23:59:59"
    startTime_linux = int(time.mktime(time.strptime(startTime, '%Y-%m-%d %H:%M:%S')))
    endTime_linux = int(time.mktime(time.strptime(endTime, '%Y-%m-%d %H:%M:%S')))
    total_batchSign = db.session.query(Operationlog.batchSign).filter(Operationlog.sendTime >= startTime_linux,
                                                                      Operationlog.sendTime <= endTime_linux).group_by(
        Operationlog.batchSign).order_by(Operationlog.sendTime.desc()).all()
    resultList = []
    for x in range(len(total_batchSign)):
        singleBatch = total_batchSign[x].batchSign
        singleBatch_sucess = db.session.query(Operationlog).filter_by(batchSign=singleBatch, result=0).count()
        singleBatch_fail = db.session.query(Operationlog).filter(Operationlog.batchSign == singleBatch,
                                                                 Operationlog.result != 0).count()
        singleBatch_unknow = db.session.query(Operationlog).filter_by(batchSign=singleBatch, result=None).count()
        singleBatch_info = db.session.query(Operationlog.sendUser, Operationlog.sendDate, Operationlog.gameName,
                                            Operationlog.cmd).filter_by(batchSign=singleBatch).first()
        singleBatch_User = singleBatch_info.sendUser
        singleBatch_Senddate = singleBatch_info.sendDate
        singleBatch_Gamename = singleBatch_info.gameName
        singleBatch_Cmd = singleBatch_info.cmd
        resultList.append(
            {"cmd": singleBatch_Cmd, "time": singleBatch_Senddate, "fail": singleBatch_fail, "batchSign": singleBatch,
             "unknow": singleBatch_unknow, "gameName": singleBatch_Gamename, "success": singleBatch_sucess,
             "user": singleBatch_User})
    return jsonify(result="true", resultList=resultList)
