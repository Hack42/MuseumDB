"""
museumdb.py

Main application module. Start the application using "python museumdb.py"
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
from contacts import *
from items import *
from suppliers import *
from models import *
from museumdbtypes import *
from models import *

define("port", default=9999, help="run on the given port", type=int)

type_classes = {    'item_type' : 'Item',
                    'system_type' : 'System',
                    'peripheral_type' : 'Peripheral',
                    'peripheral_class' : 'Peripheral class',
                    'storage_type' : 'Storage',
                    'media_type' : 'Media',
                    'documentation_type': 'Documentation'
                }

class MuseumDBApp(tornado.web.Application) :
    def __init__(self):
        handlers =  [   (r"/", IndexHandler),
                        (r'/favicon.ico', tornado.web.StaticFileHandler, {'path': './static/assets/ico/favicon.ico'}),
                        (r'/assets/(.*)', tornado.web.StaticFileHandler, {'path': './static/assets/'}),
                        (r"/add", AddItemHandler),
                        (r"/suppliers", ShowSuppliersHandler),
                        (r"/add/supplier", AddSupplierHandler),
                        (r"/edit/supplier/([0-9a-z]+)", EditSupplierHandler),
                        (r"/remove/supplier/([0-9a-z]+)", RemoveSupplierHandler),
                        (r"/contacts", ShowContactsHandler),
                        (r"/add/contact", AddContactHandler),
                        (r"/edit/contact/([0-9a-z]+)", EditContactHandler),
                        (r"/models", ShowModelsHandler),
                        (r"/types", ShowTypesHandler),
                        (r"/add/type", AddTypeHandler),
                        (r"/remove/type/([0-9a-z]+)", RemoveTypeHandler),
                        (r"/items", ShowItemsHandler),
                        (r"/add/item", AddItemHandler),
                        (r"/models", ShowModelsHandler),
                        (r"/add/model", AddModelHandler)
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        conn = pymongo.Connection()
        self.db = conn["MuseumDB"]

class IndexHandler(BaseHandler):
    def get(self):
        suppliers = self.db.suppliers.find().sort("updated_at", -1).limit(5)
        items = self.db.items.find().sort("updated_at", -1).limit(5)
        contacts = self.db.contacts.find().sort("updated_at", -1).limit(5)
        self.render('index.html', suppliers = suppliers, items = items, contacts = contacts)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(MuseumDBApp())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
