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
        owner_contacts = self.db.contacts.find({'contact_owner' : "on"}).sort('contact_name', pymongo.ASCENDING)
        donor_contacts = self.db.contacts.find({'contact_donor' : "on"}).sort('contact_name', pymongo.ASCENDING)
        self.render('add_edit_item.html', add_item = True, owner_contacts = list(owner_contacts), donor_contacts = list(donor_contacts))

class ShowItemsHandler(BaseHandler) :
    def get(self) :
        items = list(self.db.items.find())
        self.render('items.html', items = items)
