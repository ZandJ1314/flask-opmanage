# -*- coding: utf-8 -*-
import sys,time,random
reload(sys)
sys.setdefaultencoding('utf8')
from flask import render_template, redirect, request, url_for, flash, session,jsonify,json,current_app
from flask.ext.login import login_user, logout_user, current_user
from . import user
from .. import db
from ..models import *
from ..decorators import permission_required,login_required

@user.route("/userManage",methods=['GET','POST'])
@login_required
@permission_required("user")
def userManage():
    return render_template('user/userList.html')

@user.route("/listUser",methods=['GET','POST'])
@login_required
@permission_required("user")
def listUser():
	aaData = []
	AllUser = User.query.all()
	for row in range(len(AllUser)):
		RowUserDict = {}
		RowUserDict['id'] = AllUser[row].id
		RowUserDict['username'] = AllUser[row].username
		RowUserDict['roleName'] = Role.query.filter_by(id=AllUser[row].roleId).first().roleName
		RowUserDict['createTime'] = AllUser[row].createTime
		aaData.append(RowUserDict)
	UserResult = {"aaData":aaData,"iTotalDisplayRecords":len(AllUser),"iTotalRecords":len(AllUser)}
	#current_app.logger.error(str(UserResult))
	return jsonify(result=UserResult)

@user.route('/addUserSubmit',methods=['GET','POST'])
@login_required
@permission_required("user")
def addUserSubmit():
    if request.method == "POST":
        UserRoleName = request.form['user.roleId']
        UserRoleId = Role.query.filter_by(roleName=UserRoleName).first().id
        user= User()
        user.createTime = int(time.time())
        user.password = request.form['user.password']
        user.deleted = 0
        user.username = request.form['user.username']
        user.roleId = UserRoleId
        db.session.add(user)
        db.session.commit()
        return jsonify(result="true")
    else:
        Roles = []
        AllRoles = Role.query.all()
        for row in range(len(AllRoles)):
            Roles.append(AllRoles[row].roleName)
        return render_template('user/addUser.html',roles=Roles)

@user.route("/deleteUser",methods=['GET','POST'])
@login_required
@permission_required("user")
def deleteUser():
	UserId = request.args.get('userId')
	try:
		deleteUser = User.query.filter_by(id=UserId).first()
		db.session.delete(deleteUser)
		db.session.commit()
		return jsonify(result="true")
	except:
		return jsonify(result="flase")

@user.route("/editUserSubmit",methods=['GET','POST'])
@login_required
@permission_required("user")
def editUserSubmit():
    if request.method == "POST":
        if request.form['user.password'] == request.form['confirmPassword']:
            CurrUser = User.query.filter_by(username=request.form['user.username']).first()
            CurrUser.password = request.form['confirmPassword']
            db.session.commit()
            return jsonify(result="true")
        else:
            return jsonify(result="flase")
    else:
        UserId = request.args.get('userId')
        UserName = User.query.filter_by(id=UserId).first().username
        info = {"username":UserName}
        return render_template('user/editUser.html',info=info)
