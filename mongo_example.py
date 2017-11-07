from pymongo import MongoClient

"""
from datetime import datetime
now = datetime.now()
# Date of game
col_time = '%s-%s-%s-%s-%s' % (now.year, now.month, now.day, now.hour, now.minute)

# Create collection for each player frames
player1_frames_collection = db['player1' + col_time]
player2_frames_collection = db['player2' + col_time]

# Init fram data list
p1_frames = []
p2_frames = []

# for each player x frames during game:
current_frame = {}
current_frame["x"] = dframe.x
px_frames.append(current_frame)

# at end of the game:
f1 = player1_frames_collection.insert_many(p1_frames)
f2 = player2_frames_collection.insert_many(p2_frames)
"""

# Connect to the cloud MongoDB as 'hermes' user.
client = MongoClient('mongodb://hermes:hermes@info.gda.itesm.mx:27017/melee')
# client = MongoClient("mongodb://hermes:hermes@ds245615.mlab.com:45615/meleeframes")

# Select the database 'meleeframes'.
db = client['melee']              # or client.meleeframes

# Create or select collection with name: 'test-collection'.
# This creates it if it does not exists.
collection = db['test']      # or db.test-collection

# Create an object/document.
test = {
    'name' : 'herumesu',
    'lastname' : 'esupinola'
}

test2 = [
    {
        "name" : "Hermes",
        "lastname" : "Espinola"
    },
    {
        "name" : "Andres",
        "lastname" : "Barro"
    },
    {
        "name" : "Gera",
        "lastname" : "Juarez"
    }
]

# Insert the object/document to the DB.
# Do not know if the variable is necessary.
# '.inserted_id' creates an id for the object.
# post_id = collection.insert_one(test).inserted_id

# Insert more then one object/document
# post_id = collection.insert_many(test2)name"])
    # print(docs["l

# {fecha: {
#     p1:{
#         char:'link',
#         frames:[{}]
#     },
#     p2:{
#         char:¨¨,
#         frames[{}]
#     },
#     winner:'p1'
# },
# fecha2: ...}

# Iterate over a collection and print it
for docs in collection.find():
    print(docs)
    # print(docs["name"])
    # print(docs["lastname"])


# For referece: http://api.mongodb.com/python/current/tutorial.html
