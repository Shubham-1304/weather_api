import sqlite3
connection=sqlite3.connect('data.db')
cursor=connection.cursor()

create_table="CREATE TABLE IF NOT EXISTS cities(id INTEGER PRIMARY KEY,city text)"
cursor.execute(create_table)
connection.commit()
connection.close()
