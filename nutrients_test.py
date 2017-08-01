
import random

from ragdoll import *


def concat(list_of_comps):
    
    """Concatenate a list of components
    
    Ingredient and Meal are treated the same, basket is expands to 
    first-level children when concatenated. A basket component is 
    returned.
    
    list_of_comps: list
        A list of sub-Component objects.
    """
    
    list_of_baskets = [comp for comp in list_of_comps if type(comp) == BasketComponent]
    basket_item_list = []
    
    for basket in list_of_baskets:
        basket_item_list.extend(list(basket.children.values()))
    
    list_of_items = [comp for comp in list_of_comps if type(comp) != BasketComponent].extend(basket_item_list)
    print(type(list_of_items))
    
    print(list_of_items)

    return BasketComponent(name='',
                           children=list_of_items,
                           unit='g')


if __name__ == '__main__':
	sample1 = mongo.database['FM'].find()[random.randint(0,1000)]
	nut_obj1 = Loader.nutrients_loader(sample1['nutrients'])[std_nut]
	ingre1 = Loader.ingre_loader(sample1)[std_nut]

	sample2 = mongo.database['FM'].find()[random.randint(0,1000)]
	nut_obj2 = Loader.nutrients_loader(sample2['nutrients'])[std_nut]
	ingre2 = Loader.ingre_loader(sample2)[std_nut]
