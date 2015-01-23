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

#MuseumDB imports

from base import *

class ShowModelsHandler(BaseHandler) :
    def get(self) :
        models = self.db.models.find()
        self.render('models.html', models = models)

