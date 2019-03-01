from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.cache import Cache
from config import config

cache = Cache()
db = SQLAlchemy()


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'



def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)


	db.init_app(app)
	login_manager.init_app(app)

	cache.init_app(app)
	
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	from .user import user as user_blueprint
	app.register_blueprint(user_blueprint)

	from .role import role as role_blueprint
	app.register_blueprint(role_blueprint)

	from .permission import permission as permission_blueprint
	app.register_blueprint(permission_blueprint)

	from .logs import logs as logs_blueprint
	app.register_blueprint(logs_blueprint)

	from .ywtools import ywtools as ywtools_blueprint
	app.register_blueprint(ywtools_blueprint)

	from .serverlist import serverlist as serverlist_blueprint
	app.register_blueprint(serverlist_blueprint)

	from .openserver import openserver as openserver_blueprint
	app.register_blueprint(openserver_blueprint)

	from .shutdowngame import shutdowngame as shutdowngame_blueprint
	app.register_blueprint(shutdowngame_blueprint)

	from .gmcommand import gmcommand as gmcommand_blueprint
	app.register_blueprint(gmcommand_blueprint)

	from .checkver import checkver as checkver_blueprint
	app.register_blueprint(checkver_blueprint)

	from .api import api as api_blueprint
	app.register_blueprint(api_blueprint)

	from .sqlcommand import sqlcommand as sqlcommand_blueprint
	app.register_blueprint(sqlcommand_blueprint)
	
	from .setopentime import setopentime as setopentime_blueprint
	app.register_blueprint(setopentime_blueprint)

	return app	
