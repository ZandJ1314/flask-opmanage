from flask import Blueprint

checkver = Blueprint('checkver',__name__)
from . import views