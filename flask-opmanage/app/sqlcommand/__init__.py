from flask import Blueprint

sqlcommand = Blueprint('sqlcommand',__name__)
from . import views