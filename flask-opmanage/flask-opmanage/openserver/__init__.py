from flask import Blueprint

openserver = Blueprint('openserver',__name__)
from . import views