"""
suppliers.py

Module that handles everything related to suppliers. Showing, Adding, Removing, etc.
"""

# Imports
import pymongo
import os.path
import logging
from bson.objectid import ObjectId
from bson import json_util
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

class AddSupplierHandler(BaseHandler) :
    def get(self) :
        suppliers = self.db.suppliers.find()
        self.render('add_edit_supplier.html', suppliers = suppliers, add_supplier = True)

    def post(self) :
        supplier_name = self.get_argument("SupplierName")
        supplier_logo = self.get_argument("SupplierLogo")
        supplier_wiki = self.get_argument("SupplierWiki")

        logging.info("Received %s, %s, %s" % (supplier_name, supplier_logo, supplier_wiki))

        supplier = {'supplier_name': supplier_name, "supplier_logo" : supplier_logo, "supplier_wiki" : supplier_wiki,
            "created_at": datetime.datetime.now(), "updated_at": datetime.datetime.now()}

        self.db.suppliers.insert(supplier)

        suppliers = self.db.suppliers.find()
        self.render('add_edit_supplier.html', suppliers = suppliers, add_supplier = True)
        
class EditSupplierHandler(BaseHandler) :
    def get(self, supplier_id) :
        supplier = self.db.suppliers.find_one({'_id': ObjectId(supplier_id)})
        suppliers = self.db.suppliers.find()
        self.render('add_edit_supplier.html', suppliers = suppliers, add_supplier = False, supplier_name =
            supplier["supplier_name"], supplier_logo = supplier["supplier_logo"], supplier_wiki = supplier["supplier_wiki"],
            supplier_id = str(supplier["_id"]))

    def post(self, zupplier_id) :
        supplier_name = self.get_argument("SupplierName")
        supplier_logo = self.get_argument("SupplierLogo")
        supplier_wiki = self.get_argument("SupplierWiki")
        supplier_id = self.get_argument("SupplierID")

        supplier = self.db.suppliers.find_one({'_id': ObjectId(supplier_id)})

        supplier["supplier_name"] = supplier_name
        supplier["supplier_logo"] = supplier_logo
        supplier["supplier_wiki"] = supplier_wiki
        supplier["updated_at"] = datetime.datetime.now()

        self.db.suppliers.save(supplier)

        suppliers = self.db.suppliers.find()
        self.render('add_edit_supplier.html', suppliers = suppliers, add_supplier = False, supplier_name =
                    supplier["supplier_name"], supplier_logo = supplier["supplier_logo"], supplier_wiki =
                    supplier["supplier_wiki"] ,supplier_id = str(supplier["_id"]))

class RemoveSupplierHandler(BaseHandler) :
    def get(self, supplier_id) :
        supplier = self.db.suppliers.remove({'_id': ObjectId(supplier_id)})
        self.redirect("/suppliers")

class ShowSuppliersHandler(BaseHandler) :
    def get(self) :
        suppliers = self.db.suppliers.find().sort('supplier_name', pymongo.ASCENDING)

        # Check if request is AJAX, if so return JSON, else return a nicely formatted page
        if self.request.headers.get('X-Requested-With') == "XMLHttpRequest" :
            # need tor ecudoce the MongoDB search resuls back to something usable for JSON
            my_suppliers = dict()
            for supplier in suppliers :
                supplier_id = str(supplier['_id'])
                my_suppliers[supplier_id] = supplier["supplier_name"]
            self.write(json_util.dumps(my_suppliers))
        else:
            self.render('suppliers.html', suppliers = suppliers)

