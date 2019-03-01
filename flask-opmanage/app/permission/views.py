# -*- coding: utf-8 -*-
import sys,time,random
reload(sys)
sys.setdefaultencoding('utf8')
from flask import render_template, redirect, request, url_for, flash, session,jsonify,json,current_app
from flask.ext.login import login_user, logout_user, current_user
from . import permission
from .. import db
from ..models import *
from ..decorators import permission_required,login_required


@permission.route("/permissionManage",methods=['GET','POST'])
@login_required
@permission_required("permission")
def permissionManage():
	return render_template('permission/permissionList.html')


@permission.route("/listPermission",methods=['GET','POST'])
@login_required
@permission_required("permission")
def listPermission():
	aaData = []
	AllPermission = Permission.query.all()
	for row in range(len(AllPermission)):
		RowPerDict = {}
		RowPerDict['id'] = AllPermission[row].id
		RowPerDict['parentId'] = AllPermission[row].parentId
		RowPerDict['permissionName'] = AllPermission[row].permissionName
		RowPerDict['permissionDesc'] = AllPermission[row].permissionDesc
		aaData.append(RowPerDict)
	PermissionResult = {"aaData":aaData,"iTotalDisplayRecords":len(AllPermission),"iTotalRecords":len(AllPermission)}
	return jsonify(result=PermissionResult)


@permission.route("/addPermissionSubmit",methods=['GET','POST'])
@login_required
@permission_required("permission")
def addPermissionSubmit():
    if request.method == "POST":
        parentName = request.form['permission.parentId']
        permissionName = request.form['permission.permissionName']
        permissionDesc = request.form['permission.permissionDesc']
        permissionLevel = request.form['permission.level']
        parentId = Permission.query.filter_by(permissionName=parentName).first().id
        permission = Permission()
        permission.createTime = int(time.time())
        permission.parentId = parentId
        permission.permissionDesc = permissionDesc
        permission.permissionName = permissionName
        permission.level = permissionLevel
        db.session.add(permission)
        db.session.commit()
        return jsonify(result="true")
    else:
        RootPer = []
        permiss = Permission.query.filter_by(level=1).all()
        for row in range(len(permiss)):
            RootPer.append(permiss[row].permissionName)
        return render_template("permission/addPermission.html",parseroles=RootPer)


@permission.route("/childPermissionManage",methods=['GET','POST'])
@login_required
@permission_required("permission")
def childPermissionManage():
	parentId = request.args.get('permissionId')
	return render_template("permission/childPermissionList.html",parentId=parentId)

@permission.route("/listChildPermission",methods=['GET','POST'])
@login_required
@permission_required("permission")
def listChildPermission():
	parentId = request.args.get('permissionId')
	aaData = []
	AllChildPermission = Permission.query.filter_by(parentId=parentId).all()
	for row in range(len(AllChildPermission)):
		RowChildDict = {}
		RowChildDict['id'] = AllChildPermission[row].id
		RowChildDict['parentId'] = AllChildPermission[row].parentId
		RowChildDict['permissionName'] = AllChildPermission[row].permissionName
		RowChildDict['permissionDesc'] = AllChildPermission[row].permissionDesc
		aaData.append(RowChildDict)
	PermissionChlidResult = {"aaData":aaData,"iTotalDisplayRecords":len(AllChildPermission),"iTotalRecords":len(AllChildPermission)}
	return jsonify(result=PermissionChlidResult)

@permission.route("/editPermissionSubmit",methods=['GET','POST'])
@login_required
@permission_required("permission")
def editPermissionSubmit():
    if request.method == "POST":
        permissionId = request.form['permission.id']
        permissionName = request.form['permission.permissionName']
        permissionDesc = request.form['permission.permissionDesc']
        permissionURL = request.form['permission.permissionURL']
        SignPermission = Permission.query.filter_by(id=permissionId).first()
        SignPermission.permissionName = permissionName
        SignPermission.permissionDesc = permissionDesc
        SignPermission.permissionURL = permissionURL
        db.session.commit()
        return jsonify(result="true")
    else:
        permissId = request.args.get('permissionId')
        return render_template("permission/editPermission.html",permissionId=permissId)

@permission.route("/deletePermission",methods=['GET','POST'])
@login_required
@permission_required("permission")
def deletePermission():
	permissId = request.args.get('permissionId')
	SignPermission = Permission.query.filter_by(id=permissId).first()
	db.session.delete(SignPermission)
	db.session.commit()
	return jsonify(result="true")


