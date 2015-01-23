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

type_classes = {    'item_type' : 'Item',
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

        print "Submitting: class_types = %s,\nclass_results = %s" % (str(type_classes), str(class_results))
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
