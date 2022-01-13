""" connect to mongo """

import pymongo

conn_string = "mongodb://root:dbpass@localhost:27017"

client = pymongo.MongoClient(conn_string)

db = client["app"]
col = db["people"]

people = [
    {
        "firstName": "Sally",
        "lastName": "Thomas",
        "address": {
            "street": "1 Infinity Way",
            "city": "Cupertino",
            "state": "CA",
            "zipCode": "12345"
        }
    },
    {
        "firstName": "Srilakshmi",
        "lastName": "Movva",
        "address": {
            "street": "123 San Antonio Ave",
            "city": "Mountain View",
            "state": "CA",
            "zipCode": "12345"
        }
    }    
]

result = col.insert_many(people)

print(result.inserted_ids)


client.close()