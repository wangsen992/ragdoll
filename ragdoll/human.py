"""
This is a script to faciliate the construction of Human objects.
"""

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
						 "CHOCDF" : 0.5}):
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


    def get_req(self):

        req = Requirement(self)
        print(type(req))

        req.get_energy()
        req.get_macro()
        req.get_micro()

        self.nutrients = req.nutrients


