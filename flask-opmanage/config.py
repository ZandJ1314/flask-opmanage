# -*- coding: utf-8 -*-
import os,sys
reload(sys)
sys.setdefaultencoding('utf8')
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = 'Adfneiuae34877SDfekh378145u9aerjhzsd@Dfl834EWknaea'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = 'mysql://jqXMVeXg:dtvHpPx3Pw5yAzvTJZxi@127.0.0.1:5849/bxcq_yw?charset=utf8'
	#缓存类型
	CACHE_TYPE = 'filesystem'
	#缓存路径
	CACHE_DIR = 'cache'
	#游戏服WEB路径
	PHPWEBROOT = '/data/web_chroot/web'
	#游戏服域名
	GAMEFQDN = 'xhhd6.com'
	#游戏名字
	GAMENAME = 'bxcq'
	#游戏中文名
	GAMECHINESENAME = '不朽传奇'
	#游戏ID
	GAMEID = '27'
	#系统ID
	SYSTEMID = '27'
	#MDS sign
	MDSSIGN = 'I1pOOXvMvTKJ'
	#与控制台验证的key
	UPDATEKEY = 'xtLO15ded1@#J645R'
	#ywapi 白名单
	YWAPIWHITElIST = ['127.0.0.1']
	
	ALLPLATS = []

	DATASRCIP = '202.39.241.68'
	DATASRCPORT = '5849'
	DATASRCUSER = 'PpU2'
	DATASRCPASS = 'k61t628'


	SVNURL = 'http://116.62.9.14:9606/svn/bxcqrepos/'
	SVNUSERNAME = 'lhfs_update'
	SVNPASS = 'mo6iB_ZOcYAeT79ajl0YLwqCHNzi2F8b21c'
	
	

	#配置将日志写入文件
	@classmethod
	def init_app(cls,app):
		Config.init_app(app)
		import logging
		#from logging.handlers import TimedRotatingFileHandler
		from mlogging import TimedRotatingFileHandler_MP
		formatter = logging.Formatter('%(asctime)s level-%(levelname)-8s %(message)s')
		fileTimeHandler = TimedRotatingFileHandler_MP('logs/applog', "D", 1, 10)
		fileTimeHandler.suffix = "%Y%m%d.log"
		fileTimeHandler.setFormatter(formatter)
		fileTimeHandler.setLevel(logging.ERROR)
		app.logger.addHandler(fileTimeHandler)

config = {
	'default': DevelopmentConfig
}
