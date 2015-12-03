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

    def post(self) :
        item = dict()

        item['model_supplier'] = self.get_argument('ModelSupplier')
        item['model_id'] = self.get_argument('ItemModel')
        item['owner_contact_id'] = self.get_argument('OwnerContactID')
        item['donor_contact_id'] = self.get_argument('DonorContactId')
        item['date_in_collection'] = self.get_argument('InCollectionDate')
        item['serial_number'] = self.get_argument('SerialNumber')

        item["updated_at"] = datetime.datetime.now()

        self.db.items.insert(item)

        self.redirect("/items")

class ShowItemsHandler(BaseHandler) :
    def get(self) :
        items = list(self.db.items.find())

        # The basic items contain very little printable data, so enricht each item in the list with their supplier/model data
        # So we can build a usefull list of items
        for item in items :
            item['model'] = self.db.models.find_one({'_id': ObjectId(item['model_id'])})
            item['supplier'] = self.db.suppliers.find_one({'_id': ObjectId(item['model_supplier'])})

        self.render('items.html', items = items)
