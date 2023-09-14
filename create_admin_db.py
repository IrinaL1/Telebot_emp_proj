import sqlite3 as sql

con = sql.connect('admin.db')
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS `admin` (`db_name` STRING, `password` STRING)")
    con.commit()

cur.execute("SELECT * FROM `admin`")
rows = cur.fetchall()
for row in rows:
    print(row)

con_1 = sql.connect('vse.db')
cur_1 = con_1.cursor()
cur_1.execute("SELECT * FROM `emp_projects`")
rows = cur_1.fetchall()
for row in rows:
    print(row)
