from pymongo import MongoClient
from datetime import datetime
from sys import argv
import pprint
import matplotlib.pyplot as plt
import numpy as np

def makegraphs(name, j):
    client = MongoClient('mongodb://hermes:hermes@info.gda.itesm.mx:27017/melee')
    db = client['melee']
    gamescol = db['games']
    userscol = db['users']

    print('Plotting for' , name, '\b...')

    stocks = sorted(gamescol.find({'name': name}, {'p1.frame': False, 'p2.frame': False}), key = lambda s: s['date'])

    stats = userscol.find_one({'name': name})

    pprint.pprint(stats)

    for k in stocks[0]['stats'].keys():
        plt.figure(j)
        j += 1
        plt.plot([s['stats'][k] for s in stocks.copy()], label = k)
        avgs = [stocks[0]['stats'][k]]
        for i in range(2, len(stocks)):
            avgs.append(avgs[-1] * ((i - 1) / i) + stocks[i]['stats'][k] / i)
        plt.plot(avgs, label = str(k) + ' Average')
        # print(k, 'outliers:')
        # pprint.pprint(stats[k]['outliers'])

        plt.xlabel('Date')
        plt.ylabel('Score')
        plt.title(name)
        plt.grid(True)
        plt.legend()

    return j

j = 1
for i in argv[1:]:
    j = makegraphs(i, j)

plt.show()
