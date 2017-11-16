#!/usr/bin/python3
from pymongo import MongoClient
from datetime import datetime
from reglas import Frame_rewards
from sys import argv

def check(one):
    return Frame_rewards(one)

def outs(avg, stddev, k, games):
    stds = 2
    low = []
    high = []
    for g in games:
        if g['stats'][k] > avg + stds * stddev:
            print('High:', g['stats'][k])
            high.append(g['_id'])
        elif g['stats'][k] < avg - stds * stddev:
            print('Low:', g['stats'][k])
            low.append(g['_id'])
    return {'high': high, 'low': low}

def userstat(name):
    print('Calculating for', name)
    client = MongoClient('mongodb://hermes:hermes@info.gda.itesm.mx:27017/melee')
    db = client['melee']
    collection = db['games']
    dest = db['users']
    stocks = list(collection.find({'name': name}))
    # n = stocks.count()
    n = len(stocks)
    if(n == 1):
        return
    stats = []
    for s in stocks:
        s['stats'] = check(s)
        collection.update_one({'_id': s['_id']}, {"$set": {
            'stats': s['stats']
        }}, upsert=True)
        stats.append(s['stats'])
    # stocks.rewind()
    avg = {}
    stddev = {}
    outliers = {}

    for k in stats[0].keys():
        avg[k] = stats[0][k]
    for s in stats[1:]:
        for k in s.keys():
            avg[k] += s[k]
    for k in avg.keys():
        avg[k] /= n

    for k in stats[0].keys():
        stddev[k] = (stats[0][k] - avg[k]) ** 2
    for s in stats[1:]:
        for k in s.keys():
            stddev[k] += (s[k] - avg[k]) ** 2
    for k in stddev.keys():
        stddev[k] = (stddev[k] / (n - 1)) ** (1/2)

    for k in avg.keys():
        print(k, '-> Average:', avg[k], 'Standard Deviation:', stddev[k])
        outliers[k] = outs(avg[k], stddev[k], k, stocks)
        # stocks.rewind()

    fullstats = {
        'name': name,
        'date': datetime.now(),
        'stock_count': n
    }
    for k in avg.keys():
        fullstats[k] = {
            'avg': avg[k],
            'stddev': stddev[k],
            'outliers': outliers[k]
        }

    dest.replace_one({'name': name}, fullstats, True)

for name in argv[1:]:
    userstat(name)
