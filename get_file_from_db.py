import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM uploaded_files')
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()