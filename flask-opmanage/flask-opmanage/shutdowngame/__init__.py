from flask import Blueprint

shutdowngame = Blueprint('shutdowngame',__name__)
from . import views