"""
This is a script to faciliate the construction of Human objects.
"""

from db import Mongo
from composite import Nutrient, Nutrients


def Human(object):

	def __init__(self, name, gender, age, height, weight, **kwargs):
		"""Initiate a Human object

		Parameters
		----------
		name : str
			name of the Human object.
		gender : str
			gender, either "male" or "female".
		age : int
			age of the Human object, in years.
		height : float
			height of the Human object, in cm.
		weight : float
			weight of the Human object, in kg.

		"""

		self.name = name
		self.gender = gender
		self.age = age
		self.height = height
		self.weight = weight


