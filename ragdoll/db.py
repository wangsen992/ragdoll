"""
A simple draft for experimenting with a database construction.
"""
import os
import pymongo
import bson
import numpy as np
import pandas as pd

from .composite import *

nut_dict_file = "{root}/ragdoll/NUTR_DEF_more.csv".format(root=os.getcwd())
nut_dict_df = pd.read_csv(nut_dict_file, keep_default_na=False)


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

        # Use id to retrieve document of the item
        if col_name == "USDA":
            node = UsdaNode(col_name)
        elif col_name == "FM":
            node = FoodmateNode(col_name)
        elif col_name == "DIY":
            node = DiyNode(col_name)

        node.set_id(item_id)
        node.set_mongod(self)
        return node.accept(RetrieveItemVisitor)


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


class Visitor(object):

    def __init__(self, text):

        self.text=text

    def visitUsdaNode(usda_node):

        pass

    def visitFoodmateNode(fm_node):

        pass

    def visitDiyNode(DiyNode):

        pass


class RetrieveItemVisitor(Visitor):


    def visitUsdaNode(usda_node):

        def __ingredient_constructor(ing_doc):

            name = ing_doc['name']['long']
            value = 100
            unit = 'g'
            nutrient_list = []

            for nutrient in ing_doc['nutrients']:
                nutrient_list.append(__nutrient_constructor(nutrient))

            nutrients = Nutrients(input_nutrients=nutrient_list)

            ingredient =  IngredientComponent(name=name,
                                              value=value,
                                              nutrients=nutrients,
                                              unit=unit,
                                              meta={"collection" : usda_node.col_name,
                                                    "item_id" : str(ing_doc["_id"])})

            # insert meta information about database
            # ingredient.insert_meta("collection", usda_node.col_name)
            # ingredient.insert_meta("item_id", str(ing_doc["_id"]))
          
            return ingredient

        def __nutrient_constructor(nut_doc):

            
            name = nut_doc['name']
            value = nut_doc['value']
            unit = nut_doc['units']

            condition = (nut_dict_df["name_{}".format(usda_node.col_name)] == name) \
                        & (nut_dict_df["unit_{}".format(usda_node.col_name)] == unit)
            nut_info = nut_dict_df[condition]
            code = nut_info['code'].values[0]
            abbr = nut_info['abbr'].values[0]

            return Nutrient(name=name, 
                            value=value, 
                            unit=unit, 
                            abbr=abbr,
                            source=usda_node.col_name,
                            name_source=usda_node.col_name)

        collection = usda_node.mongod.database[usda_node.col_name]
        doc = collection.find_one({'_id': bson.objectid.ObjectId(usda_node.id)})

        # reconstruct the ingredient component

        return __ingredient_constructor(doc)


    def visitFoodmateNode(fm_node):

        def __ingredient_constructor(ing_doc):

            name = ing_doc['name']
            value = 100
            unit = 'g'
            nutrient_list = []

            for nutrient in ing_doc['nutrients'].items():
                nutrient_list.append(__nutrient_constructor(nutrient))

            nutrients = Nutrients(input_nutrients=nutrient_list)

            ingredient =  IngredientComponent(name=name,
                                              value=value,
                                              nutrients=nutrients,
                                              unit=unit,
                                              meta={"collection" : fm_node.col_name,
                                                    "item_id" : str(ing_doc["_id"])})

            # insert meta information about database
            # ingredient.insert_meta("collection", fm_node.col_name)
            # ingredient.insert_meta("item_id", str(ing_doc["_id"]))

            return ingredient

        def __nutrient_constructor(nut_doc):

            name, unit = nut_doc[0].split('(')
            unit = unit[:-1]
            value = nut_doc[1]
            if np.isnan(value):
                value = 0

            condition = (nut_dict_df["name_{}".format(fm_node.col_name)] == name) \
                        & (nut_dict_df["unit_{}".format(fm_node.col_name)] == unit)
            nut_info = nut_dict_df[condition]
            code = nut_info['code'].values[0]
            abbr = nut_info['abbr'].values[0]


            return Nutrient(name=name, 
                            value=value, 
                            unit=unit, 
                            abbr=abbr,
                            source=fm_node.col_name,
                            name_source=fm_node.col_name)

        collection = fm_node.mongod.database[fm_node.col_name]
        doc = collection.find_one({'_id': bson.objectid.ObjectId(fm_node.id)})

        return __ingredient_constructor(doc)

    def visitDiyNode(DiyNode):
        "No recipe for now."

        def __meal_constructor(meal_doc):


            name = meal_doc['name']
            children = list()
            print("current doc name : {name}".format(name=name))
            print([ingre_doc['name'] for ingre_doc in meal_doc['materials']])

            for ingre in meal_doc['materials']:
                print(ingre['name'])
                print(ingre['meta'])
                child = DiyNode.mongod.retrieve_item(ingre['meta']['collection'], 
                                                     ingre['meta']['item_id'])
                print("child {name} is constructed.".format(name=child.name))
                newchild = child / child.value * ingre['cook_amt']
                children.append(newchild)
            print("All children are constructed.")
            
            meal = MealComponent(name=name,
                                 children=children)
            print("Meal {name} is constructed.".format(name=meal.name))

            # insert meta information about database
            meal.insert_meta("collection", DiyNode.col_name)
            meal.insert_meta("item_id", str(meal_doc["_id"]))


            return meal


        collection = DiyNode.mongod.database[DiyNode.col_name]
        doc = collection.find_one({"_id" : bson.objectid.ObjectId(DiyNode.id)})

        return __meal_constructor(doc)



class InsertItemVisitor(Visitor):

    # def visitUsdaNode(usda_node):

    #     pass

    def visitFoodmateNode(fm_node):

        # Decompose ingredient into reasonable format according to foodmate
        ingredient = fm_node.component

        # Check for group and source
        if "type" not in ingredient.meta:
            ingredient.meta['type'] = 'DIY'

        if "source" not in ingredient.meta:
            ingredient.meta['source'] = "Analytical from ragdoll"

        # Organize nutrients into dict
        nut_dict = {"{name}({unit})".format(name=nut.name, unit=nut.unit) : nut.value\
                    for nut in ingredient.nutrients.nutrients.values()}

        # Organize out_dict
        out_dict = {"name" : ingredient.name,
                    "type" : ingredient.meta['type'],
                    "source" : ingredient.meta['source'],
                    "nutrients" : nut_dict}

        # Insert to foodmate
        result = fm_node.mongod.database[fm_node.col_name].insert_one(out_dict)
        print(result)


    def visitDiyNode(DiyNode):

        # Decompose a meal into reasonable format according to DIY format
        meal = DiyNode.component

        result = DiyNode.mongod.database[DiyNode.col_name].insert_one(meal.to_dict())
        print(result)








class Node(object):

    def __init__(self, col_name):

        self.col_name = col_name

    def set_id(self, id):

        self.id = id

    def set_mongod(self, mongod):

        self.mongod = mongod

    def set_component(self, component):

        self.component = component

    def accept(self, visitor):

        pass

class UsdaNode(Node):

    def __init__(self, col_name):

        Node.__init__(self, col_name)

    def accept(self, visitor):

        return visitor.visitUsdaNode(self)

class FoodmateNode(Node):

    def __init__(self, col_name): 

        Node.__init__(self, col_name)

    def accept(self, visitor):

        return visitor.visitFoodmateNode(self)

class DiyNode(Node):

    def __init__(self, col_name):

        Node.__init__(self, col_name)

    def accept(self, visitor):

        return visitor.visitDiyNode(self)
