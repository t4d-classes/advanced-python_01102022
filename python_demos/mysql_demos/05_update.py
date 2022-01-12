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

        sql = "update rate set exchange_rate = %s where id = %s"
    
        cur.execute(sql, (2, 1) )

        db.commit()

