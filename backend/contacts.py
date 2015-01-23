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

