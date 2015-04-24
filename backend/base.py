"""
base.py

Module that is the basis for all the Tornado HTPP request handlers
"""

# Imports
import pymongo
import os.path
import logging
from bson.objectid import ObjectId
import datetime

# Tornado imports
import torndb
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

