"""
A test for ragdoll.
"""

from ragdoll import *

mongo = MongoDB(host='47.93.246.201', port=27017, database='eatech', user='harry', password='password')

#------------------------------------------------#

def viaName(str, databaseName, dispName=True):

    '''
    Fuzzy search for name string matching (case insensitive).

    For English fuzzy search, insert string seperated with space. eg: 'Butter salt'
        Generated query: {'name.long': {'$regex': '^(?=.*Butter)(?=.*salt).+', '$options': 'i'}}
    Return: any object whose name contains all keywords in any order.
    Chinese fuzzy search not defined yet.

    TODO: 
    Search suggestions: split sentence into words and compare words with high frequency dictionary, 
        give close words search when original word is not available.

    '''

    if databaseName == 'USDA':
        path = 'name.long'
        regexStr = '^'+''.join(['(?=.*'+word+')' for word in str.split(' ')])+'.+'
    elif databaseName == 'Foodmate' or databaseName == 'DIY':
        path = 'name'
        regexStr = '.*' + str + '.*'
    else:
        raise Exception('Insert a vaild database.')


    def queryGen(str):

        query = {}
        query[path] = {}
        query[path]['$regex'] = str
        query[path]['$options'] = 'i'
        
        return query

    # further output format to be set
    display = {'_id':1}
    if dispName: display['name'] = 1

    query = queryGen(regexStr)
    
    if databaseName == 'USDA':
        cursor = mongo.database.USDA.find(query, display)
    elif databaseName == 'Foodmate':
        cursor = mongo.database.Foodmate.find(query, display)
    elif databaseName == 'DIY':
        cursor = mongo.database.DIY.find(query, display)
    else:
        raise Exception('Insert a vaild database.')        

    return cursor

#------------------------------------------------#

def viaRange(nutrients, databaseName='USDA', dispNutrients=False):
    
    # DIY contains materials not nutrients, not available right now

    '''
    Query example: 
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

def viaTag(reqDict, databaseName):
    '''
    eg: {'type':'乳类', 'name':'奶油'}
    '''
    query = reqDict
    display = {}
    for name, val in reqDict.items():
        display[name] = 1

    if databaseName == 'USDA':
        cursor = mongo.database.USDA.find(query, display)
    elif databaseName == 'Foodmate':
        cursor = mongo.database.Foodmate.find(query, display)
    elif databaseName == 'DIY':
        cursor = mongo.database.DIY.find(query, display)
    else:
        raise Exception('Insert a vaild database.')

    return cursor


#------------------------------------------------#


# test for viaName

'''
str = 'Butter salt'

cur = viaName(str,databaseName='USDA')
for doc in cur:
    print(doc)

'''


# test for viaRange

'''
nutrients = [{'abbr' : 'PROCNT', 'value' : 0.49},
             {'abbr' : 'CHOCDF', 'value' : 2.87}]

cur = viaRange(nutrients)
for doc in cur:
    print(doc)

'''


# test for viaTag

'''
dictionary = {'type':'乳类', 'name': '奶油''}

cur = viaTag(dictionary, databaseName='Foodmate')
for doc in cur:
    print(doc)

'''







