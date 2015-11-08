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
        suppliers = self.db.suppliers.find()
        
        # Item base and subtypes are loaded dynamically on page load using Ajax 
        
        self.render('add_edit_model.html', add_model = True, suppliers = suppliers)

    def post(self) :
        model_id = self.get_argument("ModelID", None, True)
        if model_id :
            model = self.db.models.find_one({'_id': ObjectId(model_id)})
        else :
            model = dict()

        model["type_class"] = self.get_argument("TypeClass");
        model["sub_type_class"] = self.get_argument("SubTypeClass");
        model["supplier_id"] = self.get_argument("SupplierID");
        model["model_name"] = self.get_argument("ModelName");

        model["created_at"] = datetime.datetime.now()
        model["updated_at"] = datetime.datetime.now()

        if model_id :
            self.db.models.save(model)
        else :
            self.db.models.insert(model)

        # From needs a list of the available suppliers
        #suppliers = self.db.suppliers.find()
        #self.render('add_edit_model.html', add_model = False, suppliers = suppliers, model = model)

        self.redirect("/models")

       
class EditModelHandler(BaseHandler) :
    def get(self, model_id) :
        model = self.db.models.find_one({'_id': ObjectId(model_id)})
        suppliers = self.db.suppliers.find()

        self.render('add_edit_model.html', add_model = False, suppliers = suppliers, model = model)

    def post(self, post_model_id) :
        model_id = self.get_argument("ModelID", None, True)
        model = self.db.models.find_one({'_id': ObjectId(model_id)})
        model["type_class"] = self.get_argument("TypeClass");
        model["sub_type_class"] = self.get_argument("SubTypeClass");
        model["supplier_id"] = self.get_argument("SupplierID");
        model["model_name"] = self.get_argument("ModelName");

        model["updated_at"] = datetime.datetime.now()

        self.db.models.save(model)

        #suppliers = self.db.suppliers.find()
        #self.render('add_edit_model.html', add_model = False, suppliers = suppliers, model = model)

        self.redirect("/models")


class ShowModelsHandler(BaseHandler) :
    def get(self) :
        models = list(self.db.models.find())
        self.render('models.html', models = models)
