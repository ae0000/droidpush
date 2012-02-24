# -*- coding: utf-8 -*-
from mongokit import *
from flaskext.mongokit import MongoKit
from datetime import datetime
import os
import random
import hashlib
import base64
from droidpush import app

db = MongoKit(app)

def hash_password(password):
    salt = base64.urlsafe_b64encode(os.urandom(30))
    salt = unicode(salt)
    hash = hashlib.sha256(password + salt)
    hash = unicode(hash.hexdigest())

    return (salt, hash)

def check_password(raw_password, enc_password, salt):
    # first add the password from the form to the salt
    new_hash = hashlib.sha256(raw_password + salt)
    new_hash = unicode(new_hash.hexdigest())

    # check the new hash with the enc_password. we do this via a constant time
    # compare function to evade timing attacks.
    # see: http://codahale.com/a-lesson-in-timing-attacks/
    if len(enc_password) != len(new_hash):
        return False

    compare = 0
    for a, b in zip(enc_password, new_hash):
        compare |= ord(a) ^ ord(b)

    return compare == 0

class Apikey(Document):
    __collection__ = 'apikeys'
    __database__ = 'droidpush'

    structure = {
        'userid': unicode,
        'key': unicode,
        'name': unicode,
        'created': datetime,
        'accessed': int,
        'status': int
    }
    required_fields = ['userid', 'key', 'name', 'created', 'accessed', 'status']
    default_values = {
        'key': u''.join(random.choice('2345679ACDEFHJKLMNPRSTUVWXYZ') for i in xrange(32)),
        'name': u'Just the default apikey',
        'created': datetime.utcnow,
        'accessed': 0, 
        'status': 1
    }
    use_dot_notation = True

    # find the apikeys for a user
    def find_by_user(self, userid):
        return db.apikeys.find({"userid": userid, "status": 1})

    # validate that the apikey is owned by the given user
    def user_has_access_to_apikey(self, userid, apikeyid):
        return db.apikeys.find_one({
            "userid": userid, 
            "status": 1, 
            "_id": ObjectId(apikeyid) })


class User(Document):
    __collection__ = 'users'
    __database__ = 'droidpush'

    # this will store the user document data
    user_data = None

    structure = {
        'email': unicode,
        'password': unicode,
        'salt': unicode,
        'created': datetime,
        'status': int
    }
    required_fields = ['email', 'password', 'salt', 'created']
    default_values = {'created': datetime.utcnow, 'status': 1}
    use_dot_notation = True

    # this loads in the actual user (from the db)
    def set_data(self, user_data):
        self.user_data = user_data

    # load the user in via the user_id (_id)
    def load_user(self, userid):
        user_search = db.users.find_one({"_id": ObjectId(userid)})
        if user_search == None:
            return False
        else:
            self.set_data(user_search)
            return True

    # this is called by the forms to validate the login credentials
    def validate_login(self, email, raw_password):
        user_search = db.users.find_one({"email": email, "status": 1})
        if user_search == None:
            return None

        # we have found a user, lets get the password and salt
        enc_password = user_search['password']
        salt = user_search['salt']

        # check it via the model
        if check_password(raw_password, enc_password, salt):
            # User is all OK, save a copy of the user data into self
            self.set_data(user_search)
            return True
        else:
            return False

    # just returns the email address
    def get_email(self):
        if self.user_data != None:
            return self.user_data['email']
        else:
            return None

    # this function is required by the login manager
    def get_id(self):
        if self.user_data != None:
            #app.logger.error('id ' + vars(self.user_data['_id']))
            return str(self.user_data['_id'])
        else:
            return None

    # this function is required by the login manager
    def is_authenticated(self):
        if self.user_data != None and self.user_data['_id'] != None:
            return True;
        else:
            return False

    # this function is required by the login manager
    def is_active(self):
        if self.user_data != None and self.user_data['status'] == 1:
            return True;
        else:
            return False

    # this function is required by the login manager
    def is_anonymous(self):
        if self.user_data == None or self.user_data['_id'] == None:
            return True;
        else:
            return False