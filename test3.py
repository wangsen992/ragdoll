"""
A test for ragdoll.
"""

from ragdoll import *

mongo = MongoDB(host='47.93.246.201', 
				port=27017, 
				database='eatech', 
				user='harry', 
				password='password',
				collections=['FM'])


test_human = Human()
test_human.get_req()
print(test_human.nutrients)

sel = {'range' : [{'abbr' : 'PROCNT', 'value' : [30, 100]}]}
ing_list = [mongo.retrieve_item('FM', str(doc['_id'])) for doc in mongo.retrieve_list(sel)]
test_basket = BasketComponent(name='test',children=ing_list)

new_baskaet = test_basket[list(test_human.nutrients.keys())]

test_ing = new_baskaet.loc('榛子(炒)')

print(test_ing.nutrients / test_human.nutrients)