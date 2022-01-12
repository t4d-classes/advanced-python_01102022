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

        sql = "select closing_date, currency_symbol, " \
              "exchange_rate from rate where id = %s"
    
        params = (1,) # create tuple with one element

        cur.execute(sql, params)

        row = cur.fetchone()

        print(row['exchange_rate'])
