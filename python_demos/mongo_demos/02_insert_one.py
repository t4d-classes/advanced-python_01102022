""" connect to mongo """

import pymongo

conn_string = "mongodb://root:dbpass@localhost:27017"

client = pymongo.MongoClient(conn_string)

db = client["app"]
col = db["people"]

col.insert_one({
    "firstName": "Bob",
    "lastName": "Smith",
    "address": {
        "street": "123 Oak Lane",
        "city": "Palo Alto",
        "state": "CA",
        "zipCode": "12345"
    }
})


client.close()