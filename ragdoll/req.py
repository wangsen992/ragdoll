"""
This is a script to faciliate the construction of Requirement objects.
"""
from bson import ObjectId
import pandas as pd
import os

from .db import MongoDB
from .composite import Nutrient, Nutrients


nut_dict_file = "{root}/ragdoll/NUTR_DEF_more.csv".format(root=os.getcwd())
nut_dict_df = pd.read_csv(nut_dict_file, keep_default_na=False)


def Harris_Benedict_Revised(weight, height, age, gender, PAL):
    
    """
    TEE estimation using revised Harris Benedict revised equation. 
    Returns a dict containing the BMR(基础代谢(千卡)) and TEE('热量(千卡)') for 
    the given body info.
    
    weight: float, in kg;
    height: float, in cm;
    age   : float, in year;
    sex   : string, male or female;
    PAL   : Level of physical activity (according to equation supplements)
    """
    
    if gender == 'male':
        value = (88.362 + 13.397 * weight + 4.799 * height - 5.677 * age) * PAL
    elif gender == 'female':
        value = (447.593 + 9.247 * weight + 3.098 * height - 4.330 * age) * PAL
    
    BMR = Nutrient(name='Energy',
                   unit='kcal',
                   abbr='ENERC_KCAL',
                   source='Analytical',
                   name_source='Foodmate',
                   value=value)
    return BMR



class Requirement(Nutrients):

    def __init__(self, human):

        self.human = human
        self.nutrients = Nutrients()

    def get_energy(self, model=Harris_Benedict_Revised):

        energy = model(weight=self.human.weight,
                       height=self.human.height,
                       age=self.human.age,
                       gender=self.human.gender,
                       PAL=self.human.PAL)
        self.nutrients.add_nutrients(energy)

    def get_macro(self):
        """Obtain the macro nutrient values

        AMRD should be in such format:
            {"PROCNT" : 0.3,
             "FAT"    : 0.2,
             "CHOCDF" : 0.5}

        """

        energy = self.nutrients.nutrients['ENERC_KCAL']
        AMRD = self.human.AMRD

        prot = Nutrient(name="Protein",
                        unit='g',
                        value=energy.value * AMRD['PROCNT'] / 4.0,
                        abbr='PROCNT',
                        source='Analytical',
                        name_source='Foodmate')
        carbs = Nutrient(name="Carbohydrate",
                         unit='g',
                         value=energy.value * AMRD['CHOCDF'] / 4.0,
                         abbr='CBH',
                         source='Analytical',
                         name_source="Foodmate")
        fat = Nutrient(name="Lipid",
                       unit='g',
                       value=energy.value * AMRD['FAT'] / 9.0,
                       abbr='LIP',
                       source='Analytical',
                       name_source="Foodmate")

        self.nutrients.add_nutrients([prot, carbs, fat])

    def get_micro(self):

        table = pd.read_csv('ragdoll/nut_doc/nut_req_{}.csv'.format(self.human.gender), 
                            keep_default_na=False)
        nutrient_list = []

        for i in table.index:
            nut = table.loc[i]
            nutrient = Nutrient(name=str(nut['name']), 
                                 value=float(nut['value']), 
                                 unit=str(nut['unit']), 
                                 abbr=str(nut['abbr']),
                                 source="old_req",
                                 name_source="Foodmate")

            nutrient_list.append(nutrient)

        self.nutrients.add_nutrients(nutrient_list)


        



