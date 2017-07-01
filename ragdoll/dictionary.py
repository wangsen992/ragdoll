"""
A dictionary to faciliate the conformation of various formats and namings
of nutrients, units, and others to a unified format. 

A key information here is that the origin of the information plays a key
part in the translation between formats. For example, all nutrient level
information is defined in its respective sources of information, therefore 
the information is store at nutrient level. 

In terms of food names, it would be difficult to translate, however, this
is required when dealing with the *meishijie* database. 

"""
import os

import pandas as pd

from .composite import Nutrient, Nutrients

nut_dict_file = "{root}/ragdoll/NUTR_DEF_more.csv".format(root=os.getcwd())

class Dictionary(object):

	def __init__(self, dict_file=None):

		pass

	def translate(self, nutrient, target):

		pass



class NutrientDictionary(Dictionary):
	"""A dictionary object for helping translating Nutrient objects

	A dictionary file with predefined format is used here to faciliate 
	the translation. 

	USDA database info is used as the general template for both english
	and Chinese version of all nutrients, so are its codes, units and 
	abbreviations.

	A pandas dataframe is used to faciliate the translation. The columns are 
	in such order. 
		* code      : nutrient code as used in USDA database;
		* unit_USDA : nutrient unit as used in USDA database;
		* abbr      : nutrient abbreviation as used in USDA database;
		* name_USDA : nutrient name as used in USDA database;
		* name_Zh   : nutrient name in Chinese;
		* unit_Zh   : nutrient unit in Chinese;
		* prec      : unknown yet;
		* sort      : unknow yet;

	"""

	def __init__(self, dict_file=nut_dict_file):

		self.dict_file = dict_file
		self.dict_df = pd.read_csv(self.dict_file)

	def translate(self, nutrient, target):
		"""translate current nutrient to target format

		It is important to locate the current format name, and this is done
		by accessing the current source attribute or the code attribute of
		the Nutrient object, then the target value of the nutrient can be
		obtained. Both the nutrient name and unit will be changed. 

		Parameters
		----------
		nutrient : Nutrient
			Nutrient object to be translated.
		target : str
			The target format to be translated into.

		"""

		# Get current name_source
		cur_name_source = nutrient.name_source
		cur_name = nutrient.name
		cur_unit = nutrient.unit

		# Extract the line of information for this nutrient
		condition = (self.dict_df["name_{}".format(cur_name_source)] == cur_name) \
					& (self.dict_df["unit_{}".format(cur_name_source)] == cur_unit)
		nut_info = self.dict_df[condition]

		# get the new names and units
		new_name_source = target
		new_name = nut_info["name_{}".format(target)].values[0]
		new_unit = nut_info["unit_{}".format(target)].values[0]

		nutrient.name = new_name
		nutrient.unit = new_unit
		nutrient.name_source = new_name_source

class NutrientsDictionary(NutrientDictionary):
	"""A dictionary object for helping translating Nutrients objects

	A dictionary file with predefined format is used here to faciliate 
	the translation. 

	USDA database info is used as the general template for both english
	and Chinese version of all nutrients, so are its codes, units and 
	abbreviations.

	A pandas dataframe is used to faciliate the translation. The columns are 
	in such order. 
		* code      : nutrient code as used in USDA database;
		* unit_USDA : nutrient unit as used in USDA database;
		* abbr      : nutrient abbreviation as used in USDA database;
		* name_USDA : nutrient name as used in USDA database;
		* name_Zh   : nutrient name in Chinese;
		* unit_Zh   : nutrient unit in Chinese;
		* prec      : unknown yet;
		* sort      : unknow yet;

	"""

	def __init__(self, dict_file=nut_dict_file):

		NutrientDictionary.__init__(self, dict_file=dict_file)

	def translate(self, nutrients, target):

		for nutrient in nutrients.values():

			super().translate(nutrient, target)
			# print(nutrient)
