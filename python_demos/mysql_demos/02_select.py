import mysql.connector
from contextlib import closing

with closing(mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="sql!DB123!",
    database="app"
)) as db:

    with closing(db.cursor(dictionary=True)) as cur:

        cur.execute(
            "select closing_date, currency_symbol, exchange_rate from rate")

        res = cur.fetchall()

        for row in res:
            print(row['exchange_rate'])
