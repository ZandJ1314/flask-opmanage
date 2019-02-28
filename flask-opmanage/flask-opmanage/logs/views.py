# -*- coding: utf-8 -*-
import sys,time,random
reload(sys)
sys.setdefaultencoding('utf8')
from flask import render_template, redirect, request, url_for, flash, session,jsonify,json,current_app
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import logs
from .. import db
from .. import cache
from ..models import *
from ..decorators import permission_required
from ..mylibs import sendsocket,getmdsapi


@logs.route("/phplogManage",methods=['GET','POST'])
@login_required
@permission_required("phplog")
def phplogManage():
    logpaths = []
    AllPaths = Phplogpath.query.all()
    for row in range(len(AllPaths)):
        logpaths.append(AllPaths[row].path)
    Allagents = cache.get('all_plats')
    AllInfo = {"logpaths":logpaths,"allagents":json.loads(Allagents)}
    return render_template('logs/phplogManage.html',AllInfo=AllInfo)

@logs.route("/phpChecklogSubmit",methods=['GET','POST'])
@login_required
@permission_required("phplog")
def phpChecklogSubmit():
    agent = request.form['agentList']
    zone = request.form['checkzone']
    checkTime = request.form['checkTime']
    checknum = request.form['checknum']
    logpath = request.form['logsList']
    if agent.strip() == "" or zone.strip() == "" or checkTime.strip() == "" or checknum.strip() == "" or logpath.strip() == "":
        return jsonify(result="信息填写不完整")
    else:
        zoneinfo = getmdsapi.getzoneinfo(agent,zone,"serverIp")
        try:
            serverIp = zoneinfo[0]['serverIp']
        except:
            return jsonify(result="获取信息出错")
        serverinfo_list = [{"platformAlias":agent,"logPath":logpath,"serverIp":serverIp,"logTime":checkTime,"serverId":zone,"logCount":checknum}]
        phpLogCmdInfo = {"checkType":"phplog","cmd":"logoperate","serverinfo_list":serverinfo_list}
        phpLogCmd = json.dumps(phpLogCmdInfo) + "#zbcyh#"
        phpLogMsg = sendsocket.send_socket(phpLogCmd)
        phpLogMsgJson = json.loads(phpLogMsg)
        return jsonify(result=phpLogMsgJson['msg'])

@logs.route("/phpDownlogSubmit",methods=['GET','POST'])
@login_required
@permission_required("phplog")
def phpDownlogSubmit():
    agent = request.form['agentList']
    zone = request.form['checkzone']
    logpath = request.form['logsList']
    checkTime = request.form['checkTime']
    if agent.strip() == "" or zone.strip() == "" or logpath.strip() == "" or checkTime.strip() == "":
        return jsonify(result="信息填写不完整",code="1")
    else:
        zoneinfo = getmdsapi.getzoneinfo(agent,zone,"serverIp")
        try:
            serverIp = zoneinfo[0]['serverIp']
        except:
            return jsonify(result="获取信息出错",code="1")
        serverinfo_list = [{"platformAlias":agent,"logPath":logpath,"serverIp":serverIp,"logTime":checkTime,"serverId":zone,"webroot":current_app.config.get('PHPWEBROOT')}]
        phpLogDownInfo = {"checkType":"phpdownlog","cmd":"logoperate","serverinfo_list":serverinfo_list}
        phpLogDownCmd = json.dumps(phpLogDownInfo) + "#zbcyh#"
        phpLogDownMsg = sendsocket.send_socket(phpLogDownCmd)
        print phpLogDownMsg
        phpLogDownMsgJson = json.loads(phpLogDownMsg)
        if phpLogDownMsgJson['code'] == "0":
            GameFqdn = current_app.config.get('GAMEFQDN')
            GameName = current_app.config.get('GAMENAME')
            filename = phpLogDownMsgJson['filename']
            FullLink = "http://s%s.%s%s.%s/ProGetLog/%s" %(zone,agent,GameName,GameFqdn,filename)
            return jsonify(result=FullLink,code="0")
        else:
            return jsonify(result=FullLink,code="1")

@logs.route("/addphplogpath",methods=['GET','POST'])
@login_required
@permission_required("phplog")
def addphplogpath():
    if request.method == "POST":
        logPath = request.form['logpath']
        phplogpath = Phplogpath()
        phplogpath.path = logPath
        db.session.add(phplogpath)
        db.session.commit()
        return jsonify(result="true")
    else:
        return render_template('logs/addphplogpath.html')


@logs.route("/javalogManage",methods=['GET','POST'])
@login_required
@permission_required("javalog")
def javalogManage():
    javalogpaths = []
    javacmds = []
    Allagents = cache.get('all_plats')
    AllPaths = Javalogpath.query.all()
    for row in range(len(AllPaths)):
        javalogpaths.append(AllPaths[row].path)
    AllCmds = Javacmd.query.all()
    for row in range(len(AllCmds)):
        javacmds.append(AllCmds[row].cmd)
    AllInfo = {"allagents":json.loads(Allagents),"javalogpaths":javalogpaths,"javacmds":javacmds}
    return render_template('logs/javalogManage.html',AllInfo=AllInfo)

@logs.route("/addjavalogpath",methods=['GET','POST'])
@login_required
@permission_required("javalog")
def addjavalogpath():
    if request.method == "POST":
        javalogPath = request.form['logpath']
        javalogType = request.form['logtypeList']
        addjavalogPath = Javalogpath()
        addjavalogPath.path = javalogPath
        addjavalogPath.type = javalogType
        db.session.add(addjavalogPath)
        db.session.commit()
        return jsonify(result="true")
    else:
        return render_template('logs/addjavalogpath.html')

@logs.route("/javaChecklogSubmit",methods=['GET','POST'])
@login_required
@permission_required("javalog")
def javaChecklogSubmit():
    agent = request.form['agentList']
    zone = request.form['checkzone']
    checkTime = request.form['checkTime']
    checknum = request.form['checknum']
    logpath = request.form['logsList']
    if agent.strip() == "" or zone.strip() == "" or checkTime.strip() == "" or checknum.strip() == "" or logpath.strip() == "":
        return jsonify(result="信息填写不完整")
    else:
        logtype = Javalogpath.query.filter_by(path=logpath).first().type
        zoneinfo = getmdsapi.getzoneinfo(agent,zone,"serverIp,javaDir")
        try:
            serverIp = zoneinfo[0]['serverIp']
            javaDir = zoneinfo[0]['javaDir']
        except:
            return jsnoify(result="获取信息出错")
        GameName = current_app.config.get('GAMENAME')
        serverinfo_list = [{"platformAlias":agent,"logPath":logpath,"serverIp":serverIp,"logTime":checkTime,"serverId":zone,"logAccount":checknum,"logtype":logtype,"javaDir":javaDir,"gamename":GameName}]
        javaLogCheckCmdInfo = {"checkType":"checkjavalog","cmd":"logoperate","serverinfo_list":serverinfo_list}
        javaLogCheckCmd = json.dumps(javaLogCheckCmdInfo) + "#zbcyh#"
        javaLogCheckMsg = sendsocket.send_socket(javaLogCheckCmd)
        javaLogCheckMsgJson = json.loads(javaLogCheckMsg)
        return jsonify(result=javaLogCheckMsgJson['msg'])

@logs.route("/javaSearchlogSubmit",methods=['GET','POST'])
@login_required
@permission_required("javalog")
def javaSearchlogSubmit():
    agent = request.form['agentList']
    zone = request.form['checkzone']
    checkTime = request.form['checkTime']
    logpath = request.form['logsList']
    timeZone = request.form['timeZone']
    searchKey = request.form['Key']
    if agent.strip() == "" or zone.strip() == "" or checkTime.strip() == "" or logpath.strip() == "" or timeZone.strip() == "" or searchKey.strip() == "":
        return jsonify(result="信息填写不完整")
    else:
        logtype = Javalogpath.query.filter_by(path=logpath).first().type
        zoneinfo = getmdsapi.getzoneinfo(agent,zone,"serverIp,javaDir")
        try:
            serverIp = zoneinfo[0]['serverIp']
            javaDir = zoneinfo[0]['javaDir']
        except:
            return jsnoify(result="获取信息出错")
        GameName = current_app.config.get('GAMENAME')
        serverinfo_list = [{"platformAlias":agent,"logPath":logpath,"serverIp":serverIp,"logTime":checkTime,"serverId":zone,"key":searchKey,"logtype":logtype,"hour":timeZone,"javaDir":javaDir,"gamename":GameName}]
        javaLogSearchCmdInfo = {"checkType":"javasearchlog","cmd":"logoperate","serverinfo_list":serverinfo_list}
        javaLogSearchCmd = json.dumps(javaLogSearchCmdInfo) + "#zbcyh#"
        javaLogSearchMsg = sendsocket.send_socket(javaLogSearchCmd)
        javaLogSearchMsgJson = json.loads(javaLogSearchMsg)
        return jsonify(result=javaLogSearchMsgJson['msg'])

@logs.route("/javaCmdSubmit",methods=['GET','POST'])
@login_required
@permission_required("javalog")
def javaCmdSubmit():
    agent = request.form['agentList']
    zone = request.form['checkzone']
    javacmd = request.form['cmdList']
    javapid = request.form['javapid']
    if javacmd.strip() != "":
        if javacmd.strip() == "jps -l":
            if agent.strip() == "" or zone.strip() == "":
                return jsonify(result="信息填写不完整")
        else:
            if agent.strip() == "" or zone.strip() == "" or javapid.strip() == "":
                return jsonify(result="信息填写不完整")
    else:
        return jsonify(result="信息填写不完整")
    zoneinfo = getmdsapi.getzoneinfo(agent,zone,"serverIp")
    try:
        serverIp = zoneinfo[0]['serverIp']
    except:
        return jsonify(result="获取信息出错")
    
    if javacmd.strip() == "jps -l":
        execcommand = "/usr/local/java/bin/%s" %(javacmd.strip())
    elif javacmd.strip() == "jstat -gcutil":
        execcommand = "/usr/local/java/bin/%s %s 1000 5" %(javacmd.strip(),javapid.strip())
    else:
        execcommand = "/usr/local/java/bin/%s %s" %(javacmd.strip(),javapid.strip())
    serverinfo_list = [{"platformAlias":agent,"serverIp":serverIp,"serverId":zone,"execcommand":execcommand,"javapid":javapid}]
    javaCmdInfo = {"checkType":"ExecCommand","cmd":"logoperate","serverinfo_list":serverinfo_list}
    javaCmd = json.dumps(javaCmdInfo) + "#zbcyh#"
    javaCmdMsg = sendsocket.send_socket(javaCmd)
    javaCmdMsgJson = json.loads(javaCmdMsg)
    return jsonify(result=javaCmdMsgJson['msg'])

@logs.route("/javaDownlogSubmit",methods=['GET','POST'])
@login_required
@permission_required("javalog")
def javaDownlogSubmit():
    agent = request.form['agentList']
    zone = request.form['checkzone']
    logpath = request.form['logsList']
    checkTime = request.form['checkTime']
    checkTimeZone = request.form['timeZone']
    if agent.strip() == "" or zone.strip() == "" or logpath.strip() == "" or checkTime.strip() == "" or checkTimeZone.strip() == "":
        return jsonify(result="信息填写不完整",code="1")
    else:
        logtype = Javalogpath.query.filter_by(path=logpath).first().type
        zoneinfo = getmdsapi.getzoneinfo(agent,zone,"serverIp,javaDir")
        try:
            serverIp = zoneinfo[0]['serverIp']
            javaDir = zoneinfo[0]['javaDir']
        except:
            return jsonify(result="获取信息出错",code="1")
        GameFqdn = current_app.config.get('GAMEFQDN')
        GameName = current_app.config.get('GAMENAME')
        serverinfo_list = [{"platformAlias":agent,"logPath":logpath,"serverIp":serverIp,"logTime":checkTime,"serverId":zone,"webroot":current_app.config.get('PHPWEBROOT'),"checkTimeZone":checkTimeZone,"javaDir":javaDir,"gamename":GameName,"logtype":logtype}]
        javaLogDownInfo = {"checkType":"javadownlog","cmd":"logoperate","serverinfo_list":serverinfo_list}
        javaLogDownCmd = json.dumps(javaLogDownInfo) + "#zbcyh#"
        javaLogDownMsg = sendsocket.send_socket(javaLogDownCmd)
        print javaLogDownMsg
        javaLogDownMsgJson = json.loads(javaLogDownMsg)
        if javaLogDownMsgJson['code'] == "0":
            filename = javaLogDownMsgJson['filename']
            FullLink = "http://s%s.%s%s.%s/ProGetLog/%s" %(zone,agent,GameName,GameFqdn,filename)
            return jsonify(result=FullLink,code="0")
        else:
            return jsonify(result=javaLogDownMsgJson['codemessage'],code="1")
