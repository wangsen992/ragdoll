"""
A test for ragdoll.
"""

from ragdoll import *
from bson.son import SON
import pprint

mongo = MongoDB(host='47.93.246.201', port=27017, database='eatech', user='harry', password='password')
# db = mongo.database


def viaName(str, databaseName='DIY'):

    # Fuzzy search for name string matching

    display = {'_id':1}
    if True: display['name'] = 1

    def USDAQueryGen(str):

        query = {}
        query['name.long'] = {}
        query['name.long']['$regex'] = '.*' + str + '.*'

        return query

    

    query = USDAQueryGen(str)
    cursor = mongo.database.USDA.find(query, display)

    return cursor





#------------------------------------------------#


def viaRange(nutrients, dispNutrients=False, databaseName='USDA'):
    
    # DIY contains materials not nutrients, not available right now

    '''
    cur = db.USDA.find({'nutrients': { '$all': [{ '$elemMatch' : {'abbr' : tag1, 'value' : val1}},
                                                { '$elemMatch' : {'abbr' : tag2, 'value' : val2}}
                                                ]}},
                       {'_id' : 1, 'nutrients' : 1})
    '''

    def queryGen(nuts, fuzzySearch=True, fltPct=0.1):
        '''
        Fuzzy search enabled by default for accurate values.
        fltPct: floating value (percentage).
        '''
        query = {}
        query['nutrients'] = {}
        query['nutrients']['$all'] = []

        for nutInfo in nuts:
            new_nutInfo = nutInfo.copy()
            val = new_nutInfo['value']
            
            # range (only support a valid range eg [10, 20] yet)
            if type(val) == list:
                new_nutInfo['value'] = {'$gt':val[0], '$lt':val[1]}
            # single value
            elif type(val) == int or type(val) == float:
                if fuzzySearch:
                    new_nutInfo['value'] = {'$gt':(1-fltPct)*val, '$lt':(1+fltPct)*val}
            else:
                raise Exception('Insert a value or a range to search.')
            
            subdict = {}
            subdict['$elemMatch'] = new_nutInfo
            query['nutrients']['$all'].append(subdict.copy())

        return query
    
    # further output format to be set
    display = {'_id' : 1}
    if dispNutrients: display['nutrients'] = 1

    query = queryGen(nutrients)
    if databaseName == 'USDA':
        cursor = mongo.database.USDA.find(query, display)
    elif databaseName == 'Foodmate':
        cursor = mongo.database.Foodmate.find(query, display)
    elif databaseName == 'DIY':
        raise Exception('DIY not supported yet, please choose a vaild database.')
    else:
        raise Exception('Insert a vaild database.')

    return cursor

#------------------------------------------------#



# test for viaRange

'''

nutrients = [{'abbr' : 'PROCNT', 'value' : 0.49},
             {'abbr' : 'CHOCDF', 'value' : 2.87}]

cur = viaRange(nutrients)
for doc in cur:
    print(doc)


'''


# test for viaName

str = 'Butter'

cur = viaName(str)
for doc in cur:
    print(cur)








