import pymongo
import json

# create connecttion with database
# Note: to connect to your own db, change the url and port number
# Also change the authenticate
client = pymongo.MongoClient('mongodb://ds121163.mlab.com',21163)
# Get the database
jasondb = client['jasondb']
# Set authentication
jasondb.authenticate('admin','admin123')
# Get collection, if no named collection then create one
companies = jasondb.companies

# name of the output file

OUTPUT_FILE_NAME = 'output.json'

# following code is to load json file to mongodb

# file = open('companies.json',encoding='utf8')
# maxNum = 100
# currentNum = 0
# for line in file:
#     if currentNum >= maxNum:
#         break
#     print(line)
#     data = json.loads(line.replace("$",""))
#     print(data)
#     companies.insert_one(data)
#     currentNum += 1
# file.close()

# define a rscheme
rscheme = {}

# a function to create rscheme
# it require a document and a path to this document
# typ of the document should be dict
def createRschema (document, path):
    # get keys
    for key in document:
        # check if the path is root or not
        # if not, add .
        if path == "":
            currentPath = key
        else:
            # for this collections ONLY
            # In this collections it has a list as a key
            if(isinstance(key, list)):
                currentPath = path + "." + covertListToString(key)
            else:
                currentPath = path + "." + key
        # add to dict
        rscheme[currentPath] = type(document.get(key)).__name__
        # recursion call
        if isinstance(document.get(key), list):
            for element in document.get(key):
                if isinstance(element, list):
                    break
                else:
                    createRschema(element, currentPath)
        elif isinstance(document.get(key),dict):
            createRschema(document.get(key),currentPath)


# A helper function to convert list to string
def covertListToString (lst):
    str = '['
    for i in lst:
        str+' , '
    str+']'
    return str

# get document in the collection and parse them
for document in companies.find({}):
    createRschema(document, "")

# output to a file
with open(OUTPUT_FILE_NAME,'w') as output:
     json.dump(rscheme, output, sort_keys=TabError, indent= 4)

print(rscheme)