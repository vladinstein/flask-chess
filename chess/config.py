import json

with open('/etc/chess_config.json') as config_file:
        config = json.load(config_file)

class Config:
    SECRET_KEY = config.get('SECRET_KEY')
    SESSION_PERMANENT = True
    SESSION_TYPE ='filesystem'
    SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')