# -*- coding: utf-8 -*-
import sys,time,random,traceback,os
from hashlib import md5
reload(sys)
sys.setdefaultencoding('utf8')
from flask import render_template, redirect, request, url_for, flash, session,jsonify,json,current_app
from flask.ext.login import login_user, logout_user,current_user
from ..decorators import login_required
from . import api
from .. import db
from .. import cache
from ..models import *
from ..mylibs import getmdsapi,sendsocket

@api.route("/ywapi/interface/combineserverlog",methods=['POST'])
def CombineServerLog():
	try:
		platformAlias = request.form['platformAlias']
		serverId = request.form['serverId']
		combineDate = request.form['combineDate']
		opType = request.form['opType']
		Sign = request.form['Sign']
		retime = request.form['retime']
		localSign = current_app.config.get('UPDATEKEY')
		signMd5 = md5(str(retime)+localSign).hexdigest().upper()
		if signMd5 == Sign:
			if opType == "select":
				combineInfo = Combineserverlog.query.filter_by(platformAlias=platformAlias,serverId=serverId,combineDate=combineDate).first()
				if combineInfo is None:
					return "0"
				else:
					return "1"
			elif opType == "insert":
				InsertCombineServerLog = Combineserverlog()
				InsertCombineServerLog.platformAlias = platformAlias
				InsertCombineServerLog.serverId = serverId
				InsertCombineServerLog.combineDate = combineDate
				db.session.add(InsertCombineServerLog)
				db.session.commit()
				return "0"
		else:
			current_app.logger.error("combineserverlog sign error")
	except:
		errorlog = traceback.format_exc()
		current_app.logger.error(errorlog)



@api.route("/ywapi/interface/OperationCallBack",methods=['GET','POST'])
def OperationCallBack():
	CallBackCode = request.form['code']
	CallBackMsg = request.form['codeMsg']
	CallBackSign = request.form['sign']
	try:
		Operationlog.query.filter_by(sign=CallBackSign).update(dict(result=CallBackCode,resultString=CallBackMsg))
		db.session.commit()
	except:
		errorlog = traceback.format_exc()
		current_app.logger.error(errorlog)
	return jsonify(result="true")

@api.route("/ywapi/interface/iplist",methods=['GET','POST'])
def Iplist():
	resultIps = []
	try:
		sign = request.form['sign']
		ips = request.form['ips']
		retime = request.form['time']
		fungroup = request.form['fungroup']
		localSign = current_app.config.get('UPDATEKEY')
		signMd5 = md5(str(retime)+localSign).hexdigest().upper()
		if signMd5 == sign:
			if ips == "all":
				if fungroup == "all":
					allIps = db.session.query(Physerverlist.dip,Physerverlist.cip).filter_by(isdeleted=0).all()
				else:
					allIps = db.session.query(Physerverlist.dip,Physerverlist.cip).filter_by(function=fungroup,isdeleted=0).all()
				for i in range(len(allIps)):
					resultIps.append(allIps[i].dip)
					resultIps.append(allIps[i].cip)
			elif ips == "dip":
				if fungroup == "all":
					allIps = db.session.query(Physerverlist.dip).filter_by(isdeleted=0).all()
				else:
					allIps = db.session.query(Physerverlist.dip).filter_by(function=fungroup,isdeleted=0).all()
				for i in range(len(allIps)):
					resultIps.append(allIps[i].dip)
			elif ips == "cip":
				if fungroup == "all":
					allIps = db.session.query(Physerverlist.cip).filter_by(isdeleted=0).all()
				else:
					allIps = db.session.query(Physerverlist.cip).filter_by(function=fungroup,isdeleted=0).all()
				for i in range(len(allIps)):
					resultIps.append(allIps[i].cip)

			return jsonify(code=0,msg="ok",data=resultIps)
		else:
			return jsonify(code=1,msg="key error")
	except:
		errorlog = traceback.format_exc()
		current_app.logger.error(errorlog)
		return jsonify(code=3,msg="get ips error")

@api.route("/ywapi/interface/collectload",methods=['GET','POST'])
def CollectLoad():
	gameServerIpsList = []
	try:
		sign = request.form['sign']
		retime = request.form['time']
		localSign = current_app.config.get('UPDATEKEY')
		signMd5 = md5(str(retime)+localSign).hexdigest()
		if signMd5 == sign:
			gameServerIps = db.session.query(Physerverlist.dip).filter_by(isdeleted=0,function="gameservers").all()
			for i in range(len(gameServerIps)):
				gameServerIpsList.append({"dip":gameServerIps[i].dip})
			nowTime = int(time.time())
			nowSignMd5 = md5(localSign+"get_loads"+str(nowTime)).hexdigest()
			remoteCmd = {"cmd":"get_loads","time":str(nowTime),"securitySign":nowSignMd5,"ips":gameServerIpsList}
			ipsLoad = sendsocket.send_socket(json.dumps(remoteCmd)+"#zbcyh#")
			ipsLoadJson = json.loads(ipsLoad)
			for i in range(len(ipsLoadJson)):
				loads = ipsLoadJson[i]['load']
				serverIp = ipsLoadJson[i]['serverIp']
				Physerverlist.query.filter_by(dip=serverIp).update(dict(load=loads))
				db.session.commit()
			return jsonify(code=0)
		else:
			return jsonify(code=1)
	except:
		errorlog = traceback.format_exc()
		current_app.logger.error(errorlog)
		return jsonify(code=3)

@api.route("/fileUpload",methods=['POST'])
@login_required
def fileUpload():
	try:
		f = request.files['file']
		f.save(os.path.join("upload",f.filename))
		return jsonify(code=0)
	except:
		errorlog = traceback.format_exc()
		current_app.logger.error(errorlog)
		return jsonify(code=2)

@api.route("/ywapi/interface/getzons", methods=['POST'])
def getzones():
    dbhost = '10.66.152.35'
    dbport = 5849
    dbuser = 'loginNV85q'
    dbpass = 'YNKFya9ReTN'
    dbname = 'txlhfs_mds'
    gamename = "'txlhfs'"
    agent = "'lhfsqq'"
    localzone = 1
    gamealias =  request.form['gamealias']
    platformalias = request.form['platformalias']
    iszone = request.form['iszone']
    try:
        db = MySQLdb.connect(host=dbhost, port=dbport, user=dbuser, passwd=dbpass, db=dbname)
        cursor = db.cursor()
        sql = 'SELECT gameAlias, platformAlias, serverId, openDate, iszone  FROM gameconfig WHERE gameAlias=%s AND platformAlias=%s AND iszone=%s' % (
            gamename, agent, localzone)
        cursor.execute(sql)
        results = cursor.fetchall()
        infos = []
        for info in results:
            if int(info[3]) == localzone:
                infos.insert(0, info)
                continue
            infos.append(info)
        db.close()
        return infos
    except:
        return 'errors'
