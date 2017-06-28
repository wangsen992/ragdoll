"""
A simple draft for experimenting with a database construction.
"""

import pymongo
import bson
import pandas as pd

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

    def __init__(self, ingredient_collection, dict_file="NUTR_DEF_CUS.txt"):

        self.collection = ingredient_collection

        # Obtain a universal dictionary for nutrients
        self.__nutrient_dict(file=dict_file)

    def retrieve_item(self, item_id):

        if type(item_id) != bson.objectid.ObjectId:
            item_id = bson.objectid.ObjectId(item_id)

        item = self.collection.find_one({'_id': item_id})
        if not item:
            print("No item found")
            return None

        else:
            formatted_item = self.__ingredient_constructor(item)

        return formatted_item

    def retrieve_list(self, selector):

        pass

    def __meal_constructor(doc):

        pass

    def __ingredient_constructor(self, doc):

        name = doc['name']['long']
        value = 100
        unit = 'g'
        nutrient_list = []

        for nutrient in doc['nutrients']:
            nutrient_list.append(self.__nutrient_constructor(nutrient))

        nutrients = Nutrients(source=name, input_nutrients=nutrient_list)

        return IngredientComponent(name=name,
                                   value=value,
                                   nutrients=nutrients,
                                   unit=unit)

    def __nutrient_constructor(self, doc):

        code = doc['code']
        name = doc['name']
        value = doc['value']
        unit = doc['units']
        abbr = self.nutrient_dict[self.nutrient_dict['code'] == code]['abbr']\
               .values[0]

        return Nutrient(name=name, value=value, unit=unit, abbr=abbr)

    def __nutrient_dict(self, file):

        "Obtain a dictionary (as pandas dataframe) for unifying nutrients"

        col_names = ['code', 'unit', 'abbr', 'name', 'prec', 'sort']
        with open(file, 'rb') as fout:
            lines = fout.readlines()
            data = [line.decode(encoding="cp1252")[1:-3]
                    .split("~^~") for line in lines]
        self.nutrient_dict = pd.DataFrame(data, columns=col_names)


class Selector(object):

    def __init__(self, desc=None):

        self.desc = desc
        self.criteria = {}

    def add_filter(self, attr, value):

        self.criteria[attr] = value

    def remove_filter(self, attr):

        del self.criteria[attr]

    def __repr__(self):

        return self.desc + "\n" + str(self.criteria)


if __name__ == '__main__':

    # Set up connection
    client = pymongo.MongoClient()
    collection = client['mydatabase'].mycollection
    
    usda_adapter = UsdaAdapter(collection)
    cheese = usda_adapter.retrieve_item("594504ec329fb04d99aad8df")
    cereal = usda_adapter.retrieve_item("594504f3329fb04d99aae769")

    # Set up a basket
    mybasket = cheese + cereal
    print("The type of mybasket is {}".format(type(mybasket)))

    # Make it a meal
    mymeal = mybasket.convert2meal(name="mymeal")
    print("The type of {name} is {otype}".format(name=mymeal.name, otype=type(mymeal)))

    # Now convert the meal into an ingredient
    newIngre = mymeal.convert2ingre(name="chereal")
    print("The type of {name} is {otype}".format(name=newIngre.name, otype=type(newIngre)))

    # Now put this newIngre into the original basket
    mybasket = mybasket + newIngre
    print("The children of mybasket are: {}".format([child.name for child in mybasket.children]))

