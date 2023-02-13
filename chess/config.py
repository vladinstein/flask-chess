import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_PERMANENT = True
    SESSION_TYPE ='filesystem'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')