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
                        (r"/remove/type/([0-9a-z]+)", RemoveTypeHandler)
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        conn = pymongo.Connection()
        self.db = conn["MuseumDB"]

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

class IndexHandler(BaseHandler):
    def get(self):
        suppliers = self.db.suppliers.find().sort("updated_at", -1).limit(5)
        items = self.db.items.find().sort("updated_at", -1).limit(5)
        contacts = self.db.contacts.find().sort("updated_at", -1).limit(5)
        self.render('index.html', suppliers = suppliers, items = items, contacts = contacts)

class AddItemHandler(BaseHandler) :
    def get(self) :
        self.render('add.html')

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
        suppliers = self.db.suppliers.find()
        self.render('suppliers.html', suppliers = suppliers)

class AddContactHandler(BaseHandler) :
    def get(self) :
        self.render('add_edit_contact.html', add_contact = True)

    def post(self) :
        contact_name = self.get_argument("ContactName")
        contact_address = self.get_argument("ContactAddress")
        contact_city = self.get_argument("ContactCity")
        contact_country = self.get_argument("ContactCountry")
        contact_telnumber = self.get_argument("ContactTelNumber")
        contact_email = self.get_argument("ContactEmail")
        contact_url = self.get_argument("ContactURL")
        contact_comment = self.get_argument("ContactComment")
        contact_show = self.get_argument("ContactShow", False)
        contact_participant = self.get_argument("ContactParticipant", False)
        contact_owner = self.get_argument("ContactOwner", False)
        contact_donor = self.get_argument("ContactDonor", False)

        contact = { "contact_name" : contact_name, "contact_address" : contact_address, "contact_city" : contact_city,
            "contact_country" : contact_country, "contact_telnumber" : contact_telnumber, "contact_email" : contact_email,
            "contact_url" : contact_url, "contact_comment" : contact_comment, "contact_show" : contact_show,
            "contact_participant" : contact_participant, "contact_owner" : contact_owner, "contact_donor" : contact_donor,
            "created_at": datetime.datetime.now(), "updated_at": datetime.datetime.now()}

        self.db.contacts.insert(contact)

        self.redirect("/contacts")

class ShowContactsHandler(BaseHandler) :
    def get(self) :
        contacts = self.db.contacts.find()
        self.render('contacts.html', contacts = contacts)

class EditContactHandler(BaseHandler) :
    def get(self, contact_id) :
        contact = self.db.contacts.find_one({'_id': ObjectId(contact_id)})
        contacts = self.db.contacts.find()
        # TODO: this is getting unwieldy, rewrite it to contacts and a single contact or even just the list of contacts with
        # the contact_id to address the correct one with all the relevant data in the template....
        self.render('add_edit_contact.html', contacts = contact, add_contact = False,
            contact_name = contact["contact_name"], contact_address = contact["contact_address"], contact_city =
            contact["contact_city"], contact_country = contact["contact_country"], contact_telnumber =
            contact["contact_telnumber"], contact_email = contact["contact_email"], contact_url = contact["contact_url"],
            contact_comment = contact["contact_comment"], contact_show = contact["contact_show"], contact_participant =
            contact["contact_participant"], contact_owner = contact["contact_owner"], contact_donor =
            contact["contact_donor"], contact_id = str(contact["_id"]))

    def post(self, kontact_id) :
        contact_id = self.get_argument("ContactID")
        contact = self.db.contacts.find_one({'_id': ObjectId(contact_id)})

        contact["contact_name"] = self.get_argument("ContactName")
        contact["contact_address"] = self.get_argument("ContactAddress")
        contact["contact_city"] = self.get_argument("ContactCity")
        contact["contact_country"] = self.get_argument("ContactCountry")
        contact["contact_telnumber"] = self.get_argument("ContactTelNumber")
        contact["contact_email"] = self.get_argument("ContactEmail")
        contact["contact_url"] = self.get_argument("ContactURL")
        contact["contact_comment"] = self.get_argument("ContactComment")
        contact["contact_show"] = self.get_argument("ContactShow", False)
        contact["contact_participant"] = self.get_argument("ContactParticipant", False)
        contact["contact_owner"] = self.get_argument("ContactOwner", False)
        contact["contact_donor"] = self.get_argument("ContactDonor", False)

        supplier["updated_at"] = datetime.datetime.now()

        self.db.contacts.save(contact)

        contacts = self.db.contacts.find()
        # TODO: this is getting unwieldy, rewrite it to contacts and a single contact or even just the list of contacts with
        # the contact_id to address the correct one with all the relevant data in the template....
        self.render('add_edit_contact.html', contacts = contact, add_contact = False,
            contact_name = contact["contact_name"], contact_address = contact["contact_address"], contact_city =
            contact["contact_city"], contact_country = contact["contact_country"], contact_telnumber =
            contact["contact_telnumber"], contact_email = contact["contact_email"], contact_url = contact["contact_url"],
            contact_comment = contact["contact_comment"], contact_show = contact["contact_show"], contact_participant =
            contact["contact_participant"], contact_owner = contact["contact_owner"], contact_donor =
            contact["contact_donor"], contact_id = str(contact["_id"]))

class ShowModelsHandler(BaseHandler) :
    def get(self) :
        models = self.db.models.find()
        self.render('models.html', models = models)

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

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(MuseumDBApp())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
