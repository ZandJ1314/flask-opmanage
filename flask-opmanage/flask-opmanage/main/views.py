# -*- coding: utf-8 -*-
import sys,time,random
reload(sys)
sys.setdefaultencoding('utf8')
from flask import render_template, redirect, request, url_for, flash, session,jsonify,json,current_app
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import main
from .. import db
from .. import cache
from ..models import *
from ..mylibs import getmdsapi,loadztree


@main.route('/time',methods=['GET','POST'])
@cache.cached(timeout=5)
def currentTime():
	return time.time()


@main.route('/',methods=['GET','POST'])
def index():
	return render_template('main/login.html')

@main.route('/login',methods=['GET','POST'])
def login():
	if request.method == "POST":
		requestUsername = request.form['username']
		requestPassword = request.form['password']
		user = User.query.filter_by(username=requestUsername).first()
		if requestUsername == "" or requestPassword == "":
			return redirect(url_for('.index'))
		elif user is not None and user.verify_password(requestPassword):
			login_user(user)
			#将用户权限写入session
			PermissionsList = []
			RoleId = User.query.filter_by(username=current_user.username).first().roleId
			RolePerms = Role_Permission.query.filter_by(roleId=RoleId).all()
			for row in range(len(RolePerms)):
				PermissionsList.append(Permission.query.filter_by(id=RolePerms[row].permissionId).first().permissionName)
			session['permissons'] = PermissionsList
			current_app.logger.error("%s is logging and permission is %s" %(current_user.username,str(PermissionsList)))
			#将所有平台名写入缓存
			AllPlatsMsg = getmdsapi.getagent()
			if int(AllPlatsMsg['code']) == 0:
				cache.delete('all_plats')
				getmdsapi.cache_plats(json.dumps(AllPlatsMsg['Msg']))
				current_app.logger.error("AllPlatMsg is %s" %(str(AllPlatsMsg['Msg'])))
			loadztree.LoadyxZtree()
			DataInfo = {"username":requestUsername,"permissionList":session['permissons']}
			return render_template('main/authentication.html',DataInfo=DataInfo)
		else:
			flash('用户名或密码错误 !')
			return redirect(url_for('.index'))
	else:
		return redirect(url_for('.index'))




@main.route('/logout',methods=['GET','POST'])
@login_required
def logout():
	current_app.logger.error("%s is logout" %(current_user.username))
	logout_user()
	return redirect(url_for('.index'))

@main.route('/changePassword',methods=['GET','POST'])
@login_required
def changePassword():
	if request.method == "POST":
		oldPass = request.form['oldPassword']
		newPass = request.form['newPassword']
		confirmPass = request.form['confirmNewPassword']
		if confirmPass != newPass:
			flash('两次密码输入不正确！')
			return render_template('main/changePassword.html')
		else:
			user = User.query.filter_by(username=current_user.username).first()
			if user.verify_password(oldPass):
				user.password = newPass
				db.session.commit()
				flash('密码修改成功!')
				return render_template('main/changePassword.html')
			else:
				flash('原密码不正确!')
				return render_template('main/changePassword.html')
	else:
		return render_template('main/changePassword.html')
