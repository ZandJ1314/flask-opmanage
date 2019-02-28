# -*- coding: utf-8 -*-
import sys, time, random

reload(sys)
sys.setdefaultencoding('utf8')
from flask import render_template, redirect, request, url_for, flash, session, jsonify, json, current_app
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import checkver
from .. import db
from .. import cache
from ..models import *
from ..decorators import permission_required
from ..mylibs import sendsocket, getmdsapi, loadztree, minitool,GetJavaVer,getjavavers


@checkver.route("/actioncheckver", methods=['POST'])
@login_required
@permission_required("checkversion")
def checkverSubmit():
    ResultListVer = getjavavers.getinfo()
    current_app.logger.error(str(ResultListVer))
    return jsonify(result="true", resultList=ResultListVer)


@checkver.route("/checkver", methods=['GET', 'POST'])
@login_required
@permission_required("checkversion")
def checkver():
    return render_template('checkver/checkVer.html')
