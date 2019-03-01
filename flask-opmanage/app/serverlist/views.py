# -*- coding: utf-8 -*-
import sys,time,random
reload(sys)
sys.setdefaultencoding('utf8')
from flask import render_template, redirect, request, url_for, flash, session,jsonify,json,current_app
from flask.ext.login import login_user, logout_user,current_user
from . import serverlist
from .. import db
from ..models import *
from ..decorators import permission_required,login_required
from ..mylibs import sendsocket,getmdsapi,loadztree,minitool

@serverlist.route("/phyServerManage",methods=['GET','POST'])
@login_required
@permission_required("servermanager")
def phyServerManage():
    localIP = []
    serverIp = []
    unionIp = []
    gameIp = []
    AllLocalIp = db.session.query(Physerverlist.lip).filter_by(isdeleted=0).group_by(Physerverlist.lip).all()
    AllServerIp = db.session.query(Physerverlist.dip).filter_by(isdeleted=0).group_by(Physerverlist.dip).all()
    AllUnionIP = db.session.query(Physerverlist.cip).filter_by(isdeleted=0).group_by(Physerverlist.cip).all()
    AllGameIp = db.session.query(Physerverlist.dip).filter_by(isdeleted=0,function="gameservers").group_by(Physerverlist.dip).all()
    for b in range(len(AllLocalIp)):
        localIP.append(AllLocalIp[b].lip)
    for b in range(len(AllServerIp)):
        serverIp.append(AllServerIp[b].dip)
    for b in range(len(AllUnionIP)):
        unionIp.append(AllUnionIP[b].cip)
    for b in range(len(AllGameIp)):
        gameIp.append(AllGameIp[b].dip)

    MdsServersMsg = getmdsapi.getallserver()
    if int(MdsServersMsg['code']) == 0:
        MdsAllIps = {}
        MdsServers = MdsServersMsg['Msg']
        for xi in range(len(gameIp)):
            MdsAllIps[gameIp[xi]] = []
        for xi in range(len(MdsServers)):
            #去掉已合服的区服
            if str(MdsServers[xi]['isCombined']).upper() == "FALSE":
                try:
                    MdsAllIps[MdsServers[xi]['serverIp']].append("%s:%s" %(MdsServers[xi]['platformAlias'],str(MdsServers[xi]['serverId'])))
                except:
                    pass
        for key in MdsAllIps:
            CurrServer = Physerverlist.query.filter_by(dip=key).first()
            CurrServer.total = len(MdsAllIps[key])
            CurrServer.desc = json.dumps(MdsAllIps[key])
            db.session.commit()

        return render_template('serverlist/phyServerList.html',AllInfo={"localIp":localIP,"serverIp":serverIp,"unionIp":unionIp})
    else:
        current_app.logger.error("获取mds区服表出错")
        return render_template('serverlist/phyServerList.html',AllInfo={"localIp":localIP,"serverIp":serverIp,"unionIp":unionIp})


@serverlist.route("/addServer",methods=['GET','POST'])
@login_required
@permission_required("servermanager")
def addServer():
    return render_template('serverlist/addPhyServer.html')

@serverlist.route("/addServerSubmit",methods=['GET','POST'])
@login_required
@permission_required("servermanager")
def addServerSubmit():
    S_function = request.form['server.serverGroup']
    S_changroup = request.form['server.chanGroup']
    S_lip = request.form['server.localIp']
    S_ip = request.form['server.serverIp']
    S_cip = request.form['server.unionIp']
    S_cpu = request.form['server.cpu']
    S_mem = request.form['server.mem']
    S_hd = request.form['server.hd']
    S_room = request.form['server.serverRoom']
    S_desc = request.form['server.description']
    add_server = Physerverlist()
    add_server.function = S_function
    add_server.changroup = S_changroup
    add_server.lip = S_lip
    add_server.dip = S_ip
    add_server.cip = S_cip
    add_server.cpu = S_cpu
    add_server.mem = S_mem
    add_server.hd = S_hd
    add_server.room = S_room
    add_server.desc = S_desc
    add_server.load = 0.0
    add_server.total = 0
    add_server.isdeleted = 0
    db.session.add(add_server)
    db.session.commit()
    return jsonify(result="true")

@serverlist.route("/editServer",methods=['GET','POST'])
@login_required
@permission_required("servermanager")
def editServer():
    if request.method == "GET":
        editServer = {}
        serverId = request.args.get('serverId')
        oneServerInfo = Physerverlist.query.filter_by(id=int(serverId)).first()
        editServer['id'] = serverId
        editServer['lip'] = oneServerInfo.lip
        editServer['dip'] = oneServerInfo.dip
        editServer['cip'] = oneServerInfo.cip
        editServer['room'] = oneServerInfo.room
        editServer['desc'] = oneServerInfo.desc
        editServer['cpu'] = oneServerInfo.cpu
        editServer['mem'] = oneServerInfo.mem
        editServer['hd'] = oneServerInfo.hd
        return render_template('serverlist/editPhyServer.html',editServer=editServer)
    elif request.method == "POST":
        S_id = request.form['server.id']
        S_lip = request.form['server.localIp']
        S_dip = request.form['server.serverIp']
        S_cip = request.form['server.unionIp']
        S_cpu = request.form['server.cpu']
        S_mem = request.form['server.mem']
        S_hd = request.form['server.hd']
        S_room = request.form['server.serverRoom']
        S_desc = request.form['server.description']
        CurrServer = Physerverlist.query.filter_by(id=int(S_id)).first()
        CurrServer.lip = S_lip
        CurrServer.dip = S_dip
        CurrServer.cip = S_cip
        CurrServer.cpu = S_cpu
        CurrServer.mem = S_mem
        CurrServer.hd = S_hd
        CurrServer.room = S_room
        CurrServer.desc = S_desc
        CurrServer.isdeleted = 0
        db.session.commit()
        return jsonify(result="true")
@serverlist.route("/deleteServer",methods=['GET','POST'])
@login_required
@permission_required("servermanager")
def deleteServer():
    serverId = request.args.get('serverId')
    CurrSer = Physerverlist.query.filter_by(id=int(serverId)).first()
    CurrSer.isdeleted = 1
    db.session.commit()
    return jsonify(result="true")

@serverlist.route("/listPhyServer",methods=['GET','POST'])
@login_required
@permission_required("servermanager")
def listPhyServer():
    filterStr = "isdeleted=0"
    if request.form['functionGroup'] != "groups":
        filterStr = "%s and function='%s'" %(filterStr,request.form['functionGroup'])
    if request.form['chanGroup'] != "all":
        filterStr = "%s and changroup='%s'" %(filterStr,request.form['chanGroup'])
    if request.form['localIp'] != "lip":
        filterStr = "%s and lip='%s'" %(filterStr,request.form['localIp'])
    if request.form['serverIp'] != "dip":
        filterStr = "%s and dip='%s'" %(filterStr,request.form['serverIp'])
    if request.form['unionIp'] != "uip":
        filterStr = "%s and cip='%s'" %(filterStr,request.form['unionIp'])
    aaData = []
    AllData = db.session.execute("select * from physerverlist where %s order by `load` asc,`total` asc" %(filterStr)).fetchall()
    for row in range(len(AllData)):
        RowServerDict = {}
        RowServerDict['id'] = AllData[row].id
        RowServerDict['localIp'] = AllData[row].lip
        RowServerDict['serverIp'] = AllData[row].dip
        RowServerDict['unionIp'] = AllData[row].cip
        RowServerDict['cpu'] = AllData[row].cpu
        RowServerDict['mem'] = AllData[row].mem
        RowServerDict['hd'] = AllData[row].hd
        RowServerDict['serverRoom'] = AllData[row].room
        RowServerDict['load'] = AllData[row].load
        RowServerDict['total'] = AllData[row].total
        RowServerDict['description'] = AllData[row].desc
        aaData.append(RowServerDict)
    ServerResult = {"aaData":aaData,"iTotalDisplayRecords":len(AllData),"iTotalRecords":len(AllData)}
    return jsonify(result=json.dumps(ServerResult))
