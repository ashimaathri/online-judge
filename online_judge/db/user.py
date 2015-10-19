import bcrypt
import hashlib

from pymongo import MongoClient
from db import db

user_collection = db['users']

class User(object):
    @staticmethod
    def exists(username):
        return user_collection.find_one({'username': username}) is not None

    def __init__(self, username, password=None, salt=None):
        user = user_collection.find_one({'username': username})

        if not user:
            # Create
            self.username = username
            self.salt = bcrypt.gensalt()
            self.password = hashlib.sha512(password + self.salt).hexdigest()
            self.save()
        else:
            # Load
            self.username = user['username']
            self.salt = user['salt']
            self.password = user['password']

    def save(self):
        user_collection.update_one({'username': self.username},
                                   {'$set': {'username': self.username, 'password': self.password, 'salt': self.salt}},
                                   True)

    def delete(self):
        user_collection.delete_one({'username': self.username})

    def verify(self, password):
        return self.password == hashlib.sha512(password + self.salt).hexdigest()
