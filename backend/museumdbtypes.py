"""
museumdbtypes.py

Module that handles everything related to museum item types. Adding, Showing, Removing etc.
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
from  tornado.escape import json_decode
from  tornado.escape import json_encode

#MuseumDB imports

from base import *

type_classes = {    'item_type' : 'Model',
                    'system_type' : 'System',
                    'peripheral_type' : 'Peripheral',
                    'peripheral_class' : 'Peripheral class',
                    'storage_type' : 'Storage',
                    'media_type' : 'Media',
                    'documentation_type': 'Documentation'
                }

class ShowTypesHandler(BaseHandler) :
    def get(self) :
        # TODO: this method is a mess, is it a type_class, class_type, or something else?
        class_results = dict()
        for class_type, class_type_name in type_classes.iteritems():
            results = self.db.types.find({"type_class" : class_type})
            if results.count() > 0 :
                class_results[class_type] = results

        self.render('types.html', class_types = type_classes, class_results = class_results)
            
class AddTypeHandler(BaseHandler) :
    def get(self) :
        self.render('add_edit_type.html', class_types = type_classes, add_type = True)

    def post(self) :
        type_name = self.get_argument("TypeName")
        type_class = self.get_argument("TypeClass")

        new_type = {'type_class' : type_class, 'type_name': type_name}

        self.db.types.save(new_type)

        self.redirect("/add/type")

class RemoveTypeHandler(BaseHandler) :
    def get(self, type_id) :
        type_result = self.db.types.remove({'_id': ObjectId(type_id)})
        self.redirect("/types")

class ShowTypeClassesHandler(BaseHandler) :
    def get(self) :
        if self.request.headers.get('X-Requested-With') == "XMLHttpRequest" :
            # Return the base types with their short and long names
            # Base types are in the "Items" class, so look for everything called "item_type"
            results = self.db.types.find({"type_class" : "item_type"}).sort('type_name', pymongo.ASCENDING)
            base_types = dict()
            for result in results :
                type_name = result['type_name'].lower() + "_type"
                base_types[type_name] = result['type_name']
                
            self.write(json_util.dumps(base_types))
        else :
            # If not "ajaxy" redirect to types page
            self.redirect("/types")

class ShowTypeClassHandler(BaseHandler) :
    def get(self, type_class) :
        if self.request.headers.get('X-Requested-With') == "XMLHttpRequest" :
            # Find the specific base type values for the supplied type_class
            types = self.db.types.find({"type_class" : type_class})
            self.write(json_util.dumps(types))
        else :
            # If not "ajaxy" redirect to types page
            self.redirect("/types")
