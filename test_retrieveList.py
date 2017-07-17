"""
A test for retrieve_list
"""

from ragdoll import *

mongo = MongoDB(host='47.93.246.201', port=27017, database='eatech', user='harry', password='password')

# selector = {'name': '胡萝卜'}
# selector = {'range': [{'name':'蛋白质', 'value':[25,100]},{'name':'脂肪','value':[0,10]}]}
selector = {'range':[{'abbr' : 'PROCNT', 'value' : 0.49}, {'abbr' : 'CHOCDF', 'value' : [1,2]}]}

data = mongo.retrieve_list(selector)
for doc in data:
    item = mongo.retrieve_item(doc['collection'],doc['_id'])
    print(item)
