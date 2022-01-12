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

        sql = "insert into rate (closing_date, currency_symbol, " \
              "exchange_rate) values (%s, %s, %s)"
    
        params = [
            ('2019-01-04','EUR', 0.87),
            ('2019-01-05','EUR', 0.86),
            ('2019-01-06','EUR', 0.88),
        ]

        cur.execute(sql, params[0])
        # cur.executemany(sql, params)

        db.commit()

