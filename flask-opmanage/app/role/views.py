# -*- coding: utf-8 -*-
import sys,time,random
reload(sys)
sys.setdefaultencoding('utf8')
from flask import render_template, redirect, request, url_for, flash, session,jsonify,json,current_app
from flask.ext.login import login_user, logout_user, current_user
from . import role
from .. import db
from ..models import *
from ..decorators import permission_required,login_required

@role.route('/roleManage',methods=['GET','POST'])
@login_required
@permission_required("role")
def roleManage():
	return render_template('role/roleList.html')

@role.route('/listRole',methods=['GET','POST'])
@login_required
@permission_required("role")
def listRole():
	aaData = []
	AllRole = Role.query.all()
	for row in range(len(AllRole)):
		Rowdict = {}
		Rowdict['id'] = AllRole[row].id
		Rowdict['roleName'] = AllRole[row].roleName
		Rowdict['description'] = AllRole[row].description
		aaData.append(Rowdict)
	Result = {"aaData":aaData,"iTotalDisplayRecords":len(AllRole),"iTotalRecords":len(AllRole)}
	return jsonify(result=Result)

@role.route("/deleteRole",methods=['GET','POST'])
@login_required
@permission_required("role")
def deleteRole():
	RoleId = request.args.get('roleId')
	try:
		deleteRole = Role.query.filter_by(id=RoleId).first()
		db.session.delete(deleteRole)
		db.session.commit()
		return jsonify(result="true")
	except:
		return jsonify(result="flase")

@role.route('/addRoleSubmit',methods=['GET','POST'])
@login_required
@permission_required("role")
def addRoleSubmit():
    if request.method == "POST":
        roleName = request.form['roleName']
        roleDesc = request.form['description']
        role = Role.query.filter_by(roleName=roleName).first()
        if role is None:
            role = Role()
            role.roleName = roleName
            role.description = roleDesc
            role.createTime = time.time()
            db.session.add(role)
            db.session.commit()
            return jsonify(result="true")
        else:
            return jsonify(result="flase")
    else:
        return render_template('role/addRole.html')

@role.route("/assignPermission",methods=['GET','POST'])
@login_required
@permission_required("role")
def assignPermission():
	if request.method == "GET":
		RoleId = request.args.get('roleId')
		RolePerId = []
		AllPerId = Role_Permission.query.filter_by(roleId=RoleId).all()
		for row in range(len(AllPerId)):
			RolePerId.append(AllPerId[row].permissionId)
		TreeNodes = []
		AllPermission = Permission.query.all()
		for row in range(len(AllPermission)):
			RowPermissionDict = {}
			RowPermissionDict['id'] = int(AllPermission[row].id)
			if AllPermission[row].id in RolePerId:
				RowPermissionDict['checked'] = "true"
			if AllPermission[row].permissionName == "root":
				RowPermissionDict['pId'] = 0
			else:
				RowPermissionDict['pId'] = int(AllPermission[row].parentId)
			RowPermissionDict['name'] = AllPermission[row].permissionDesc
			TreeNodes.append(RowPermissionDict)
		AllInfo = {"TreeNodes":json.dumps(TreeNodes).decode("unicode-escape"),"roleId":RoleId}
		return render_template('role/assignPermission.html',AllInfo=AllInfo)
	else:
		RoleId = request.args.get('roleId')
		permIds = str(request.args.get('permIds'))
		AllRolePerm = Role_Permission.query.filter_by(roleId=RoleId).all()
		for row in range(len(AllRolePerm)):
			db.session.delete(AllRolePerm[row])
			db.session.commit()
		if permIds.strip() != "":
			AllPermid = permIds.split(',')
			for i in range(len(AllPermid)):
				SignPerm = Role_Permission()
				SignPerm.roleId = int(RoleId)
				SignPerm.permissionId = int(AllPermid[i])
				db.session.add(SignPerm)
				db.session.commit()
			return jsonify(result="true")
		else:
			return jsonify(result="true")


