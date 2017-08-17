"""
A simple draft for loading nutritional informations from different sources.
"""
from .nutrient import *

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


class Loader(object):

    # @staticmethod
    # def nutrients_loader(doc):

    #     data = []
    #     index = []
    #     units = []

    #     for nut in doc:
    #         index.append(nut['name'])
    #         data.append(nut['value'])
    #         units.append(nut['unit']

    #     nutrients = Nutrients(data=data, units=units, index=index)

    #     return nutrients

    def nutrients_loader(doc):

        nut_list = [nutrient_constructor(nut_doc) for nut_doc in doc]

        return Nutrients(input_nutrients=nut_list)
