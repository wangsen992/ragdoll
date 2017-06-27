"""
A simple draft for experimenting with a database construction.
"""

import pymongo
import bson

from .composite import *


# Implementing an adapter 
class DatabaseTarget(object):
    """
    This is the Target component for the adapter pattern on mongodb,
    in order to support different data structure from the database.

    Both ingredient and recipes can be search from this interface.
    """

    def __init__(self):

        pass

    def retrieve_item(self, item_id):

        pass

    def retrieve_list(self, selector):

        pass

    def insert_item(self, item):

        pass

    def update_item(self, item_id, item):

        pass

class UsdaAdapter(DatabaseTarget):

    def __init__(self, ingredient_collection):

        self.collection = ingredient_collection

    def retrieve_item(self, item_id):

        if type(item_id) != bson.objectid.ObjectId:
            item_id = bson.objectid.ObjectId(item_id)

        item = self.collection.find_one({'_id' : item_id})
        if not item:
            print("No item found")
            return None

        else:
            
        
        return item

    def retrieve_list(self, selector):







class Selector(object):

    def __init__(self, desc=None):

        self.desc = desc
        self.criteria = {}

    def add_filter(self, attr, value):

        self.criteria[attr] = value

    def remove_filter(self, attr):

        del self.criteria[attr]

    def __repr__(self):

        return self.desc + "\n" +  str(self.criteria)




# # define a pymongo class for handling connection to database. 
# # This one may not be necessary. 
# class MongoAdapter(pymongo.MongoClient):

#     def __init__(self, 
#                  host="localhost", 
#                  port=27017, 
#                  database='eatech',
#                  user=None, 
#                  password=None):

#         # Initialise connection with the database, obtain a MongoClient object
#         pymongo.MongoClient.__init__(self, host, port)
#         self.db = self[database]
#         self.db.authenticate(user, password)

#     def get_database(self, database, user=None, password=None):

#         pass


if __name__ == '__main__':
    
    pass

