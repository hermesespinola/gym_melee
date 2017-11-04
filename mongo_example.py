from pymongo import MongoClient

# Connect to the cloud MongoDB as 'hermes' user.
client = MongoClient("mongodb://hermes:hermes@ds245615.mlab.com:45615/meleeframes")

# Select the database 'meleeframes'.
db = client['meleeframes']              # or client.meleeframes

# Create or select collection with name: 'test-collection'.
# This creates it if it does not exists.
collection = db['test-collection']      # or db.test-collection

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
#post_id = collection.insert_one(test).inserted_id

# Insert more then one object/document
#post_id = collection.insert_many(test2)

# Iterate over a collection and print it
for docs in collection.find():
    print docs
    print docs["name"]
    print docs["lastname"]


# For referece: http://api.mongodb.com/python/current/tutorial.html