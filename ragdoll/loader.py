"""
A simple draft for loading nutritional informations from different sources.
"""
from .composite import *

from pandas import Series

def nutrient_constructor(nut_doc):

    
    name = nut_doc['name']
    value = nut_doc['value']
    unit = nut_doc['unit']
    abbr = nut_doc['abbr']

    return Nutrient(name=name, 
                    value=value, 
                    unit=unit, 
                    abbr=abbr)


def ingredient_constructor(ing_doc, col_name='', item_id=''):

    name = ing_doc['name']['long']
    value = 100
    unit = 'g'
    nutrient_list = []

    for nutrient in ing_doc['nutrients']:
        nutrient_list.append(nutrient_constructor(nutrient))

    nutrients = Nutrients(input_nutrients=nutrient_list)

    ingredient =  IngredientComponent(name=name,
                                      value=value,
                                      nutrients=nutrients,
                                      unit=unit,
                                      meta={"collection" : col_name,
                                            "item_id" : item_id})

  
    return ingredient

class Loader(object):

    # @staticmethod
    # def nutrients_loader(doc):

    #     data = []
    #     index = []
    #     units = []

    #     for nut in doc:
    #         index.append(nut['name'])
    #         data.append(nut['value'])
    #         units.append(nut['unit'])

    #     nutrients = Nutrients(data=data, units=units, index=index)

    #     return nutrients

    @staticmethod
    def ingre_loader(doc, col_name='', item_id=''):

        return ingredient_constructor(doc, col_name, item_id)