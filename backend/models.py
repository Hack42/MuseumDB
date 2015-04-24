"""
models.py

Module that handles everything related to hardware models. Showing, Adding, Removing, etc.
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

#MuseumDB imports

from base import *

class AddModelHandler(BaseHandler) :
    def get(self) :
        #item_types = list(self.db.types.find({"type_class" : 'item_type'}))
        #for item_type in item_types :
        #    logging.info("Types = %s" % str(item_type['type_name']))
        
        # To add a model, the form needs to know all the suppliers
        # And all the base types
        self.render('add_edit_modes.html', add_model = True)

class ShowModelsHandler(BaseHandler) :
    def get(self) :
        models = list(self.db.models.find())
        self.render('models.html', models = models)
