from flask import Blueprint

logs = Blueprint('logs',__name__)
from . import views