# -*- coding: utf-8 -*-
""" Composite structures for ragdoll compositions.

A composite structure is defined here to facilitate composition operations. 
The flexible use of Series and DataFrame and their integration with tree-like
structure is the key feature. 

By separating the nutrients and the ingredients, it is possible for future
extension with more databases. 
"""

import numpy as np
from pandas import Series, DataFrame

from .nutrients import Nutrients
from .flyweight import IngreFlyweightFactory

def Component(DataFrame):
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

	pass

def IngredientComponent(Component):

	pass

def BasketComponent(Component):

	pass

def MealComponent(Component):

	pass