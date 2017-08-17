import pandas as pd

from ragdoll import *

mongo = MongoDB(host='47.93.246.201', 
				port=27017, 
				database='eatech', 
				user='harry', 
				password='password',
				collections=['USDA'])

abbr_conv = pd.read_csv('usda2std.csv')

target_col = 'usda'

vite_content = ['VITEA', 'TOCPHA', 'TOCPHB', 'TOCPHG', 'TOCPHD',
				'TOCTRA', 'TOCTRB', 'TOCTRG', 'TOCTRD']

def update_usda_doc(doc):

	new_doc = {}

	# ingre level
	new_doc['name'] = doc['name']
	new_doc['_id'] = doc['_id']
	new_doc['nutrients'] = []
	vite_amt = 0

	for nut in doc['nutrients']:

		if nut['abbr'] in abbr_conv['abbr_usda'].values:

			nut_info = abbr_conv[abbr_conv['abbr_usda'] == nut['abbr']]
			name = nut_info['name'].values[0]
			abbr = nut_info['abbr'].values[0]
			unit = nut['units']
			amt = nut['value']

			new_doc['nutrients'].append({'name' : name,
										 'abbr' : abbr,
										 'unit' : unit,
										 'value' : amt})

		elif nut['abbr'] in vite_content:
			vite_amt += nut['value']

		else: 
			continue

	vite_doc = {'name' : 'Vitamin E',
				'abbr' : 'VITE',
				'unit' : 'mg',
				'value' : vite_amt}
	new_doc['nutrients'].append(vite_doc)

	new_doc['group'] = doc['group']


	return new_doc


if __name__ == '__main__':
	
	# ingre_doc = mongo.retrieve_item('USDA', "59451260c6d282587a30749a")
	# new_doc = update_usda_doc(ingre_doc)
	# ingre = Loader.ingre_loader(new_doc)

	# get cursor for source collection
	old_cursor = mongo.database['USDA'].find()
	old_count = old_cursor.count()
	print("Total number of docs in USDA: {}".format(old_count))

	# get existing names for check
	new_name_cursor = mongo.database['usda'].find(projection={'_id':0, 'name.long':1})
	new_name_list = [doc['name']['long'] for doc in new_name_cursor]
	print("current number of entries in usda : {}\n".format(len(new_name_list)))

	# recreate a new usda

	for i, doc in enumerate(mongo.database['USDA'].find()):

		if doc['name']['long'] in new_name_list:
			continue
		new_doc = update_usda_doc(doc)
		mongo.database['usda'].insert(new_doc)

		if i % 200 == 0:
			print("Progress report: {} of {}".format(i+1, old_count))

	print("Finished")
