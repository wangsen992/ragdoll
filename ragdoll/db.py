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

    Sub-classes should return in the format defined in composite.py.
    """

    def __init__(self):

        pass

    def retrieve_item(self, item_id):

        # Use id to retrieve documents of the item

        # construct the ingredient/meal item according to the format required

        # return a workable object

        pass

    def retrieve_list(self, selector):

        # Use the selector to retrieve a list of documents of the item

        # for each of the documents, format according to composite.py

        # return the list

        pass

    def insert_item(self, item):

        # given an object define as in composite.py, reconstruct the document
        # according to the specs of the particular collection

        pass

    def update_item(self, item_id, item):

        # given an object defined as in composite.py, update the document 
        # according to the specs of the particular collection.

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
            pass
        
        return item

    def retrieve_list(self, selector):

        pass

    def __meal_constructor(doc):

        pass

    def __ingredient_constructor(doc):

        pass






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

