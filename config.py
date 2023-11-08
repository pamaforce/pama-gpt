# MySQL数据库配置
class BaseConfig:
	DIALECT = 'mysql'
	DRIVER = 'pymysql'
	HOST = '127.0.0.1'
	PORT = '3306'
	USERNAME = 'root'
	PASSWORD = '20030507oy'
	DATABASE = 'pama_gpt'
	SECRET_KEY = 'pamaforce'
	POE_TOKEN = 'xsSXUIfoF2KJt80Ox_lIvw=='
	# mysql不识别utf-8，需要直接写成utf8
	SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
	# SQLALCHEMY_DATABASE_URI = f"{DIALECT}+{DRIVER}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset=utf8"
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	# SQLALCHEMY_ECHO = True
