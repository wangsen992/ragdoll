"""
A simple draft for experimenting with a database construction.
"""
import os
import pymongo

import numpy as np
import pandas as pd

from bson.objectid import ObjectId


# Implementing an adapter
class MongoDB(object):
    """MongoDB connection and support requests

    
    """

    def __init__(self, 
                 host="localhost", 
                 port=27017, 
                 database="mydatabase",
                 user=None,
                 password=None,
                 collections=['USDA','FM','shiwuku']):
        """Initiation with Mongodb databases

        Parameters
        ----------
        Refer to pymongo.MongoClient

        """
        client = pymongo.MongoClient(host=host, port=port)
        self.database = client[database]
        if bool(user) & bool(password):
            self.database.authenticate(name=user, password=password)

        col_list = self.database.collection_names()
        if (set(collections) <= set(col_list)) == False:
            raise Exception('Invalid database name in collections.')
        self.collections = collections


    def retrieve_item(self, col_name, item_id):
        """Retrieve item as original doc"""

        # check if the given col_name is provided at initiation. 
        if col_name not in self.collections:
            raise ValueError("col_name {} not in self.collections.".format(col_name))
        
        # Use id to retrieve document of the item

        collection = self.database[col_name]
        doc = collection.find_one({'_id': ObjectId(item_id)})

        return doc


    def retrieve_list(self, selector):

        # Use the selector to retrieve a list of documents of the item
        # for each of the documents, format according to composite.py
        # return the list

        def viaName(str):

            '''
            Fuzzy search for name string matching (case insensitive).

            For English fuzzy search, insert string seperated with space. eg: 'Butter salt'
                Generated query: {'name.long': {'$regex': '^(?=.*Butter)(?=.*salt).+', '$options': 'i'}}
            Return: any object whose name contains all keywords in any order.
            Chinese fuzzy search not defined yet.

            TODO: 
            Search suggestions: split sentence into words and compare words with high frequency dictionary, 
                give close words search when original word is not available.

            '''

            path = 'name.long' 
            regexStr = '^'+''.join(['(?=.*'+word+')' for word in str.split(' ')])+'.+'

            def queryGen(str):

                query = {}
                query[path] = {}
                query[path]['$regex'] = str
                query[path]['$options'] = 'i'
                
                return query

            query = queryGen(regexStr)

            return query


        def viaRange(nutrients):
            
            # DIY contains materials not nutrients, not available right now

            '''
            Query example: 
            cur = db.USDA.find({'nutrients': { '$all': [{ '$elemMatch' : {'abbr' : tag1, 'value' : val1}},
                                                        { '$elemMatch' : {'abbr' : tag2, 'value' : val2}}
                                                        ]}},
                               {'_id' : 1, 'nutrients' : 1})
            '''

            def queryGen(nuts, fuzzySearch=True, fltPct=0.1):
                '''
                Fuzzy search enabled by default for accurate values.
                fltPct: floating value (percentage).
                '''
                query = {}
                query['nutrients'] = {}
                query['nutrients']['$all'] = []

                for nutInfo in nuts:
                    new_nutInfo = nutInfo.copy()
                    val = new_nutInfo['value']
                    
                    # range (only support a valid range eg [10, 20] yet)
                    if type(val) == list:
                        new_nutInfo['value'] = {'$gt':val[0], '$lt':val[1]}
                    # single value
                    elif type(val) == int or type(val) == float:
                        if fuzzySearch:
                            new_nutInfo['value'] = {'$gt':(1-fltPct)*val, '$lt':(1+fltPct)*val}
                    else:
                        raise Exception('Insert a value or a range to search.')
                    
                    subdict = {}
                    subdict['$elemMatch'] = new_nutInfo
                    query['nutrients']['$all'].append(subdict.copy())

                return query

            query = queryGen(nutrients)

            return query


        def viaTag(reqDict):

            '''
            eg: {'group':'乳类', 'tag':'高脂肪'}
            '''
            
            return reqDict

        #------------------------------------------------#

        def queryGen(selector):

            queryList = []
            for key, val in selector.items():
                if key == 'name':
                    newSel = viaName(val)
                elif key == 'range': 
                    newSel = viaRange(val)
                else:
                    newSel = viaTag(val)
                queryList.append(newSel)
            query = {}
            query['$and'] = queryList

            return query

        query = queryGen(selector)
        data = []
        for dbName in self.collections:
            cur = self.database[dbName].find(query,{'_id':1, 'name.long':1})
            for doc in cur:
                doc['collection'] = dbName
                data.append(doc)

        return data

        

    def insert_item(self, col_name, item):

        # input item is either ingredient or meal, we treat them all the same. 
        if col_name == "USDA":
            node = UsdaNode(col_name)
        elif col_name == "Foodmate":
            node = FoodmateNode(col_name)
        elif col_name == "DIY":
            node = DiyNode(col_name)

        node.set_component(item)
        node.set_mongod(self)
        return node.accept(InsertItemVisitor)



    def update_item(self, item_id, item):

        # given an object defined as in composite.py, update the document
        # according to the specs of the particular collection.

        pass