"""
Use sharing to support large numbers of fine-grained objects
efficiently.

This script is adopted from https://sourcemaking.com/design_patterns/flyweight/python/1
"""

import abc
from bson import ObjectId

from .db import MongoDB
from .loader import *


# class IngreFlyweightFactory:
#     """
#     Create and manage flyweight objects.
#     Ensure that flyweights are shared properly. When a client requests a
#     flyweight, the FlyweightFactory object supplies an existing instance
#     or creates one, if none exists.
#     """

#     def __init__(self, mongo):
#         self._ingre_flyweights = {}
#         self.mongo = mongo

#     def get_flyweight(self, key, doc=None):
#         """
#         key is a tuple of (collection, id)
#         """
#         try:
#             ingre_flyweight = self._ingre_flyweights[key]
#         except KeyError:
#             if doc==None:
#                 doc = self.mongo.retrieve_item(key[0], key[1])
#             doc['col'] = key[0]
#             ingre_flyweight = ConcreteIngreFlyweight(doc)
#             self._ingre_flyweights[key] = ingre_flyweight
#         return ingre_flyweight


# class IngreFlyweight(metaclass=abc.ABCMeta):
#     """
#     Declare an interface through which flyweights can receive and act on
#     extrinsic state.

#     nut_doc : dict
#         Imported data of ingredient information of specified format. 
#     """

#     def __init__(self, doc):
        
#         self._construct_ingre(doc)

#     def _construct_ingre(self, doc):

#         # decompose ingredient doc
#         self.key = (doc['col'], doc['_id'].__str__)
#         self.name = doc['name']['long']

#         data = []
#         index = []
#         units = []

#         for nut in doc['nutrients']:
#             index.append(nut['name'])
#             data.append(nut['value'])
#             units.append(nut['unit'])

#         self.nutrients = Nutrients(data=data, units=units, index=index)


#     @abc.abstractmethod
#     def operation(self, extrinsic_state):
#         pass

#     @abc.abstractmethod
#     def apply_amt(self, amt):

#         pass


# class ConcreteIngreFlyweight(IngreFlyweight):
#     """
#     Implement the Flyweight interface and add storage for intrinsic
#     state, if any. A ConcreteFlyweight object must be sharable. Any
#     state it stores must be intrinsic; that is, it must be independent
#     of the ConcreteFlyweight object's context.
#     """

#     def operation(self, extrinsic_state):
#         pass

#     def apply_amt(self, amt):

#         return self.nutrients * amt / 100

