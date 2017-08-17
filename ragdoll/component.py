# -*- coding: utf-8 -*-
"""Composite data structures

After a lot of time of fruitless trial and error, a possibly useful revelation occurs to me that I should start with what is actually useful for now.

Right now, there are two main things important at hand:

Composition: how to organize the hierarchical structure of ingredients, meals, diets and more.
Computation: how to facilitate the computation processes.
Composition and computation are interconnected. As for computation, available python packages normally use NumPy, Pandas and SciPy, it is thus essential to have easy to use conversion between the data structures provided and numpy & pandas series and dataframe.

A pretty cool feature that should be included is the concept of basket and meal. 
* A basket allows its children to change their relative weights to each other. 
* A meal have its children's ratios locked, thus any change to the total amount of the basket will scale the amounts of children proportionally.

There are four types of methods provided for the general data structure:

* I/O methods
    *from_doc(doc)
    *to_doc(self)
* Property methods
    * children: a list of children (empty for Ingredient)
    * value : current value (scalar object)
    * nutrients : current nutrients values (nutrients object)
    * amounts : current value of children (first level only) (series object)
    * child_nutrients : current nutrients values of children (dataframe object)
    * default: same object with value as 100g
* Manipulation methods
    * set_value(self, int | list | array)
    * add_children(self, children)
    * remove_children(self, children)
    * slice_nutrients(self, list)
    * slice_children(self, list)
* Conversion methods
    * from_pd(self, amounts) [This is removed as set_values can perform the same task.]
"""

import abc
import copy
from collections import defaultdict, OrderedDict

import pandas as pd

from .nutrient import Nutrient, Nutrients
from .nutrient import key_matching
from .nutrient import std_nut
from .loader import Loader

recipe_title_format_str = "{index:<5} {value:<10} {db:10s} {name: <20s}\n"
recipe_entry_format_str = "{index:<5} {value:<10.1f} {db:10s} {name: <20s}\n"

class Component(metaclass=abc.ABCMeta):
    """
    Declare the interface for objects in the composition.
    Implement default behavior for the interface common to all classes,
    as appropriate.
    Declare an interface for accessing and managing its child
    components.
    Define an interface for accessing a component's parent in the
    recursive structure, and implement it if that's appropriate
    (optional).
    """

    # I/O methods
    @staticmethod
    @abc.abstractmethod
    def from_doc(doc):
        pass

    @abc.abstractmethod
    def to_doc(self):
        pass

    # Property methods
    @property
    @abc.abstractmethod
    def children(self):
        pass

    @property
    @abc.abstractmethod
    def value(self):
        pass

    @property
    @abc.abstractmethod
    def nutrients(self):
        pass

    @property
    @abc.abstractmethod
    def amounts(self):
        pass

    @property
    @abc.abstractmethod
    def child_nutrients(self):
        pass

    @property
    @abc.abstractmethod
    def default(self):
        pass

    # manipulation methods
    @abc.abstractmethod
    def set_value(self, other, in_place=False):
        pass

    @abc.abstractmethod
    def add_children(self, *components):
        pass

    @abc.abstractmethod
    def remove_children(self, *key):
        pass

    @abc.abstractmethod
    def slice_nutrients(self, *nut_list):
        pass

    @abc.abstractmethod
    def slice_children(self, *chd_list):
        pass

    # Conversion methods
    # None implemented

    @abc.abstractmethod
    def __repr__(self):
        pass


    # test function, remove later.
    def show_text(self):

        print("This is a test string.")


class Composite(Component):
    """
    Define behavior for components having children.
    Store child components.
    Implement child-related operations in the Component interface.
    """

    def __init__(self, name, children, collection='', item_id=''):

        self.name = name
        self._collection = collection
        self._item_id = item_id
        self._children = OrderedDict()
        self.add_children(*children)
        self._doc = {}

    # I/O methods
    @staticmethod
    def from_doc(doc):

        name = doc['name']['long']
        children = []
        for child in doc['children']:
            if 'children' in child:
                children.append(Composite.from_doc(child))
            else:
                children.append(Ingredient.from_doc(child))

        out_comp = Composite(name=name,
                             children=children,
                             collection=doc['collection'],
                             item_id = doc['_id'])
        out_comp._doc = doc
        return out_comp

    def to_doc(self):
        
        out_doc = {}
        if len(self._doc) != 0:
            out_doc['name'] = self._doc['name']
        else:
            out_doc['name'] = {'sci' : '', 'common' : [], 'long' : self.name}
        out_doc['collection'] = self._collection
        out_doc['_id'] = self._item_id

        # this only apply to Ingredient (leaf)
        out_doc['children'] = [child.to_doc() for child in self.children]
        out_doc['nutrients'] = self.nutrients.to_doc()

        return out_doc



    # Property methods
    @property
    def children(self):

        return list(self._children.values())


    @property
    def value(self):

        if len(self._children) == 0:
            return 0
        else:
            return sum([child.value for child in self.children])  
    

    @property
    def nutrients(self):

        if len(self._children) == 0:
            return Nutrients()

        else:
            return Nutrients.sum([child.nutrients for child in self.children])
   
    @property
    def amounts(self):

        data = []
        index = []

        for child in self.children:
            data.append(child.value)
            index.append(child.name)

        return pd.Series(data=data, index=index, name=self.name)


    @property
    def child_nutrients(self):

        names = [child.name for child in self.children]
        nut_values = [child.nutrients.to_series() for child in self.children]

        return pd.DataFrame(nut_values,
                            index=names)

    @property
    def default(self):
        """default value 

        For the basic composite, every children is default to 100g.
        """

        default_children = [child.default for child in self.children]

        out_comp = copy.deepcopy(self)
        out_comp._children = OrderedDict()
        out_comp.add_children(*default_children)

        return out_comp

    # Manipulation method
    def set_value(self, other, in_place=False):

        if type(other) in [int, float]:

            raise TypeError("Values to be set must be a list.")

        if len(other) != len(self._children):

            raise ValueError("Input factor does not have the same length.")

        if in_place:
            for child, new_value in zip(self.children, other):
                child.set_value(new_value, in_place=True)
        else:
            out_composite = copy.deepcopy(self)
            for child, new_value in zip(out_composite.children, other):
                child.set_value(new_value, in_place=True)

            return out_composite

    def add_children(self, *components):

        for component in components:
            self._children[component.name] = component

    def remove_children(self, *keys):

        for key in keys:
            del self._children[key]

    def slice_nutrients(self, *nut_list):
        
        out_composite = copy.deepcopy(self)
        
        for key, child in out_composite._children.items():

            out_composite._children[key] = out_composite._children[key].slice_nutrients(*nut_list)

        return out_composite


    def slice_children(self, *chd_list):
        
        out_composite = copy.deepcopy(self)
        out_composite._children = OrderedDict()

        for child_name in chd_list:

            if child_name in self._children:
                out_composite._children[child_name] = self._children[child_name]
            else: 
                raise IndexError("Given index not present in children.")

        return out_composite


    def __repr__(self):

        name_str = "Name: {name}\n".format(name=self.name)
        value_str = "Value: {value}\n".format(value=self.value)
        recipe_title_str = recipe_title_format_str.format(index="INDEX",
                                                          name="NAME",
                                                          value="VALUE",
                                                          db="COLLECTION"
                                                          )

        recipe_entry_str = ''.join([recipe_title_format_str.format(index=i,
                                                           name=child.name,
                                                           value=child.value,
                                                           db=child._collection
                                                          )
                            for i, child in enumerate(self.children)])

        return name_str + value_str + recipe_title_str \
               + recipe_entry_str + '\n' + self.nutrients.__repr__()


class Ingredient(Component):
    """
    Represent leaf objects in the composition. A leaf has no children.
    Define behavior for primitive objects in the composition.
    """

    def __init__(self, 
                 name,
                 nutrients,
                 collection = '',
                 item_id = ''):

        self.name = name
        self._nutrients = nutrients
        self._collection = collection
        self._item_id = item_id
        self._value = 100
        self._doc = {}
        self._children = OrderedDict()

    # I/O methods
    @staticmethod
    def from_doc(doc):

        out_ingre = Ingredient(name=doc['name']['long'],
                               nutrients=Loader.nutrients_loader(doc['nutrients'])[std_nut],
                               collection=doc['collection'],
                               item_id=doc['_id'])
        out_ingre._doc = doc

        return out_ingre

    def to_doc(self):

        out_doc = {}
        out_doc['_id'] = self._item_id
        out_doc['collection'] = self._collection
        out_doc['value'] = self.value
        out_doc['nutrients'] = self._nutrients.to_doc()
        
        try:
            out_doc['name'] = self._doc['name']
        except KeyError:
            out_doc['name'] = {'sci' : '', 'common' : [], 'long' : self.name}

        return out_doc

    # Property methods
    @property
    def children(self):

        return list(self._children.values())

    @property
    def value(self):

        return self._value

    @property
    def nutrients(self):

        return self._nutrients * self._value / 100

    @property
    def amounts(self):

        return pd.Series()

    @property
    def child_nutrients(self):

        return pd.DataFrame(columns=list(self._nutrients.keys()))

    @property
    def default(self):

        out_ingre = copy.deepcopy(self)
        out_ingre._value = 100
        return out_ingre

    # Manipulation methods
    def set_value(self, other, in_place=False):
        
        if in_place:

            self._value = other

        else:

            out_ingre = copy.deepcopy(self)
            out_ingre._value = other
            return out_ingre

    def add_children(self, *components):
        
        raise TypeError("Leaf component cannot add children.")

    def remove_children(self, *key):
        raise TypeError("Leaf component cannot remove children.")

    def slice_nutrients(self, *nut_list):
        

        out_ingre = copy.deepcopy(self)
        out_nuts = out_ingre.nutrients[nut_list]

        out_ingre._nutrients = out_nuts

        return out_ingre

    def slice_children(self, *chd_list):
        
        raise TypeError("Ingredient is a leaf object, cannot be sliced anymore.")

    def __repr__(self):
        
        return "Ingredient\n" +\
               "Name : {}\n".format(self.name) +\
               "Value : {}\n".format(self.value) +\
               "Nutrients: \n" +\
               self.nutrients.__repr__()


def main():
    pass


