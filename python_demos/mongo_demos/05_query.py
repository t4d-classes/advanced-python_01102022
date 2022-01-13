""" find document with mongo """
from contextlib import closing
import pymongo

conn_string = "mongodb://root:dbpass@localhost:27017"

with closing(pymongo.MongoClient(conn_string)) as client:

    db = client["app"]
    col = db["people"]

    people_named_srilakshmi = col.find({ 'firstName': 'Srilakshmi' })

    for person in people_named_srilakshmi:
        print(person)
