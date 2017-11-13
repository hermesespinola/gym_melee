from pymongo import MongoClient
from datetime import datetime
from sys import argv
import pprint
import matplotlib.pyplot as plt
import numpy as np

client = MongoClient('mongodb://hermes:hermes@info.gda.itesm.mx:27017/melee')
db = client['melee']
gamescol = db['games']
userscol = db['users']

name = argv[1]
print('Plotting for' , name, '\b...')

stocks = sorted(gamescol.find({'name': name}, {'p1.frame': False, 'p2.frame': False}), key = lambda s: s['date'])
stats = userscol.find({'name': name})

pprint.pprint(stats)

for k in stocks[0]['stats'].keys():
    plt.plot([s['stats'][k] for s in stocks], label = k)
    print(k, 'outliers:')
    pprint.pprint(stats[k]['outliers'])

plt.xlabel('Date')
plt.ylabel('Score')
plt.title(name)
plt.grid(True)
plt.legend()
plt.show()
