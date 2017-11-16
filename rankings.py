from pymongo import MongoClient

def rank_users():
    client = MongoClient('mongodb://hermes:hermes@info.gda.itesm.mx:27017/melee')
    db = client['melee']
    collection = db['users']
rank_users()
