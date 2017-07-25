# -*- coding: utf-8 -*-
""" Composite structures for ragdoll compositions.

A composite structure is defined here to facilitate composition operations. 
The flexible use of Series and DataFrame and their integration with tree-like
structure is the key feature. 

By separating the nutrients and the ingredients, it is possible for future
extension with more databases. 
"""

import numpy as np
from pandas import Series, DataFrame
from anytree import NodeMixin

from .nutrient import Nutrients
# from .flyweight import IngreFlyweightFactory

class FoodNode(DataFrame, NodeMixin):
	"""FoodNode

	"""

	def __init__(self, 
				 name=None,
				 parent=None,
				 nutrients=None,
				 value=100,
				 ):

		DataFrame.__init__(self, nutrients)
		self.name = name
		self.parent = parent
		self.value = value
		self.units = nutrients.units


	def operation():

		pass