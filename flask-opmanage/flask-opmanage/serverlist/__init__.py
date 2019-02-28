from flask import Blueprint

serverlist = Blueprint('serverlist',__name__)
from . import views