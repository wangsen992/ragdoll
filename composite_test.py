"""
A test for ragdoll.composite
"""

from ragdoll import *

mongo = MongoDB(host='47.93.246.201', port=27017, database='eatech', user='harry', password='password')

meal = mongo.retrieve_item('DIY', "595597b5d4ae8333cc8e257e")
meal2 = mongo.retrieve_item('DIY', "59585f8fd4ae831417e50206")