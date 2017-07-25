# -*- coding: utf-8 -*-
""" Basic nutrient objects for ragdoll operations.

Nutrient and Nutrients objects are defined within this scirpt. The idea is 
that Nutrients object inherits directly from pandas.Series to make full use
of its functionality in data analysis. Additional attributes can be defined
by expanding the parent object. 

By separating the nutrients and the ingredients, it is possible for future
extension with more databases. 
"""

import numpy as np
from pandas import Series, DataFrame

from collections import defaultdict, OrderedDict

# format string used for representation of things
title_format_str = "{abbr:<10s} {value:<10} {unit:<10s} {name:<15s}\n"
entry_format_str = "{abbr:<10s} {value:<10.2f} {unit:<10s} {name:<15s}\n"
recipe_title_format_str = "{index:<5} {value:<10} {unit:<5s} {db:10s} {name: <20s}\n"
recipe_entry_format_str = "{index:<5} {value:<10.1f} {unit:<5s} {db:10s} {name: <20s}\n"


class Nutrient(object):
	"""A basic concrete class for handling nutrient-level operations.

	This serves as a **basic** class, which facilitates potential future
	customization of nutrient classes for different databases. 

	Future customization of nutrient functions can be facilitated by 
	using a function to create functions. Methods provided to provide 
	functions with different behaviors based on nutrient attributes. 

	* Currently Nutrient objects do not handle conversion of units. Future
	  support required.
	"""

	def __init__(self, abbr, value, unit, source='Unknown', name_source='Unknown'):
		"""Initiation of Nutrient object.

		Note
		----
		Parameters including name, unit and abbr should be coordinated by
		the dict_file based on the NUTR_DEF_CUS.txt to ensure compatibility
		with ingredient nutrient information from individual databases.
		
		Parameters
		----------

		value : float
			The value (amount) of the initiated nutrient in the given unit.
		unit : str
			The unit of the initiated nutrient by which the value is given.
		abbr : str
			The abbreviation of the initiated nutrient.
		source : str
			The source of the nutritional information, name of the database
			collection the **information** is obtained from.
		name_source : str
			The source of the name of the nutrient, name of the database 
			collection the **name** is used in. 

		"""
		self.abbr = abbr
		self.value = value
		self.unit = unit
		self.name_source=name_source
		self.source = set()
		if type(source) == str:
			self.source.add(source)
		elif type(source) == set:
			self.source.update(source)


	def __add__(self, other):
		"""Addition with another Nutrient object.

		Parameters
		----------
		other : Nutrient
			The other Nutrient object to be added. Enforcement on the type of
			nutrient required. Currently it is based on equality of name, unit
			and abbr.

		Returns
		-------
		Nutrient
			A Nutrient object of same type (name, unit, abbr), with value being
			the sum of both. 

		"""


		assert self.__type_test(other), "Type mismatch between two nutrient objects."

		source = self.source.copy()
		source.update(other.source)

		return Nutrient(name=self.name,
						value=self.value + other.value,
						unit=self.unit,
						abbr=self.abbr,
						source=source,
						name_source=self.name_source)

	def __sub__(self, other):
		"""Subtraction of another Nutrient object.

		Note
		----
		This method currently enforces that : self.value >= other.value.

		Parameters
		----------
		other : Nutrient
			The other Nutrient object to be added. Enforcement on the type of
			nutrient required. Currently it is based on equality of name, unit
			and abbr.

		Returns
		-------
		Nutrient
			A Nutrient object of same type (name, unit, abbr), with value being
			the difference between the first and the second. 
		
		"""

		assert self.__type_test(other), "Type mismatch between two nutrient objects."

		assert (self.value >= other.value), "First nutrient value smaller than the second."

		source = self.source.copy()
		source.update(other.source)


		return Nutrient(name=self.name,
						value=self.value - other.value,
						unit=self.unit,
						abbr=self.abbr,
						source=source,
						name_source=self.name_source)

	def __mul__(self, scalar):
		"""Multiplication with a scalar.

		Note
		----
		This method currently enforces that : scalar >= 0

		Parameters
		----------
		scalar : float or int
			The scalar value to the multiplied with. 

		Returns
		-------
		Nutrient
			A Nutrient object of same type (name, unit, abbr), with value being
			self.value multiplied with the scalar. 

		"""

		if type(scalar) not in [int, float]:
			raise ValueError("Must be multiplied with a scalar.")

		assert (scalar >= 0), "Scalar must be equal or larger than zero!"

		return Nutrient(name=self.name,
						value=self.value * scalar,
						unit=self.unit,
						abbr=self.abbr,
						source=self.source,
						name_source=self.name_source)

	def __rmul__(self, scalar):
		"""Reverse multiplication. 

		This is a supporting function for multiplication. Ensure commutative
		rules. It directly calls self.__mul__ method.

		Parameters
		----------
		scalar : float or int
			The scalar value to the multiplied with. 


		Returns
		-------
		Nutrient
			A Nutrient object of same type (name, unit, abbr), with value being
			self.value multiplied by the scalar. 

		"""

		return self.__mul__(scalar)

	def __truediv__(self, other):
		"""True division by a scalar or Nutrient object of same type.

		A division happens in two ways. 
			1. Divided by a scalar;
			2. Divided by a Nutrient object of the same type. 

		This method handles both situation indiscriminately for both input
		classes. 

		Note
		----
		This method currently enforces that : scalar > 0

		Parameters
		----------
		other : float/int or Nutrient
			* If type(other) in [float, int], perform division on self.value
			  with other.
			* If type(other) == Nutrient, after type check, division is 
			  performed by divided self.value with other.value

		Returns
		-------
		Nutrient:
			A Nutrient object of same type (name, unit, abbr), with value being
			self.value divided by the scalar or other.value. 

		"""

		if type(other) in [int, float]:
			assert (other > 0), "Scalar must be larger than zero!"

			return Nutrient(name=self.name,
							value=self.value / other,
							unit=self.unit,
							abbr=self.abbr,
							source=self.source,
							name_source=self.name_source)

		elif self.__type_test(other):

			return Nutrient(name=self.name,
							value=self.value / other.value,
							unit=" ",
							abbr=self.abbr,
							source=self.source,
							name_source=self.name_source)

		else:
			raise TypeError("Must be divided with a scalar or Nutrient object of the same type.")

		

	def __floordiv__(self, other):
		"""Floor division by a scalar or Nutrient object of same type.
		
		Note
		----
		This method enforces that : scalar > 0

		Parameters
		----------
		other : float/int or Nutrient
			* If type(other) in [float, int], perform division on self.value
			  with other.
			* If type(other) == Nutrient, after type check, division is 
			  performed by divided self.value with other.value

		if scalar provided, returns a Nutrient object;
		if Nutrient object of same type provided, returns a scalar.

		Returns
		-------
		Nutrient:
			A Nutrient object of same type (name, unit, abbr), with value being
			self.value divided by the scalar or other.value.
		"""

		if type(other) in [int, float]:
			assert (other > 0), "Scalar must be larger than zero!"

			return Nutrient(name=self.name,
							value=self.value // other,
							unit=self.unit,
							abbr=self.abbr,
							source=self.source,
							name_source=self.name_source)

		elif self.__type_test(other):

			return self.value // other.value

		else:
			raise TypeError("Must be divided with a scalar or Nutrient object of the same type.")

	def __mod__(self, other):
		"""modulus by a scalar or Nutrient object of same type.

		Note
		----
		This method enforces that : scalar > 0

		Parameters
		----------
		other : float/int or Nutrient
			* If type(other) in [float, int], perform division on self.value
			  with other.
			* If type(other) == Nutrient, after type check, division is 
			  performed by divided self.value with other.value

		if scalar provided, returns a Nutrient object;
		if Nutrient object of same type provided, returns a scalar.

		Returns
		-------
		Nutrient:
			A Nutrient object of same type (name, unit, abbr), with value being
			self.value modularized by the scalar or other.value.
		"""

		if type(other) in [int, float]:
			assert (other > 0), "Scalar must be larger than zero!"

			return Nutrient(name=self.name,
							value=self.value % other,
							unit=self.unit,
							abbr=self.abbr,
							source=self.source,
							name_source=self.name_source)

		elif self.__type_test(other):

			return self.value % other.value

		else:
			raise TypeError("Must be modularized with a scalar or Nutrient object of the same type.")

	def __lt__(self, other):
		"""Check less than condition with another Nutrient.

		Parameters
		----------
		other : Nutrient
			The other Nutrient object to be compared with. Enforcement on the type of
			nutrient required. Currently it is based on equality of name, unit
			and abbr.

		Returns
		-------
		bool
			True if less than, False otherwise.

		"""

		if self.__type_test(other):

			return self.value < other.value

	def __le__(self, other):
		"""Check less than or equal to condition with another Nutrient.

		Parameters
		----------
		other : Nutrient
			The other Nutrient object to compared with. Enforcement on the type of
			nutrient required. Currently it is based on equality of name, unit
			and abbr.

		Returns
		-------
		bool
			True if less than or equal to, False otherwise.

		"""

		if self.__type_test(other):

			return self.value <= other.value

	def __eq__(self, other):
		"""Check equal to condition with another Nutrient.

		Parameters
		----------
		other : Nutrient
			The other Nutrient object to compared with. Enforcement on the type of
			nutrient required. Currently it is based on equality of name, unit
			and abbr.

		Returns
		-------
		bool
			True if equal, False otherwise.

		"""

		if self.__type_test(other):

			return self.value == other.value

	def __ne__(self, other):
		"""Check unequal to condition with another Nutrient.

		Parameters
		----------
		other : Nutrient
			The other Nutrient object to compared with. Enforcement on the type of
			nutrient required. Currently it is based on equality of name, unit
			and abbr.

		Returns
		-------
		bool
			True if unequal, False otherwise.

		"""

		if self.__type_test(other):

			return self.value != other.value

	def __ge__(self, other):
		"""Check greater than or equal to condition with another Nutrient.

		Parameters
		----------
		other : Nutrient
			The other Nutrient object to compared with. Enforcement on the type of
			nutrient required. Currently it is based on equality of name, unit
			and abbr.

		Returns
		-------
		bool
			True if greater than or equal to, False otherwise.

		"""

		if self.__type_test(other):

			return self.value >= other.value

	def __gt__(self, other):
		"""Check greater than condition with another Nutrient.

		Parameters
		----------
		other : Nutrient
			The other Nutrient object to compared with. Enforcement on the type of
			nutrient required. Currently it is based on equality of name, unit
			and abbr.

		Returns
		-------
		bool
			True if greater, False otherwise.

		"""

		if self.__type_test(other):

			return self.value > other.value

	# Functions for emulating container types.

	def __repr__(self):
		"""The representation of objects of Nutrient class."""

		title_str = title_format_str.format(abbr='ABBR',
										    name='NAME',
										    value='VALUE',
										    unit='UNIT')
		entry_str = entry_format_str.format(abbr=self.abbr,
										    name=self.name,
										    value=self.value,
										    unit=self.unit)
		return title_str + entry_str

	def __type_test(self, other):
		"""Internal method to testing compatibility.

		Three attributes are tested: 
			* name
			* abbr
			* unit

		Parameters
		----------
		other: Nutrient
			The other Nutrient object to compared with. 

		Returns
		-------
		bool
			True if compatible, False otherwise.

		"""

		if type(other) != Nutrient:
			raise TypeError("Second argument must be a Nutrient object.")
			return False

		if self.name != other.name:
			raise ValueError("Nutrient names not the same.")
			return False

		elif self.abbr != other.abbr:
			print(self.name)
			print(self.abbr)
			print(other.name)
			print(other.abbr)
			raise ValueError("Abbreviations not the same.")
			return False

		elif self.unit != other.unit:
			print(self.name)
			print(self.unit)
			print(other.name)
			print(other.unit)
			raise ValueError("Unit types not the same.")
			return False

		return Tru

class Nutrients(Series): 

	def __init__(self, data, units, index):
		"""Initiate Nutrients object

		Key information are entered for constructing the Series-inherited 
		Nutrients object. Additional information are defined as attributes.

		data: list of floats
			value of nutrients
		units: list of strings
			units of nutrients
		index: list of strings
			abbreviations of nutrients, full name should refer to documentation.

		"""

		Series.__init__(self, data=data, index=index)
		self.units = Series(data=units, index=index)

