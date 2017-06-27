"""
Key objects for the package, including basic component, ingredient, meal, 
nutrients, and their interactions. 

The idea is to apply a composite structure, such that ingredient and meal
can be treated as the same structure by clients. Addition and substraction 
should be abstracted with plus and minus signs for simple manipulation. 
"""

class Nutrient(object):

	def __init__(self, name, value, unit, abbr):

		self.name = name
		self.value = value
		self.unit = unit
		self.abbr = abbr
		self.desc = dict()
		self.desc['missing_info'] = list()

	def __add__(self, other):

		if self.name != other.name:
			raise ValueError("Nutrient names not the same.")

		if self.unit != other.unit:
			raise ValueError("Unit types not the same.")

		if self.abbr != other.abbr:
			raise ValueError("Abbreviations not the same.")

		return Nutrient(name=self.name,
						value=self.value + other.value,
						unit=self.unit,
						abbr=self.abbr)

	def __sub__(self, other):

		if self.name != other.name:
			raise ValueError("Nutrient names not the same.")

		if self.unit != other.unit:
			raise ValueError("Unit types not the same.")

		if self.abbr != other.abbr:
			raise ValueError("Abbreviations not the same.")

		return Nutrient(name=self.name,
						value=self.value - other.value,
						unit=self.unit,
						abbr=self.abbr)

	def __mul__(self, scalar):

		if type(scalar) not in [int, float]:
			raise ValueError("Must be multiplied with a scalar.")

		return Nutrient(name=self.name,
						value=self.value * scalar,
						unit=self.unit,
						abbr=self.abbr)

	def __rmul__(self, scalar):

		return self.__mul__(scalar)

	def __truediv__(self, scalar):

		if type(scalar) not in [int, float]:
			raise ValueError("Must be multiplied with a scalar.")

		return Nutrient(name=self.name,
						value=self.value / scalar,
						unit=self.unit,
						abbr=self.abbr)


	def __repr__(self):

		format_string = "name  : {name}\n" + \
						"value : {value:.3f}\n" + \
						"unit  : {unit}\n" + \
						"abbr  : {abbr}"
		return format_string.format(name=self.name,
									value=self.value,
									unit=self.unit,
									abbr=self.abbr)

class _Nutrients(object):
	"""This is an organizer of nutrients"""

	def __init__(self, name, nutrients=dict()):
		self.nutrients = nutrients
		self.source = name

	def _add_nutrients(self, *nutrients):
		"This method is used to construct Nutrients object"

		for nutrient in nutrients:

			# Check type
			if type(nutrient) != Nutrient:
				raise TypeError("Input nutrient must be in Nutrient Class.")

			if nutrient.name in self.nutrients:
				raise ValueError("nutrient already present in the Object.")

			self.nutrients[nutrient.abbr] = nutrient

	def __add__(self, other):
		"This is a manipulation on the _Nutrients objects"

		# check other type
		if type(other) != _Nutrients:
			raise TypeError("Second argument not Nutrients object")

		newNutrients_dict = dict()

		self_keys = self.nutrients.keys()
		other_keys = other.nutrients.keys()

		for abbr in self_keys | other_keys:

			if abbr in self_keys & other_keys:

				newNutrients_dict[abbr] = self.nutrients[abbr] + other.nutrients[abbr]

			elif abbr in self_keys and abbr not in other_keys:

				newNutrients_dict[abbr] = self.nutrients[abbr]
				newNutrients_dict[abbr].desc['missing_info'].append(other.name)

			elif abbr not in self_keys and abbr in other_keys:

				newNutrients_dict[abbr] = other.nutrients[abbr]
				newNutrients_dict[abbr].desc['missing_info'].append(self.name)

		return _Nutrients(name=self.name + "+" + other.name,
						  nutrients=newNutrients_dict)

	def __sub__(self, other):

		# check other type
		if type(other) != _Nutrients:
			raise TypeError("Second argument not Nutrients object")

		newNutrients_dict = dict()

		self_keys = self.nutrients.keys()
		other_keys = other.nutrients.keys()

		for abbr in self_keys | other_keys:

			if abbr in self_keys & other_keys:

				newNutrients_dict[abbr] = self.nutrients[abbr] - other.nutrients[abbr]

			elif abbr in self_keys and abbr not in other_keys:

				newNutrients_dict[abbr] = self.nutrients[abbr]
				newNutrients_dict[abbr].desc['missing_info'].append(other.name)

			elif abbr not in self_keys and abbr in other_keys:

				newNutrients_dict[abbr] = float('-inf')
				newNutrients_dict[abbr].desc['missing_info'].append(self.name)

		return _Nutrients(name=self.name + "-" + other.name,
						  nutrients=newNutrients_dict)

	def __mul__(self, scalar):

		if type(scalar) not in [int, float]:
			raise ValueError("Must be multiplied with a scalar.")

		newNutrients_dict = dict()

		for abbr in self.nutrients.keys():

			newNutrients_dict[abbr] = self.nutrients[abbr] * scalar

		return _Nutrients(name=self.name + "*" + str(scalar),
						  nutrients=newNutrients_dict)

	def __rmul__(self, scalar):

		return self.__mul__(scalar)

	def __truediv__(self, scalar):

		if type(scalar) not in [int, float]:
			raise ValueError("Must be multiplied with a scalar.")

		newNutrients_dict = dict()

		for abbr in self.nutrients.keys():

			newNutrients_dict[abbr] = self.nutrients[abbr] / scalar

		return _Nutrients(name=self.name + "/" + str(scalar),
						  nutrients=newNutrients_dict)



# Composite class for ingredients and meals

class Component(object):

	def __init__(self, name="unnamed"):

		self.name = name
		self.amt = 0
		self.unit = 'g'
		self.children = list()
		self.nutrients = _Nutrients(name=name)



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

	def __init__(self, name, amt, nutrients, unit='g', ingre_group=None, portions=None):

		Component.__init__(self, name)
		self.amt = amt
		self.unit = unit
		self.nutrients = nutrients
		self.ingre_group = ingre_group
		self.portions = portions

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




class MealComponent(Component):

	def __init__(self, 
				 name, 
				 children, 
				 meal_group, 
				 portions):

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

	def construction(self):
		"Construct the meal information from its children. "

		pass







		



