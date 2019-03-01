from flask import Blueprint

gmcommand = Blueprint('gmcommand',__name__)
from . import views