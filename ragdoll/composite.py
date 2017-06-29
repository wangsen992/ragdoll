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

from collections import defaultdict

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

	def __init__(self, name, value, unit, abbr):
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

		"""

		self.name = name
		self.value = value
		self.unit = unit
		self.abbr = abbr


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

		return Nutrient(name=self.name,
						value=self.value + other.value,
						unit=self.unit,
						abbr=self.abbr)

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

		return Nutrient(name=self.name,
						value=self.value - other.value,
						unit=self.unit,
						abbr=self.abbr)

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
						abbr=self.abbr)

	def __rmul__(self, scalar):
		"""Reverse multiplication. 

		This is a supporting function for multiplication. Ensure commutative
		rules. It directly calls self.__mul__ method.

		Parameters
		----------
		scalar : float or int
			The scalar value to the multiplied with. 

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
							abbr=self.abbr)

		elif self.__type_test(other):

			return self.value / other.value

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
							abbr=self.abbr)

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
							abbr=self.abbr)

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

	def __repr__(self):
		"""The representation of objects of Nutrient class."""

		format_string = "name  : {name}\n" + \
						"value : {value:.3f}\n" + \
						"unit  : {unit}\n" + \
						"abbr  : {abbr}\n\n"
		return format_string.format(name=self.name,
									value=self.value,
									unit=self.unit,
									abbr=self.abbr)

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
			raise ValueError("Abbreviations not the same.")
			return False

		elif self.unit != other.unit:
			raise ValueError("Unit types not the same.")
			return False

		return True


class Nutrients(object):
	"""An organizer of a group of nutrients.

	This is an organizer of nutrients, it handles the operation among
	clusters of nutrients.

	Abbreviation, as the key of nutrients, are used for quick matching of 
	nutrients of the same type. The dictionary of abbreviation and nutrient
	names are defined in a separated file, e.g. NUTR_DEF_CUS.txt.
	
	An important concept of operation is whether use union or intersection 
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

	def __init__(self, source="unknown", input_nutrients=list()):
		"""Initiation of Nutrient object

		Initialization requires type and format check on the nutrient objects
		supplied. Therefore, the addition of nutrients can be handled by 
		__add_nutrients method, which conducts the type and format check.

		Parameters
		----------
		source : str
			The source name of the Nutrients, typically the name of ingredient
			containing the Nutrients object.
		input_nutrients : list
			A list of children (IngredientComponent or MealComponent) to be
			included at the initialization of the Nutrients object.

		"""

		self.source = source
		self.nutrients = dict()
		self.__add_nutrients(*input_nutrients)

		

	def __add_nutrients(self, *nutrients):
		"""Insert nutrients into the Nutrients object.

		Note
		----
		As the number of nutrients is not certain, asterisk (*) is added for 
		the function to be able to handle both single, double entry or entry 
		as a list. 
		
		Parameters
		----------
		*nutrients : Nutrient or list of Nutrient objects
			Nutrient object or a list of Nutrient objects to be added.
		
		"""


		for nutrient in nutrients:

			if nutrient.abbr in self.nutrients:
				# Cumulate nutrient values if there is existing Nutrient object
				# of the same type.

				assert self.nutrients[nutrient.abbr]._Nutrient__type_test(nutrient), "Nutrient not compatible with existing nutrient"
				self.nutrients[nutrient.abbr] = self.nutrients[nutrient.abbr] + nutrient
			else:
				# Add Nutrient to collection if no existing Nutrient object
				# of the same type. 
				self.nutrients[nutrient.abbr] = nutrient


	def __nutrient_check(nutrient):
		"""A nutrient check on inputting nutrients
		
		This is now only a loner function, not called anywhere. 		

		Check the type and format of the input nutrient. Only passed one can be
		added to the Nutrients object. 

		Currently, only the type check is conducted. Potentially in the future,
		a more sophisticated format can be implemented for better control.

		Parameters
		----------
		nutrient : Nutrient
			Input Nutrient object to be checked.

		"""

		# Check on type
		return type(nutrient) == Nutrient



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
		newNutrients_dict = dict()

		# Obtain the keys from both Nutrients objects. 
		self_keys = self.nutrients.keys()
		other_keys = other.nutrients.keys()

		# Perform addition.
		if method == "union":

			for abbr in self_keys | other_keys:

				if abbr in self_keys & other_keys:

					newNutrients_dict[abbr] = self.nutrients[abbr] + other.nutrients[abbr]

				elif abbr in self_keys and abbr not in other_keys:

					newNutrients_dict[abbr] = self.nutrients[abbr]

				elif abbr not in self_keys and abbr in other_keys:

					newNutrients_dict[abbr] = other.nutrients[abbr]

		elif method == "intersect":

			for abbr in self_keys & other_keys:

				newNutrients_dict[abbr] = self.nutrients[abbr] + other.nutrients[abbr]

		return Nutrients(source=self.source + "+" + other.source,
						 input_nutrients=list(newNutrients_dict.values()))

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

		newNutrients_dict = dict()

		self_keys = self.nutrients.keys()
		other_keys = other.nutrients.keys()

		if method == "union":

			for abbr in self_keys | other_keys:

				if abbr in self_keys & other_keys:

					newNutrients_dict[abbr] = self.nutrients[abbr] - other.nutrients[abbr]

				elif abbr in self_keys and abbr not in other_keys:

					newNutrients_dict[abbr] = self.nutrients[abbr]

				elif abbr not in self_keys and abbr in other_keys:

					newNutrients_dict[abbr] = float('-inf')

		if method == "intersect":

			for abbr in self_keys & other_keys:

				newNutrients_dict[abbr] = self.nutrients[abbr] - other.nutrients[abbr]

		return Nutrients(source=self.source + "-" + other.source,
						 input_nutrients=list(newNutrients_dict.values()))

	def __sub__(self, other):
		"""Wrapper function of self.sub for operation overloading on "-". """

		return self.sub(other, method="intersect")


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
		Nutrients
			A Nutrients object of with the same Nutrient objects, with value
			of each being Nutrient.value multiplied with the scalar. 

		"""

		if type(scalar) not in [int, float]:
			raise ValueError("Must be multiplied with a scalar.")

		assert (scalar >= 0), "Scalar must be equal or larger than zero!"

		newNutrients_dict = dict()

		for abbr in self.nutrients.keys():

			newNutrients_dict[abbr] = self.nutrients[abbr] * scalar

		return Nutrients(source=self.source + "*" + str(scalar),
						 input_nutrients=list(newNutrients_dict.values()))

	def __rmul__(self, scalar):
		"""Wrapper function of self.__mul__ for operation overloading on "*"."""

		return self.__mul__(scalar)

	def __truediv__(self, scalar):
		"""Division of a scalar.

		Note
		----
		This method currently enforces that : scalar > 0

		Parameters
		----------
		scalar : float or int
			The scalar value to the multiplied with. 

		Returns
		-------
		Nutrients
			A Nutrients object of with the same Nutrient objects, with value
			of each being Nutrient.value divided by the scalar. 

		"""

		if type(scalar) not in [int, float]:
			raise ValueError("Must be multiplied with a scalar.")

		assert (scalar > 0), "Scalar must be larger than zero!"

		newNutrients_dict = dict()

		for abbr in self.nutrients.keys():

			newNutrients_dict[abbr] = self.nutrients[abbr] / scalar

		return Nutrients(source=self.source + "/" + str(scalar),
						 input_nutrients=list(newNutrients_dict.values()))


	def __repr__(self):
		"""Representation of Nutrients object."""

		return "Source : {}\n".format(self.source) +\
			   "Number of nutrients : {}\n".format(len(self.nutrients)) +\
			   ''.join([nut.__repr__() for nut in self.nutrients.values()])


# Composite class for ingredients and meals

class Component(object):

	def __init__(self, name="unknown"):

		self.name = name
		self.value = 0
		self.unit = 'g'
		self.children = list()
		self.nutrients = Nutrients(source=name)


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

	def list_nutrients(self):

		return [nut.name for nut in self.nutrients.nutrients.values()]

	def display_macro(self):

		macro_nut_abbr = ['ENERC_KCAL','PROCNT', 'FAT', 'CHOCDF']

		for key in macro_nut_abbr:
			print(self.nutrients.nutrients[key])

	def to_json(self):

		pass


class IngredientComponent(Component):

	def __init__(self, name, value, nutrients, unit='g'):

		Component.__init__(self, name)
		self.value = value
		self.unit = unit
		self.nutrients = nutrients

	def add(self, other):

		if not issubclass(type(other), Component) :
			raise TypeError("Second argument not a sub-Component object")

		if type(other) == IngredientComponent:
			return BasketComponent(name='MyBasket',
								   children=[self, other])

		elif type(other) == BasketComponent:
			return BasketComponent(name='MyBasket',
								   children=[self, *other.children])

		elif type(other) == MealComponent:
			return BasketComponent(name='MyBasket',
								   children=[self, other])

	def __add__(self, other):

		return self.add(other)

	def __sub__(self, other):

		pass

	def __mul__(self, scalar):

		if type(scalar) not in [int, float]:
			raise ValueError("Must be multiplied with a scalar.")

		assert (scalar >= 0), "Scalar must be equal or larger than zero!"

		return IngredientComponent(name=self.name,
								   value=self.value * scalar,
								   unit=self.unit,
								   nutrients=self.nutrients * scalar)

	def __rmul__(self, scalar):

		return self.__mul__(scalar)

	def __truediv__(self, scalar):

		if type(scalar) not in [int, float]:
			raise ValueError("Must be multiplied with a scalar.")

		assert (scalar > 0), "Scalar must be larger than zero!"

		return IngredientComponent(name=self.name,
								   value=self.value / scalar,
								   unit=self.unit,
								   nutrients=self.nutrients / scalar)

	def __repr__(self):

		return "Ingredient\n" +\
			   "Name : {}\n".format(self.name) +\
			   "Value : {} {}\n".format(self.value, self.unit) +\
			   "Nutrients: \n" +\
			   self.nutrients.__repr__()

class BasketComponent(Component):

	def __init__(self, name, children=list(), unit='g'):

		Component.__init__(self, name)
		self.unit = unit
		self.children = children
		self.compute_value()
		self.compute_nutrition()

	def compute_nutrition(self):
		"Intersect addition is used implicitly."

		self.nutrients = sum([child.nutrients for child in self.children])

	def compute_value(self):

		self.value = sum([child.value for child in self.children])

	def update_attr(self):

		self.compute_nutrition()
		self.compute_value()

	def insert_child(self, child):
		"""
		Support only single entry now, types include IngredientComponent, 
		MealComponent.
		"""
		# Verify the type of the child
		if type(child) not in [IngredientComponent, MealComponent]:
			raise TypeError("Inserted child must be either IngredientComponent "+\
							"or MealComponent.")

		self.children.append(child)
		self.update_attr()

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

		if type(other) == IngredientComponent:
			return BasketComponent(name='MyBasket',
								   children=[*self.children, other])

		elif type(other) == BasketComponent:
			return BasketComponent(name='MyBasket',
								   children=[*self.children, *other.children])

		elif type(other) == MealComponent:
			return BasketComponent(name='MyBasket',
								   children=[*self.children, other])

	def __add__(self, other):

		return self.add(other)

	def __sub__(self, other):

		pass

	def __mul__(self, scalar):
		
		if type(scalar) not in [int, float]:
			raise ValueError("Must be multiplied with a scalar.")

		assert (scalar >= 0), "Scalar must be equal or larger than zero!"

		children = [child * scalar for child in self.children]

		return BasketComponent(name=self.name,
							   children=children)

	def __rmul__(self, scalar):

		return self.__mul__(scalar)

	def __truediv__(self, scalar):

		if type(scalar) not in [int, float]:
			raise ValueError("Must be multiplied with a scalar.")

		assert (scalar > 0), "Scalar must be larger than zero!"

		children = [child / scalar for child in self.children]

		return BasketComponent(name=self.name,
							   children=children)

	def convert2ingre(self, name):

		return IngredientComponent(name, 
								   value=self.value,
								   nutrients=self.nutrients, 
								   unit=self.unit)

	def convert2meal(self, name, recipe=None):

		"Simply create a meal object now, no recipes required."
		"This should be the only way to create a MealComponent object."

		return MealComponent(name=name,
							 children=self.children,
							 unit=self.unit)


class MealComponent(BasketComponent):

	def __init__(self, 
				 name, 
				 children,
				 unit='g'
				 ):

		BasketComponent.__init__(self, name, children, unit)
		self.compute_value()
		self.compute_nutrition()


	def __repr__(self):

		return "Meal \n" +\
			   "Name : {}\n".format(self.name) +\
			   "Value : {} {}\n".format(self.value, self.unit) +\
			   "Children \n{}\n".format([child.name for child in self.children]) +\
			   "Nutrients: \n" +\
			   self.nutrients.__repr__()


if __name__ == '__main__':
	
	# Test the behaviours of Nutrient
	protein = Nutrient(name='protein',
					   value=100,
					   unit='g',
					   abbr='prot')
	carbs = Nutrient(name='carbohydrate',
					 value=100,
					 unit='g',
					 abbr='cab')
	fat = Nutrient(name='fat',
				   value=100,
				   unit='g',
				   abbr='fat')
	print(protein)
	print(protein + protein * 0.5)

	# Test the behaviours of Nutrients
	Nut1 = Nutrients(source="Nut 1", input_nutrients=[protein, carbs, fat])
	print(Nut1)
	Nut2 = Nutrients(source="Nut 2", input_nutrients=[protein * 0.3, 
												  carbs * 1.5,
												  fat * 1.0,
												  carbs * 1.3])
	print(Nut2)

	Nut3 = Nut1 + Nut2

	print(Nut3)

	# Test the construction of Ingredient
	ingre1 = IngredientComponent(name='test_ingre', value=100, unit='g', nutrients=Nut1)
	print(ingre1)

	ingre2 = IngredientComponent(name='test_ingre2', value=100, unit='g', nutrients=Nut2)
	print(ingre2)
	meal = MealComponent(name='test_meal', children=[ingre1, ingre2])
	print(meal)

	meal2 = MealComponent(name='compound_meal', children=[ingre2, meal])




