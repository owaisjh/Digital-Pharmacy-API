import sqlite3
import csv

connection = sqlite3.connect('meds.db')

cursor = connection.cursor()

count=1
with open("list.csv","rt") as f:
    data = csv.reader(f)
    for row in data:
        if row[3]==" ":
            break
        else:
            print(count)
            count= count+1
            query = "INSERT INTO allmeds VALUES (?, ?, ?, ?)"
            cursor.execute(query, (row[3], "temp", row[2], 500))
            create_table = "CREATE TABLE IF NOT EXISTS " + "temp" + " (medname text, cost int, quantity int)"
            cursor.execute(create_table)

            query = "INSERT INTO " + "temp" + " VALUES (?, ?, ?)"
            cursor.execute(query, (row[3], row[2], 500))







connection.commit()
connection.close()