# -*- coding: utf-8 -*-
"""The most basic object in Ragdoll, amount.

Amount object mainly exist to handle algebraic operations with physical
meanings. For example, 

	1g + 10g = 11g
	1g + 1kg = 1.001kg
	1cm + 1dm = 1.1dm
	1g + 1cm : not valid!!!!!

The handling on unit is supported beyond the scope of user. However, it
could be possible for users to apply unit conversion operations on those
amount objects.
"""

mass_conversion_dict = {'g' : 1,
						'mg' : 1e-3,
						'µg' : 1e-6,
						'kg' : 1e3}
length_conversion_dict = {'m' : 1,
						  'cm' : 1e-2,
						  'mm' : 1e-3}
conversion_dict = {'mass' : mass_conversion_dict,
				   'length' : length_conversion_dict}

# Module level functions

def find_type(unit):
	"""Find the type of the unit.
	"""

	for name, d in conversion_dict.items():
		if unit in d:
			return name
	else:
		raise TypeError("Invalid input unit.")

def find_target_unit(amtA, amtB):

	target_unit = amtA.unit \
		  if conversion_dict[amtA.value_type][amtA.unit] >= \
		     conversion_dict[amtB.value_type][amtB.unit] \
		  else amtB.unit

	return target_unit

# Main module object

class Amount(object):
	"""A help class coodinating values and units.

	Note
	----
	Default unit conversion direction is upward. 

	"""

	def __init__(self, value, unit):
		"""As name suggests."""

		self.value = value
		self.unit = unit
		self.value_type = find_type(unit)


	def convert(self, target_unit):
		"""Convert the value from one unit into another"""

		if self.value_type != find_type(target_unit):

			raise TypeError("target_unit is not the same type.")

		conversion_factor = conversion_dict[self.value_type][self.unit] \
						   / conversion_dict[self.value_type][target_unit]

		target_value = self.value * conversion_factor

		return Amount(value=target_value,
					  unit=target_unit)


	def __add__(self, other):
		"""Summation between two Amount objects"""

		# Perform type check
		self.__type_check(other)

		# Consolidate units before operation

		target_unit = self.__find_target_unit(other)

		# Obtain value

		new_self = self.convert(target_unit)
		new_other = other.convert(target_unit)

		return Amount(value=new_self.value + new_other.value,
					  unit=target_unit)
	
	def __sub__(self, other):
		"""subtraction between two Amount objects"""

		# Perform type check
		self.__type_check(other)

		# Consolidate units before operation

		target_unit = self.__find_target_unit(other)

		# Obtain value

		new_self = self.convert(target_unit)
		new_other = other.convert(target_unit)

		return Amount(value=new_self.value - new_other.value,
					  unit=target_unit)

	def __mul__(self, scalar):
		"""Multiplication between Amount object and scalar."""

		# Perform type check
		if type(scalar) not in [int, float]:
			raise TypeError("Amount object must be multiplied with scalar.")

		# Perform operation
		return Amount(value=self.value * scalar,
					  unit=self.unit)

	def __rmul__(self, scalar):
		"""Multiplication between Amount object and scalar."""

		return self.__mul__(scalar)

	def __truediv__(self, other):
		"""Multiplication between Amount object and scalar or Amount obj."""

		if type(other) in [int, float]:
			# Perform operation
			return Amount(value=self.value / other,
						  unit=self.unit)

		elif type(other) == Amount:
			# Perform type check
			self.__type_check(other)

			# Consolidate unit
			target_unit = self.__find_target_unit(other)

			# Obtain value

			new_self = self.convert(target_unit)
			new_other = other.convert(target_unit)

			return new_self.value / new_other.value

		else:
			raise TypeError("Amount object must be divided with a scalar or Amount object.")



	def __find_target_unit(self, other):

		target_unit = find_target_unit(self, other)

		return target_unit

	def __type_check(self, other):

		# First check other is Amount object
		if type(other) != Amount:
			raise TypeError("Second argument is not Amount object.")

		# Second check type of Amount objects
		if self.value_type != other.value_type:
			raise TypeError("Second argument is not the same type.")

	def __repr__(self):

		return "{o.value}{o.unit}".format(o=self)

if __name__ == '__main__':
	
	val1 = Amount(value=10, unit='g')
	val2 = Amount(value=10, unit='mg')
	val3 = Amount(value=5, unit='cm')
	print(val1)
	print(val2)
	print(val3)

	out_val1 = val1 + val1
	print(out_val1)  # result: 20.01g
	out_val2 = val1 + val2
	print(out_val2)  # result: 10.01g
	out_val3 = val1 / val2
	print(out_val3)  # result : 1000.0



