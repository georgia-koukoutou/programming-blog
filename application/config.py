import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "c434c9b7cf370b5f5f3f13a741bd9fab"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost/blog"

