import json
from ragdoll import *

##### Retrieving the nutritional requirements ###################
print("Retrieving the nutritional requirements")

# Initiate a sample Human object with required parameters

test_human = Human(name='John',
			  gender='male',
			  age=26,
			  height=180,
			  PAL=1.5,
			  AMRD={'PROCNT':0.25,
			  		'FAT':0.25,
			  		'CBH':0.5})

# Obtain the nutritioanl requirements
test_human.get_req()

# Print out the nutritional requirements
print("This is the human object:")
print(test_human)
print("\n")

# Accessing the Nutrients object as below
print("Accessing nutrients object...")
print(test_human.nutrients)
print("\n")

# Then convert nutrients to pd.Series with to_series() method
nut_req = test_human.nutrients.to_series()
print("Nutrients object converted to pd.Series.")
print(nut_req)
print("\n")


#### Retrieving a random set of ingredients from database ###############
print("Retrieving a random set of ingredients from database")

# database connection is already initiated at package-level __init__
print("This is the MongoDB object that performs database operations.")
print(mongo)
print("\n")

# use retrieve_random() method to obtain a given number of random ingredients 
# as documents
print("Retrieving a random set of ingredients.")
doc = mongo.retrieve_random('FM', 3) # FM refers to foodmate database

# Convert to ingredient object with from_doc() method.
ingre1 = Ingredient.from_doc(doc[0])
ingre2 = Ingredient.from_doc(doc[1])
ingre3 = Ingredient.from_doc(doc[2])
print(ingre1)
print(ingre2)
print(ingre3)

#### Search for ingredients with given criteria #####################
print("Search for ingredients with given criteria")
# Note that the search scope (collections) is set at package-level __init__
sel = {'range' : [{'abbr' : 'PROCNT', 'value' : [30, 100]}]}
list_docs = mongo.retrieve_list(sel)
print("Number of docs returned: {}".format(len(list_docs)))
test_doc = list_docs[0]
print("Sample doc: {}".format(test_doc))

#### Retrieving a particular ingredient from database ###############
print("Retrieving a particular ingredient from database")

doc = mongo.retrieve_item(col_name=test_doc['collection'], item_id=test_doc['_id'])
test_ingre = Ingredient.from_doc(doc)
print(test_ingre)


#### Composition with a given list of children ###############
print("Composition with a given list of children.")
list_of_children = [ingre1, ingre2, ingre3]
comp = Composite(name='test_comp',
				 children=list_of_children)
print(comp)

#### Alter the values of children with set_value mathod #################
print("Altering the values of children with set_value() method.")
target_values = [35, 24, 57]
comp_new = comp.set_value(target_values)
comp_new.name = 'test_comp_new'
print(comp_new)

#### Now export the nutritional values of Composite out as sereis #################
print("Now export the nutritional values of Composite as series")
nut_val = comp_new.nutrients.to_series()
print(nut_val)

#### Get percentage ######
print("Now with both nutritional requirements and values as series, the percentage\n"
	  "can be obtained")

# First conform nut_req and nut_val to their intersect keys
common_keys = key_matching(nut_req.index, nut_val.index)
print(common_keys)

# Here the conformaiton is at the Series level, it can also be down at Nutrients
# level with dictionary style indexing or Component level with slice_nutrients method
nut_perc = nut_val[common_keys] / nut_req[common_keys]
print(nut_perc)
