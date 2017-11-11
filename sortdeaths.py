from pymongo import MongoClient
import pprint

client = MongoClient('mongodb://hermes:hermes@info.gda.itesm.mx:27017/melee')
db = client['melee']
collection = db['games']

one = collection.find()[0]
print(one['date'])

prev = {'percent': 0}
for i in one['p1']['frame']:
    if i['stock'] != 0:
        # pprint.pprint(prev['percent'])
        pprint.pprint(i['percent'])
        print(i['dead'], i['dead_fall'], i['stock'])
    prev = i

print('=======================================================')

prev = {'percent': 0}
for i in one['p2']['frame']:
    if i['stock'] != 0:
        # pprint.pprint(prev['percent'])
        pprint.pprint(i['percent'])
        print(i['dead'], i['dead_fall'], i['stock'])
    prev = i
