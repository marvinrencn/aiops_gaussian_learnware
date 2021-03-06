# -*- coding=utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))

ENV = os.getenv("FLASK_ENV")
DEBUG = ENV == "development"
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", 'mysql+mysqlconnector://root:root@localhost:3306/giraffe')
SQLALCHEMY_TRACK_MODIFICATIONS = False

