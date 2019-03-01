from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask.ext.login import UserMixin, AnonymousUserMixin
from . import db, login_manager

class Combineserverlog(db.Model):
	__table__name = "combineserverlog"
	id = db.Column(db.Integer,primary_key=True)
	platformAlias = db.Column(db.String(255),nullable=True)
	serverId = db.Column(db.String(255),nullable=True)
	combineDate = db.Column(db.String(255),nullable=True)
	


class Physerverlist(db.Model):
	__table__name = "pyhserverlist"
	id = db.Column(db.Integer,primary_key=True)
	function = db.Column(db.String(255),nullable=True)
	changroup = db.Column(db.String(255),nullable=True)
	lip = db.Column(db.String(255),nullable=True)
	dip = db.Column(db.String(255),nullable=True)
	cip = db.Column(db.String(255),nullable=True)
	cpu = db.Column(db.String(255),nullable=True)
	mem = db.Column(db.String(255),nullable=True)
	hd = db.Column(db.String(255),nullable=True)
	room = db.Column(db.String(255),nullable=True)
	load = db.Column(db.Float,nullable=True)
	total = db.Column(db.Integer,nullable=True)
	desc = db.Column(db.String(255),nullable=True)
	isdeleted = db.Column(db.Integer,nullable=True)	

class Operationlog(db.Model):
	__table__name = "operationlog"
	id = db.Column(db.Integer,primary_key=True)
	batchSign = db.Column(db.String(255),nullable=True)
	callBackTime = db.Column(db.BigInteger,nullable=True)
	cmd = db.Column(db.String(255),nullable=True)
	cmdString = db.Column(db.String(255),nullable=True)
	gameName = db.Column(db.String(255),nullable=True)
	platformAlias = db.Column(db.String(255),nullable=True)
	result = db.Column(db.Integer,nullable=True)
	resultString = db.Column(db.String(255),nullable=True)
	sendDate = db.Column(db.String(255),nullable=True)
	sendTime = db.Column(db.BigInteger,nullable=True)
	sendUser = db.Column(db.String(255),nullable=True)
	serverId = db.Column(db.Integer,nullable=True)
	serverName = db.Column(db.String(255),nullable=True)
	sign = db.Column(db.String(255),nullable=True)
	state = db.Column(db.Integer,nullable=True)
	version = db.Column(db.String(255),nullable=True)


class Gmcommandlog(db.Model):
	__table__name = "gmcommandlog"
	id = db.Column(db.Integer,primary_key=True)
	batchsign = db.Column(db.String(255),nullable=True)
	senddate = db.Column(db.String(255),nullable=True)
	sendtime = db.Column(db.BigInteger,nullable=True)
	command = db.Column(db.String(255),nullable=True)
	senduser = db.Column(db.String(255),nullable=True)
	platform = db.Column(db.String(255),nullable=True)
	serverid = db.Column(db.Integer,nullable=True)
	result = db.Column(db.Integer,nullable=True)

class Javacmd(db.Model):
	__table__name = "javacmd"
	id = db.Column(db.Integer,primary_key=True)
	cmd = db.Column(db.String(255),nullable=False)


class Javalogpath(db.Model):
	__table__name = "javalogpath"
	id = db.Column(db.Integer,primary_key=True)
	path = db.Column(db.String(255),nullable=False)
	type = db.Column(db.String(255),nullable=False)

class Phplogpath(db.Model):
	__table__name = "phplogpath"
	id = db.Column(db.Integer,primary_key=True)
	path = db.Column(db.String(255),nullable=False)

class Role(db.Model):
	__tablename__ = "roles"
	id = db.Column(db.Integer,primary_key=True)
	createTime = db.Column(db.BigInteger)
	description = db.Column(db.String(255),nullable=True)
	roleName = db.Column(db.String(255),nullable=True)

class Permission(db.Model):
	__tablename__ = "permissions"
	id = db.Column(db.Integer,primary_key=True)
	createTime = db.Column(db.BigInteger,nullable=True)
	parentId = db.Column(db.Integer)
	permissionDesc = db.Column(db.String(255),nullable=True)
	permissionName = db.Column(db.String(255))
	permissionURL = db.Column(db.String(255),nullable=True)
	level = db.Column(db.Integer)


class Role_Permission(db.Model):
	__tablename__ = "role_permissions"
	id = db.Column(db.Integer,primary_key=True)
	permissionId = db.Column(db.Integer)
	roleId = db.Column(db.Integer)


class User(UserMixin,db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)
	createTime = db.Column(db.BigInteger)
	deleted = db.Column(db.Integer)
	password_hash = db.Column(db.String(128))
	roleId = db.Column(db.Integer)
	username = db.Column(db.String(255))
	
	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
