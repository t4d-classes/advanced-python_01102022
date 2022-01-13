""" connect to mongo """

import pymongo

conn_string = "mongodb://root:dbpass@localhost:27017"

client = pymongo.MongoClient(conn_string)

print(client)

client.close()