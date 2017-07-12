# -*- coding: utf-8 -*-
""" Composite structures for ragdoll operations.

This module defines the basic classes for the package, including Component, 
IngredientComponent, BasketComponent, MealComponent, Nutrient and Nutrients.
While Nutrients is simply an aggregation of Nutrients, the four *component 
classes are formed with a composite structure. 

The idea is to apply a composite structure, such that ingredient and meal
can be treated as the same structure by clients. Addition and subtraction 
should be abstracted with plus and minus signs for simple manipulation. 

By separating the nutrients and the ingredients, it is possible for future
extension with more databases. 
"""
from collections import defaultdict, OrderedDict

import pandas as pd

from .amount import Amount

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

	def __init__(self, name, value, unit, abbr, source='Unknown', name_source='Unknown'):
		"""Initiation of Nutrient object.

		Note
		----
		Parameters including name, unit and abbr should be coordinated by
		the dict_file based on the NUTR_DEF_CUS.txt to ensure compatibility
		with ingredient nutrient information from individual databases.
		
		Parameters
		----------
		name : str
			The name of the initiated nutrient.
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

		self.name = name
		self.amt = Amount(value, unit)
		self.abbr = abbr
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

		new_amt = self.amt + other.amt

		return Nutrient(name=self.name,
						value=new_amt.value,
						unit=new_amt.unit,
						abbr=self.abbr,
						source=source,
						name_source=self.name_source)

	def __sub__(self, other):
		"""Subtraction of another Nutrient object.

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

		source = self.source.copy()
		source.update(other.source)

		new_amt = self.amt - other.amt

		return Nutrient(name=self.name,
						value=new_amt.value,
						unit=new_amt.unit,
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

		if type(scalar) in [int, float]:

			new_amt = self.amt * scalar

			return Nutrient(name=self.name,
							value=new_amt.value,
							unit=new_amt.unit,
							abbr=self.abbr,
							source=self.source,
							name_source=self.name_source)

		else:
			raise TypeError("Nutrient object must be multiplied with a scalar.")

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

			new_amt = self.amt / other


		elif self.__type_test(other):

			new_amt = self.amt / other.amt

		else:
			raise TypeError("Must be divided with a scalar or Nutrient object of the same type.")

		return Nutrient(name=self.name,
						value=new_amt.value,
						unit=new_amt.unit,
						abbr=self.abbr,
						source=self.source,
						name_source=self.name_source)


	def __repr__(self):
		"""The representation of objects of Nutrient class."""

		title_str = title_format_str.format(abbr='ABBR',
										    name='NAME',
										    value='VALUE',
										    unit='UNIT')
		entry_str = entry_format_str.format(abbr=self.abbr,
										    name=self.name,
										    value=self.amt.value,
										    unit=self.amt.unit)
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

		elif self.abbr != other.abbr:
			raise ValueError("Abbreviations not the same.")

		return True


class Nutrients(object):
	"""An organizer of a group of nutrients.

	This is an organizer of nutrients, it handles the operation among
	clusters of nutrients.

	Abbreviation, as the key of nutrients, are used for quick matching of 
	nutrients of the same type. The dictionary of abbreviation and nutrient
	names are defined in a separated file, e.g. NUTR_DEF_CUS.txt.
	
	An important concept of operation is whether use **union** or **intersection** 
	for algebraic operations between clusters of nutrients. 
		* Union:

			All nutrients' information are preserved. However, nutrients
			with incomplete information source (not-available in certain
			ingredient) can only indicate a minimum level of nutrient, but 
			no indication of the upper limit. Therefore those values must
			be used with **caution**.

		* Intersect:

			Only nutrients present in all ingredients are retained and computed.
			This ensures precise (at database level) nutritional information
			of the resultant object.

	For all operations below, **Intersect** is chosen as default. However, 
	explicit call on operation methods without operation overloading can be 
	made by stating *method='union'* as argument.
	
	Note
	----
	For union operation, missing info handling (for mismatch of nutrients) is 
	completely ignored in this version. 

	Divisions between Nutrients is unknown. Not defined right now.

	"""

	def __init__(self, input_nutrients=list()):
		"""Initiation of Nutrient object

		Initialization requires type and format check on the nutrient objects
		supplied. Therefore, the addition of nutrients can be handled by 
		__add_nutrients method, which conducts the type and format check.

		While input_nutrients are entered as list, they are transformed into
		OrderedDict afer initiation. 

		Parameters
		----------
		input_nutrients : list
			A list of children (IngredientComponent or MealComponent) to be
			included at the initialization of the Nutrients object.

		"""

		self.nutrients = OrderedDict()
		self.add_nutrients(input_nutrients)
		self.update_attrs()


	def update_attrs(self):

		# Set attrs
		self.nutrs = [nut for nut in self.nutrients.values()]
		self.abbrs = [nut.abbr for nut in self.nutrients.values()]
		self.names = [nut.name for nut in self.nutrients.values()]
		self.sources = [nut.source for nut in self.nutrients.values()]
		self.name_sources = [nut.name_source for nut in self.nutrients.values()]
		self.units = [nut.amt.unit for nut in self.nutrients.values()]
		self.values = [nut.amt.value for nut in self.nutrients.values()]
		self.amts = [nut.amt for nut in self.nutrients.values()]
		self.size = self.__len__()

	def add_nutrients(self, nutrients):
		"""Insert nutrients into the Nutrients object.
		
		Parameters
		----------
		*nutrients : Nutrient or list of Nutrient objects
			Nutrient object or a list of Nutrient objects to be added.
		
		"""
		if type(nutrients) != list:

			nutrients = [nutrients, ]

		for nutrient in nutrients:

			assert (type(nutrient) == Nutrient), "{} not a Nutrient object.".format(nutrient)

			if nutrient.abbr in self.nutrients:
				# Cumulate nutrient values if there is existing Nutrient object
				# of the same type.
				assert self.nutrients[nutrient.abbr]._Nutrient__type_test(nutrient), "Nutrient not compatible with existing nutrient"
				self.nutrients[nutrient.abbr] = self.nutrients[nutrient.abbr] + nutrient
			else:
				# Add Nutrient to collection if no existing Nutrient object
				# of the same type. 
				self.nutrients[nutrient.abbr] = nutrient

	def add(self, other, method="intersect"):
		"""Addition with another Nutrients object

		Performs summation between two Nutrients objects. When two Nutrients
		objects are added together, the choice between **union** and 
		**intersect** must be made. addition is performed at nutrient-level
		for all nutrients. 

		Parameters
		----------
		other : Nutrients
			The other Nutrients object to be added.
		method : str
			Method for managing mismatching Nutrient objects within both
			Nutrients objects. Default "intersect"

		Returns
		-------
		Nutrients
			Nutrients object with summation results.

		"""

		# check other type
		if type(other) != Nutrients:
			if other == 0:
				return self
			else:
				raise TypeError("Second argument not Nutrients object")

		# Initiate a new dictionary for addition.
		newNutrients_dict = OrderedDict()

		# Obtain the keys from both Nutrients objects. 
		self_keys = self.nutrients.keys()
		other_keys = other.nutrients.keys()

		# Perform addition.
		if method == "union":

			for abbr in self_keys | other_keys:

				if abbr in self_keys & other_keys:

					newNutrients_dict[abbr] = self.nutrients[abbr] + other.nutrients[abbr]

				else:
					newNutrients_dict[abbr] = self.nutrients[abbr] if abbr \
											  in self_keys else other.nutrients[abbr]

		elif method == "intersect":

			for abbr in self_keys & other_keys:

				newNutrients_dict[abbr] = self.nutrients[abbr] + other.nutrients[abbr]

		return Nutrients(input_nutrients=list(newNutrients_dict.values()))

	def __add__(self, other):
		"""Wrapper function of self.add for operation overloading on "+". """

		return self.add(other, method="intersect")

	def __radd__(self, other):
		"""Wrapper function of self.add for operation overloading on "+". """

		return self.add(other, method="intersect")

	def sub(self, other, method="intersect"):
		"""Subtraction of another Nutrients object

		Performs subtraction between two Nutrients objects. When two Nutrients
		objects are performing subtraction, the choice between **union** and 
		**intersect** must be made. addition is performed at nutrient-level
		for all nutrients. 

		Parameters
		----------
		other : Nutrients
			The other Nutrients object to subtract with.
		method : str
			Method for managing mismatching Nutrient objects within both
			Nutrients objects. Default "intersect"

		Returns
		-------
		Nutrients
			Nutrients object with subtraction results.

		"""
		# check other type
		if type(other) != Nutrients:
			raise TypeError("Second argument not Nutrients object")

		newNutrients_dict = OrderedDict()

		self_keys = self.nutrients.keys()
		other_keys = other.nutrients.keys()

		if method == "union":

			for abbr in self_keys | other_keys:

				if abbr in self_keys & other_keys:

					newNutrients_dict[abbr] = self.nutrients[abbr] - other.nutrients[abbr]

				else:

					newNutrients_dict[abbr] = self.nutrients[abbr] if abbr in \
											  self_keys else (-1) * other.nutrients[abbr]

		if method == "intersect":

			for abbr in self_keys & other_keys:

				newNutrients_dict[abbr] = self.nutrients[abbr] - other.nutrients[abbr]

		return Nutrients(input_nutrients=list(newNutrients_dict.values()))

	def __sub__(self, other):
		"""Wrapper function of self.sub for operation overloading on "-". """

		return self.sub(other, method="intersect")

	def multiply(self, scalar):
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
		Nutrients
			A Nutrients object of with the same Nutrient objects, with value
			of each being Nutrient.value multiplied with the scalar. 

		"""

		if type(scalar) not in [int, float]:
			raise ValueError("Must be multiplied with a scalar.")

		newNutrients_dict = OrderedDict()

		for abbr in self.nutrients.keys():

			newNutrients_dict[abbr] = self.nutrients[abbr] * scalar

		return Nutrients(input_nutrients=list(newNutrients_dict.values()))

	def __mul__(self, scalar):

		return self.multiply(scalar)

	def __rmul__(self, scalar):
		"""Wrapper function of self.__mul__ for operation overloading on "*"."""

		return self.multiply(scalar)

	def divide(self, other, method='intersect'):
		"""Division of a scalar.

		Note
		----
		This method currently enforces that : scalar > 0

		Parameters
		----------
		other : (float or int), or Nutrients
			The scalar value to the multiplied with. 

		Returns
		-------
		Nutrients
			A Nutrients object of with the same Nutrient objects, with value
			of each being Nutrient.value divided by the scalar. 

		"""

		newNutrients_dict = OrderedDict()

		if type(other) in [int, float]:

			for abbr in self.nutrients.keys():

				newNutrients_dict[abbr] = self.nutrients[abbr] / other
		
		elif type(other) == Nutrients:

			if method == 'intersect':
				for abbr in self.nutrients.keys() & other.nutrients.keys():
					newNutrients_dict[abbr] = self.nutrients[abbr] / other.nutrients[abbr]
			elif method == 'union':
				raise ValueError("union can't be performed.")

		else:
			raise TypeError("Nutrients must be divided by a scalar or another Nutrients object.")

		return Nutrients(input_nutrients=list(newNutrients_dict.values()))

	def __truediv__(self, other):

		return self.divide(other)

	# Emulating container type behaviors
	def __len__(self):

		return len(self.nutrients)

	def __getitem__(self, key):

		if type(key) == str:

			key = [key, ]

		if type(key) == list:

			return Nutrients(input_nutrients=[self.nutrients[k] for k in key])

		else:

			raise TypeError("Key must be either a string or a list.")

	def __delitem__(self, key):

		if type(key) == str:

			key = [key, ]

		if type(key) == list: 
			for k in key:
				del self.nutrients[k]
			self.update_attrs()

		else:
			raise TypeError("Indexing must come with either str or list type.")

	def __iter__(self):

		for i in self.nutrients.values():
			yield i

	# Sort capability
	def sort(self, key='amt', reverse=False):
		"""Sort with a specified key"""

		nutrients = sorted(self.nutrients.values(),
						   key=lambda nut : getattr(nut, key),
						   reverse=reverse)

		return Nutrients(input_nutrients=nutrients)

	# Aggregate functions
	# This remains a problem as the sum may not have a physical meaning. 

	# grouping
	def group(self):
		"""Group with Nutrient types
		
		Note
		----
		So there is a need to update Nutrient relation at Nutrient __init__.

		"""

		pass

	def simplify(self):
		"""Simplify Nutrients with nutrients relationships.
		
		A unified simplification of Nutrients can serve two purposes:
		1. Create a much clearer representation of nutrients available inside.
		2. Enable a more fluid computation across Nutrients objects, and also
		   allows a better sorting operation by avoiding different nutrient 
		   types colliding on each other. 

		"""

		pass

	def unify_units(self, target_unit='g'):

		nutrients = []
		for nut in self.nutrs:
			new_amt = nut.amt.convert(target_unit)
			nutrients.append(Nutrient(name=nut.name,
									  value=new_amt.value,
									  unit=new_amt.unit,
									  abbr=nut.abbr,
									  source=nut.source,
									  name_source=nut.name_source))

		return Nutrients(input_nutrients=nutrients)

	def __repr__(self):
		"""Representation of Nutrients object."""
		title_str = title_format_str.format(abbr='ABBR',
										    name='NAME',
										    value='VALUE',
										    unit='UNIT')

		entry_str = "".join([entry_format_str.format(abbr=nut.abbr,
												     name=nut.name,
												     value=nut.amt.value,
												     unit=nut.amt.unit) 
							 for nut in self])

		return title_str + entry_str


# Composite class for ingredients and meals

class Component(object):
	"""Abstract class for the composite structure

	Component class serves as the base class for the composite structure
	consisting of the IngredientComponent class[leaf], the BasketComponent 
	class [composite] and the MealComponent class [composite].

	The purpose of the composite structure is two-fold:
		1. enables a recursive structure of the meal, assisting flexible 
		   composition of meals.
		2. consolidate a unified interface for all component classes towards
		   external clients, thus clients do not need to know which component
		   they are operating on. 
	
	Relationships between IngredientComponent, BasketComponent, and 
	MealComponent: 
		* IngredientComponent has no children, it acts as the leaf within 
		  the recursive structure. 
		* BasketComponet is a composite, it has children. The uniqueness about
		  the BasketComponent from a MealComponent is that when new components 
		  are added to a BasketComponent, those added components are always in
		  the first level. 
		* MealComponent is similar to a BasketComponent, but it can only be
		  obtained by calling the .convert2meal() method on the BasketComponent.
	
	This relationship can be better illustrated with the equations below:
		*. Ingredient1 + Ingredient2 = Basket1
			*. Basket1.children consists of (Ingredient1, Ingredient2)
		*. Ingredient3 + Ingredient4 + Ingredient5 = Basket2
			*. Basket2.children consists of (Ingredient3, Ingredient4, Ingredient5)
		*. Ingredient6 + Basket1 = Basket4
			*. Basket4.children consists of (Ingredient 6, Ingredient3 to Ingredient5)
		*. Basket1 + Basket2 = Basket3
			*. Basket3.children consists of (Ingredient1 to Ingredient5)
		*. Basket1.convert2meal() = Meal1
			*. Meal1.children = Basket1.children
		*. Basket2 + Meal1 = Basket3
			*. Basket3.children consists of (Ingredient3 to Ingredient5, and Meal1)

	Key operations:

	There are two key sets of operations for the basic classes:
	*. Indexing operations: As these classes act as containers, it is important
	   to provide flexible indexing methods to enable a large set of potential
	   operations. Those includes:
		1. Indexing
		2. Iterating
		3. length
		4. size
		5. grouping?

	*. Algebraic operations: Important to manipulate values by performing 
	   algebraic operations such as addition, subtraction, multiplication
	   and division between components. 

	The relationship between components and their variation in methods decides
	that BasketComponent inherits MealComponents, as MealComponents shares
	similar operations with IngredientComponents. 

	"""

	def __init__(self, name="unknown"):

		self.name = name
		self.amt = Amount(value=0, unit='g')
		self.children = OrderedDict()
		self.nutrients = Nutrients()
		self.meta = dict()

	def __identity_check(self, other):

		"""Test the identity between components"""

		if type(self) != type(other) \
		   or self.name != other.name \
		   or self.meta != other.meta:

			return False

		else:
			return True

	def add(self, other):

		"""Summation between two Components

		Three types of components can be added to an IngredientComponent:

		* IngredientComponent: 
			*. if two IngredientComponent objects are the same, in terms of 
			   meta infomation, the IngredientComponent is returned with 
			   added value. 

			*. if two IngredientComponent objects are not the same, in terms
			   of meta information, a BasketComponent with children as a OrderedDict 
			   consisting of those two Ingredient Components.

		*. BasketComponent: 
			*. If the IngredientComponent has peer in the BasketComponent (meta),
			   this IngredientComponent will be added to that peer.
			*. If the IngredientComponent has no peer in the BasketComponent,
			   this IngredientComponent will be added to the children of the 
			   BasketComponent.

		*. MealComponent:
			*. A BasketComponent is returned with children as a OrderedDict 
			   consisting of the IngredientComponent and the MealComponent.

		Parameters
		----------
		other: IngredientComponent or BasketComponent or MealComponent
			The object to be added with. 

		Returns
		-------
		IngredientComponent or BasketComponent
			Type depends on the class of **other**.


		"""

		pass

	def sub(self, other):

		pass

	def multiply(self, other):

		pass

	def divide(self, other):

		pass

	def __add__(self, other):

		pass

	def __sub__(self, other):

		pass

	def __mul__(self, scalar):

		pass

	def __rmul__(self, scalar):

		return self.__mul__(scalar)

	def __truediv__(self, scalar):

		pass



	def insert_meta(self, key, value):

		self.meta[key] = value

	def list_nutrients(self):

		return [nut.name for nut in self.nutrients.nutrients.values()]

	def display_macro(self):

		pass

	def display_minerals(self):

		mineral_nut_abbr = ['CA', 'FE', 'MG', 'P', 'K', 'NA', 'ZN', 'CU', 'FLD',
							'MN', 'SE']

		for key in mineral_nut_abbr:
			try:
				print(self.nutrients.nutrients[key])
			except:
				continue


class IngredientComponent(Component):
	"""Leaf class for the composite structure
	
	IngredientComponent class is the leaf class, thus it has no children. 
	It represents an ingredient of a meal. It cannot be decomposed further
	into other ingredients, but only into individual nutrients. 

	There are two types of operations available with IngredientComponent:
		1. Algebraic operation: with operator overloading, four operations are
		   defined for IngredientComponent: 
		   1. Summation
		   2. Subtraction
		   3. Multiplication
		   4. Division

		2. Dataframe-like Indexing: with over-riding some methods, easier 
		   indexing operations are possible to faciliate quick retrieval of 
		   information. 

	"""

	def __init__(self, name, value, nutrients, unit='g', meta=dict()):

		Component.__init__(self, name)
		self.value = value
		self.unit = unit
		self.nutrients = nutrients
		self.meta = meta

	def add(self, other):
		"""Summation between two Components

		Three types of components can be added to an IngredientComponent:

		* IngredientComponent: 
			*. if two IngredientComponent objects are the same, in terms of 
			   meta infomation, the IngredientComponent is returned with 
			   added value. 

			*. if two IngredientComponent objects are not the same, in terms
			   of meta information, a BasketComponent with children as a OrderedDict 
			   consisting of those two Ingredient Components.

		*. BasketComponent: 
			*. If the IngredientComponent has peer in the BasketComponent (meta),
			   this IngredientComponent will be added to that peer.
			*. If the IngredientComponent has no peer in the BasketComponent,
			   this IngredientComponent will be added to the children of the 
			   BasketComponent.

		*. MealComponent:
			*. A BasketComponent is returned with children as a OrderedDict 
			   consisting of the IngredientComponent and the MealComponent.

		Parameters
		----------
		other: IngredientComponent or BasketComponent or MealComponent
			The object to be added with. 

		Returns
		-------
		IngredientComponent or BasketComponent
			Type depends on the class of **other**.


		"""

		if not issubclass(type(other), Component) :
			raise TypeError("Second argument not a sub-Component object")

		if type(other) == IngredientComponent:
			if self.meta == other.meta \
			   and self.name == other.name \
			   and self.unit == other.unit:

				return IngredientComponent(name=self.name,
										   value=self.value+other.value,
										   nutrients=self.nutrients+other.nutrients,
										   unit=self.unit,
										   meta=self.meta)
			else:

				return BasketComponent(name='MyBasket',
									   children=[self, other])

		elif type(other) == BasketComponent:
			return BasketComponent(name='MyBasket',
								   children=[self, *other.children.values()])

		elif type(other) == MealComponent:
			return BasketComponent(name='MyBasket',
								   children=[self, other])

	def sub(self, other):
		"""Subtraction of another IngredientComponent of same kind
		
		Only IngredientComponent object of the same kind (meta) can be 
		subtracted from self. Currently, there should be enforcement on
		self.value >= other.value.

		Parameters
		----------
		other: IngredientComponent
			The IngredientComponent of the same kind (meta) to be subtracted
			with.

		Returns
		-------
		IngredientComponent
			An IngredientComponent of the same kind with its values being
			self.value - other.value.

		"""

		if type(other) != IngredientComponent:
			raise TypeError("Second argument must be an IngredientComponent object.")

		if self.meta != other.meta:
			raise ValueError("Two IngredientComponent objects' meta do not match.")

		if self.value < other.value:
			raise ValueError("Value of first IngredientComponent must be larger"
							 " or equal to that of the second one.")

		return IngredientComponent(name=self.name,
								   value=self.value-other.value,
								   nutrients=self.nutrients+other.nutrients,
								   unit=self.unit,
								   meta=self.meta)

	def __add__(self, other):
		"""Overloading of the + operator."""

		return self.add(other)

	def __sub__(self, other):
		"""Overloading of the - operator."""
		
		return self.sub(other)

	def multiply(self, other):
		"""Multiplication with a scalar

		Parameters
		----------
		other: int or float
			The scalar to be multiplied with. 

		Returns
		-------
		IngredientComponent
			An IngredientComponent of the same kind with its values being
			self.value * other.

		"""

		if type(other) not in [int, float]:
			raise ValueError("Must be multiplied with a scalar.")

		assert (other >= 0), "Scalar must be equal or larger than zero!"

		return IngredientComponent(name=self.name,
								   value=self.value * other,
								   unit=self.unit,
								   nutrients=self.nutrients * other,
								   meta=self.meta)

	def __mul__(self, scalar):
		"""Overloading of the * operator."""
		
		return self.multiply(scalar)

	def __rmul__(self, scalar):
		"""Overloading of the * operation in case of reverse order"""

		return self.multiply(scalar)

	def divide(self, other):
		"""Division by another IngredientComponent of same kind or a scalar.
		
		There are two data types that can be inputted as other: 
		*. IngredientComponent
			Only IngredientComponent object of the same kind (meta) can divide 
			self. Check other.value > 0. It returns a scalar with value being
			self.value / other.value
		*. Scalar (int or float)
			An IngredientComponent of the same kind is returned with its value
			being self.value / other. Check other > 0.


		Parameters
		----------
		other: IngredientComponent or (int or float)
			The IngredientComponent of the same kind (meta) or the scalar to 
			divide self. 

		Returns
		-------
		(int or float) or IngredientComponent
			Ratio between the two IngredientComponents of the same kind, or, 
			an IngredientComponent of the same kind with its values being
			self.value - other.

		"""

		if type(other) in [int, float]:

			assert (other > 0), "Scalar must be larger than zero!"

			return IngredientComponent(name=self.name,
									   value=self.value / other,
									   unit=self.unit,
									   nutrients=self.nutrients / other,
									   meta=self.meta)
		elif type(other) == IngredientComponent:

			assert (self.meta == other.meta), ("Two IngredientComponent objects' "
											   "meta do not match.")

			assert (other.value > 0), "Second IngredientComponent value <= 0."

			return self.value / other.value


	def __truediv__(self, other):
		"""Overloading of the / operator."""

		return self.divide(other)


	# Container methods		
		
	def __len__(self):
		"""Returns the number of nutrients within the Ingredients."""

		return len(self.nutrients)

	def __getitem__(self, key):


		if type(key) not in [str, list]:

			raise TypeError("Indexing must come with either str or list type.")

		if type(key) == str:

			return self.nutrients[key]

		else:
			return IngredientComponent(name=self.name,
									   value=self.value,
									   nutrients=self.nutrients[key],
									   unit=self.unit,
									   meta=self.meta
									   )

	def __delitem__(self, key):

			del self.nutrients[key]


	def __iter__(self):

		return self.nutrients.__iter__()

	def items(self):

		for key in self.nutrients:

			yield(key, self.nutrients[key])

	def keys(self):

		return self.nutrients.keys()

	def values(self):

		return self.nutrients.values()



	def __repr__(self):

		return "Ingredient\n" +\
			   "Name : {}\n".format(self.name) +\
			   "Value : {} {}\n".format(self.value, self.unit) +\
			   "Nutrients: \n" +\
			   self.nutrients.__repr__()


def flatten(AggComponent):
	"Helper function for flattening BasketComponent and MealComponent."

	children = []

	if len(AggComponent.children) == 0:
		children.append(AggComponent)

	else:
		for child in AggComponent.children.values():
			children.extend(flatten(child))

	return children


class BasketComponent(Component):

	def __init__(self, name, children=list(), unit='g'):

		Component.__init__(self, name)
		self.unit = unit
		self.add_children(children)

	def add_children(self, children):
		"""Insert ingredients into the Basket object.

		Note
		----
		As the number of children is not certain, asterisk (*) is added for 
		the function to be able to handle both single, double entry or entry 
		as a list. 
		
		Parameters
		----------
		*children : Nutrient or list of Nutrient objects
			Nutrient object or a list of Nutrient objects to be added.
		
		"""

		if type(children) not in [IngredientComponent, MealComponent, list]:

			raise TypeError("Input type must be in IngredientComponent, MealComponent or list")

		if type(children) != list:

			children = [children, ]

		for child in children:

			if child.name in self.children:
				# Cumulate child values if there is existing object
				# of the same type.
				self.children[child.name] = self.children[child.name] + child
			else:
				# Add Nutrient to collection if no existing Nutrient object
				# of the same type. 
				self.children[child.name] = child

		self.update_attr()

	def compute_nutrition(self):
		"Intersect addition is used implicitly."

		self.nutrients = sum([child.nutrients for child in self.children.values()])

	def compute_value(self):

		self.value = sum([child.value for child in self.children.values()])

	def update_attr(self):

		self.compute_nutrition()
		self.compute_value()

	def remove_child(self, index):
		"""Remove child with index, no regret here."""

		if type(index) != int or index < 0:
			raise ValueError("Input index not correct.")

		self.children.remove(index)
		self.update_attr()

	def add(self, other):

		"Only for ingredient-ingredient summation for now"
		if not issubclass(type(other), Component) :
			raise TypeError("Second argument not a sub-Component object")

		if type(other) in [IngredientComponent, MealComponent]:
			return BasketComponent(name='MyBasket',
								   children=[*self.children.values(), other])

		elif type(other) == BasketComponent:
			return BasketComponent(name='MyBasket',
								   children=[*self.children.values(), *other.children.values()])


	def __add__(self, other):

		return self.add(other)

	def __sub__(self, other):

		pass

	def __mul__(self, scalar):
		
		if type(scalar) not in [int, float]:
			raise ValueError("Must be multiplied with a scalar.")

		assert (scalar >= 0), "Scalar must be equal or larger than zero!"

		children = [child * scalar for child in self.children.values()]

		return BasketComponent(name=self.name,
							   children=children)

	def __rmul__(self, scalar):

		return self.__mul__(scalar)

	def __truediv__(self, scalar):

		if type(scalar) not in [int, float]:
			raise ValueError("Must be multiplied with a scalar.")

		assert (scalar > 0), "Scalar must be larger than zero!"

		children = [child / scalar for child in self.children.values()]

		return BasketComponent(name=self.name,
							   children=children)

	def __len__(self):

		return len(self.children)

	def loc(self, key):
		"""
		__getitem__ should be consistently used for nutrients indexing,
		.loc(key) can be used for children selection.
		"""

		if type(key) not in [str, list]:

			raise TypeError("Input key must be str or list.")


		if type(key) == str:


			return self.children[key]

		else:


			return BasketComponent(name=self.name,
								   unit=self.unit,
								   children=[self.children[k] for k in key]
								   )

	def __getitem__(self, key):

		if type(key) not in [str, list]:

			raise TypeError("Input key must be str or list.")

		if type(key) == str:

			key = [key, ]

		return BasketComponent(name=self.name,
							   unit=self.unit,
							   children = [child[key] for child in self.children.values()])

	def __delitem__(self, key):

			del self.children[key]
			self.update_attr()


	def __iter__(self):

		return self.children.__iter__()

	def items(self):

		for key in self.children:

			yield(key, self.children[key])

	def keys(self):

		return self.children.keys()

	def values(self):

		return self.children.values()


	def convert2ingre(self, name):

		return IngredientComponent(name, 
								   value=self.value,
								   nutrients=self.nutrients, 
								   unit=self.unit)

	def convert2meal(self, name, recipe=None):

		"Simply create a meal object now, no recipes required."
		"This should be the only way to create a MealComponent object."

		return MealComponent(name=name,
							 children=list(self.children.values()),
							 unit=self.unit)

	def __repr__(self):

		name_str = "Name: {name}\n".format(name=self.name)
		value_str = "Value: {value} {unit}\n".format(value=self.value,
												   unit=self.unit)
		recipe_title_str = recipe_title_format_str.format(index="INDEX",
														  name="NAME",
														  value="VALUE",
														  unit="UNIT",
														  db="COLLECTION"
														  )

		recipe_entry_str = ''.join([recipe_title_format_str.format(index=i,
													 	   name=child.name,
													       value=child.value,
													       unit=child.unit,
													       db=child.meta['collection']
													      )
							for i, child in enumerate(self.children.values())])

		return name_str + value_str + recipe_title_str \
			   + recipe_entry_str + '\n' + self.nutrients.__repr__()


class MealComponent(BasketComponent):

	def __init__(self, 
				 name, 
				 children,
				 unit='g',
				 meta=dict()
				 ):

		BasketComponent.__init__(self, name, children, unit)
		self.meta = meta

	def add(self, other):

		"Only for ingredient-ingredient summation for now"
		if not issubclass(type(other), Component) :
			raise TypeError("Second argument not a sub-Component object")

		if type(other) == IngredientComponent:
			return BasketComponent(name='MyBasket',
								   children=[self, other])

		elif type(other) == BasketComponent:
			return BasketComponent(name='MyBasket',
								   children=[self, *other.children.values()])

		elif type(other) == MealComponent:
			return BasketComponent(name='MyBasket',
								   children=[self, other])
	def __sub__(self, other):

		pass

	def __mul__(self, scalar):
		
		if type(scalar) not in [int, float]:
			raise ValueError("Must be multiplied with a scalar.")

		assert (scalar >= 0), "Scalar must be equal or larger than zero!"

		children = [child * scalar for child in self.children.values()]

		return MealComponent(name=self.name,
							   children=children)

	def __rmul__(self, scalar):

		return self.__mul__(scalar)

	def __truediv__(self, scalar):

		if type(scalar) not in [int, float]:
			raise ValueError("Must be multiplied with a scalar.")

		assert (scalar > 0), "Scalar must be larger than zero!"

		children = [child / scalar for child in self.children.values()]

		return MealComponent(name=self.name,
							   children=children)

	def __add__(self, other):

		return self.add(other)


	def flatten(self):

		children = flatten(self)

		return MealComponent(name=self.name,
							 children=children,
							 unit=self.unit,
							 meta=self.meta)



	def to_dict(self):

		out_dict = dict()

		out_dict['name'] = self.name
		out_dict['value'] = self.value
		out_dict['unit'] = self.unit
		out_dict['materials'] = [{'name': child.name,
								  'cook_amt' : child.value,
								  'meta' : child.meta} for child in self.children.values()]

		return out_dict









