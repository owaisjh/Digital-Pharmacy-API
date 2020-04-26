import sqlite3

connection = sqlite3.connect('meds.db')

cursor = connection.cursor()

#create_table = "CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, username text, user_name text, items text, cost int, address text, contact int, paymenttype text, status int, daterec date, datecomp date) "

#create_table = "ALTER TABLE allmeds ADD PRIMARY KEY (id) "

create_table = "DELETE FROM allmeds WHERE category='temp' "


#create_table = "CREATE TABLE orders (id INTEGER PRIMARY KEY, username text, user_name text, items text, cost int, address text, contact int, paymenttype text, status int, daterec date, datecomp date)"

cursor.execute(create_table)


connection.commit()

connection.close()