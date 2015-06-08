"""
items.py

Module that handles everything related to museum items. Showing, Adding, Removing, etc.
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

class AddItemHandler(BaseHandler) :
    def get(self) :
        item_types = list(self.db.types.find({"type_class" : 'item_type'}))
        for item_type in item_types :
            logging.info("Types = %s" % str(item_type['type_name']))
        self.render('add_edit_item.html', item_types = item_types, add_item = True)

class ShowItemsHandler(BaseHandler) :
    def get(self) :
        items = list(self.db.items.find())
        self.render('items.html', items = items)
