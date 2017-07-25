"""
A simple draft for loading nutritional informations from different sources.
"""

from .nutrient import *

class Loader(object):

    @staticmethod
    def nutrients_loader(doc):

        data = []
        index = []
        units = []

        for nut in doc:
            index.append(nut['name'])
            data.append(nut['value'])
            units.append(nut['unit'])

        nutrients = Nutrients(data=data, units=units, index=index)

        return nutrients

    @staticmethod
    def ingre_loader(doc):

        name = doc['name']['long']

        data = []
        index = []
        units = []

        for nut in doc['nutrients']:
            index.append(nut['name'])
            data.append(nut['value'])
            units.append(nut['unit'])

        nutrients = Nutrients(data=data, units=units, index=index)
        
        return (name, nutrients)