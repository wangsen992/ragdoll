"""
A test for ragdoll.
"""

from pymongo import MongoClient
import ragdoll as rd

client = MongoClient()
col = client['mydatabase'].mycollection

usda_adapter = rd.UsdaAdapter(col, dict_file="ragdoll/NUTR_DEF_CUS.txt")
cheese = usda_adapter.retrieve_item("594504ec329fb04d99aad8df")
cereal = usda_adapter.retrieve_item("594504f3329fb04d99aae769")

cheese.display_macro()
cereal.display_macro()

meal = (cheese + cereal).convert2meal(name='test_meal')
meal.display_macro()