import mysql.connector
from contextlib import closing

with closing(mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="sql!DB123!"
)) as mydb:

    print(mydb)

    print(mydb.is_connected())

print(mydb.is_connected())
