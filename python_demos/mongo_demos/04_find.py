""" find document with mongo """
from contextlib import closing
import pymongo

conn_string = "mongodb://root:dbpass@localhost:27017"

with closing(pymongo.MongoClient(conn_string)) as client:

    db = client["app"]
    col = db["people"]

    # person = col.find_one()
    # print(person)

    people = col.find()

    for person in people:
        print(person)
