"""
Key objects for the package, including basic component, ingredient, meal, 
nutrients, and their interactions. 

The idea is to apply a composite structure, such that ingredient and meal
can be treated as the same structure by clients. Addition and substraction 
should be abstracted with plus and minus signs for simple manipulation. 

Another potential usage is to map new database information into objects defined
in this module, and output into desired format. 
"""

from collections import defaultdict

class Nutrient(object):
	"""
	Nutrient object handles individual-nutrient-level operations.

	Future customization of nutrient functions can be facilitated by 
	using a function to create functions. Methods provided to provide 
	functions with different behaviours based on nutrient attributes. 

	Currently Nutrient objects do not handle conversion of units.
	"""

	def __init__(self, name, value, unit, abbr):

		self.name = name
		self.value = value
		self.unit = unit
		self.abbr = abbr


	def __add__(self, other):

		assert self.__type_test(other), "Type mismatch between two nutrient objects."

		return Nutrient(name=self.name,
						value=self.value + other.value,
						unit=self.unit,
						abbr=self.abbr)

	def __sub__(self, other):

		assert self.__type_test(other), "Type mismatch between two nutrient objects."

		assert (self.value >= other.value), "First nutrient value smaller than the second."

		return Nutrient(name=self.name,
						value=self.value - other.value,
						unit=self.unit,
						abbr=self.abbr)

	def __mul__(self, scalar):

		if type(scalar) not in [int, float]:
			raise ValueError("Must be multiplied with a scalar.")

		assert (scalar >= 0), "Scalar must be equal or larger than zero!"

		return Nutrient(name=self.name,
						value=self.value * scalar,
						unit=self.unit,
						abbr=self.abbr)

	def __rmul__(self, scalar):

		return self.__mul__(scalar)

	def __truediv__(self, other):
		"""
		Supports division by both scalar and nutrient of same type. 

		if scalar provided, returns a Nutrient object;
		if Nutrient object of same type provided, returns a scalar.
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
		"""
		Supports floor division by both scalar and nutrient of same type. 

		if scalar provided, returns a Nutrient object;
		if Nutrient object of same type provided, returns a scalar.
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
		"""
		Supports floor division by both scalar and nutrient of same type. 

		if scalar provided, returns a Nutrient object;
		if Nutrient object of same type provided, returns a scalar.
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

		if self.__type_test(other):

			return self.value < other.value

	def __le__(self, other):

		if self.__type_test(other):

			return self.value <= other.value

	def __eq__(self, other):

		if self.__type_test(other):

			return self.value == other.value

	def __ne__(self, other):
		"Inequality can only be tested with nutrients of the same type."

		if self.__type_test(other):

			return self.value != other.value

	def __ge__(self, other):

		if self.__type_test(other):

			return self.value >= other.value

	def __gt__(self, other):

		if self.__type_test(other):

			return self.value > other.value

	def __repr__(self):

		format_string = "name  : {name}\n" + \
						"value : {value:.3f}\n" + \
						"unit  : {unit}\n" + \
						"abbr  : {abbr}\n\n"
		return format_string.format(name=self.name,
									value=self.value,
									unit=self.unit,
									abbr=self.abbr)

	def __type_test(self, other):

		"Test condition for operations. True to allow operations of same type."
		if type(other) != Nutrient:
			raise TypeError("Second argument must be a Nutrient object.")
			return False

		if self.name != other.name:
			raise ValueError("Nutrient names not the same.")
			return False

		elif self.unit != other.unit:
			raise ValueError("Unit types not the same.")
			return False			

		elif self.abbr != other.abbr:
			raise ValueError("Abbreviations not the same.")
			return False

		return True



class Nutrients(object):
	"""
	This is an organizer of nutrients, it handles the operation among
	a cluster of nutrients.

	Abbreviation, as the key of nutrients, are used for quick matching of 
	nutrients of the same type. 
	
	An important operation is to get union and intersection of available 
	nutrients from groups of nutrients. 

	Missing info handling (for mismatch of nutrients) is completely ignored
	in this version. 

	Divsions between Nutrients is unknown. Not defined right now.
	"""

	def __init__(self, source="unknown", input_nutrients=list()):
		"""
		Initialization requires type and format check on the nutrient objects
		supplied. Therefore, the addition of nutrients can be handled by 
		add_nutrients method, which conducts the type and format check.
		"""

		self.source = source
		self.nutrients = dict()
		self.add_nutrients(*input_nutrients)

	def add_nutrients(self, *nutrients):
		"""
		This method is used to construct Nutrients object.

		If a list is inputted, add asterisk to tell the method that it is a 
		list.

		For a list with number of nutrients of the same type, consolidate first 
		before addition.
		"""

		for nutrient in nutrients:

			if nutrient.abbr in self.nutrients:
				assert self.nutrients[nutrient.abbr]._Nutrient__type_test(nutrient), "Nutrient not compatible with existing nutrient"
				self.nutrients[nutrient.abbr] = self.nutrients[nutrient.abbr] + nutrient
			else:
				self.nutrients[nutrient.abbr] = nutrient


	def __nutrient_check(nutrient):

		"""
		Check the type and format of the input nutrient. Only passed one can be
		added to the Nutrients object. 

		Currently, only the type check is conducted. Potentially in the future,
		a more sophisticated format can be implemented for better control.
		"""

		# Check on type
		return type(nutrient) == Nutrient



	def add(self, other, method="intersect"):
		"""
		This is a manipulation on the Nutrients objects. This is then reused 
		for operation overloading. 

		Arguments:
		other: Nutrients, 
		method: str, method for handling mismatch between Nutrients objects. 
				"union" : union of nutrients, annotation in nutrient
				"intersect" : intersect of nutrients, no annotation possible.
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

		return self.add(other, method="intersect")

	def sub(self, other, method="intersect"):

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

		return self.sub(other, method="intersect")


	def __mul__(self, scalar):

		if type(scalar) not in [int, float]:
			raise ValueError("Must be multiplied with a scalar.")

		assert (scalar >= 0), "Scalar must be equal or larger than zero!"

		newNutrients_dict = dict()

		for abbr in self.nutrients.keys():

			newNutrients_dict[abbr] = self.nutrients[abbr] * scalar

		return Nutrients(source=self.source + "*" + str(scalar),
						 input_nutrients=list(newNutrients_dict.values()))

	def __rmul__(self, scalar):

		return self.__mul__(scalar)

	def __truediv__(self, scalar):

		if type(scalar) not in [int, float]:
			raise ValueError("Must be multiplied with a scalar.")

		assert (scalar > 0), "Scalar must be larger than zero!"

		newNutrients_dict = dict()

		for abbr in self.nutrients.keys():

			newNutrients_dict[abbr] = self.nutrients[abbr] / scalar

		return Nutrients(source=self.source + "/" + str(scalar),
						 input_nutrients=list(newNutrients_dict.values()))


	def __repr__(self):

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


class IngredientComponent(Component):

	def __init__(self, name, value, nutrients, unit='g'):

		Component.__init__(self, name)
		self.value = value
		self.unit = unit
		self.nutrients = nutrients

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

	def __repr__(self):

		return "Ingredient\n" +\
			   "Name : {}\n".format(self.name) +\
			   "Value : {} {}\n".format(self.value, self.unit) +\
			   "Nutrients: \n" +\
			   self.nutrients.__repr__()




class MealComponent(Component):

	def __init__(self, 
				 name, 
				 children,
				 unit='g'
				 ):

		Component.__init__(self, name)
		self.unit = unit
		self.children = children
		self.__compute_value()
		self.__compute_nutrition()


	def __compute_nutrition(self):

		nutrients = Nutrients(source=self.name)
		for child in self.children:
			if type(child) == IngredientComponent:
				nutrients = nutrients.add(child.nutrients, method="union")

			elif type(child) == MealComponent:
				nutrients = nutrients.add(child.nutrients, method="union")

		self.nutrients = nutrients

	def __compute_value(self):

		self.value = sum([child.value for child in self.children])

	def __update_attr(self):

		self.__compute_nutrition()
		self.__compute_value()

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




