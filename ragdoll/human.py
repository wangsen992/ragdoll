"""
This is a script to faciliate the construction of Human objects.
"""
import copy

from .req import *


class Human(object):

    def __init__(self, 
    			 name='test', 
    			 gender='male', 
    			 age=25, 
    			 height=175, 
    			 weight=68, 
    			 PAL=1.2, 
    			 AMRD={"PROCNT" : 0.3,
						 "FAT"    : 0.2,
						 "CBH" : 0.5}):
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
        self.PAL = PAL
        self.AMRD = AMRD
        self.nutrients = Nutrients()


    def get_req(self):

        req = Requirement(self)

        req.get_energy()
        req.get_macro()
        req.get_micro()

        self.nutrients = req.nutrients

    def slice_nutrients(self, *nut_list):
        
        out_human = copy.deepcopy(self)
        out_nuts = out_human.nutrients[nut_list]

        out_human.nutrients = out_nuts

        return out_human

    def __repr__(self):

        return "Human Object\n" +\
               "name : {}\n".format(self.name) +\
               "gender : {}\n".format(self.gender) +\
               "age : {}\n".format(self.age) +\
               "height : {}\n".format(self.height) +\
               "weight : {}\n".format(self.weight) +\
               "PAL : {}\n".format(self.PAL) +\
               "AMRD : {}\n".format(self.AMRD) +\
               self.nutrients.__repr__()


