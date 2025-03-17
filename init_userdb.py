import sqlite3

conn = sqlite3.connect('userdb.db')

with open('schema.sql') as file:
    conn.executescript(file.read())

cur = conn.cursor()

cur.execute("INSERT INTO users (username, password) VALUES (?,?)", ('Reed', '123'))
cur.execute("INSERT INTO users (username, password) VALUES (?,?)", ('David', '1234'))
cur.execute("INSERT INTO users (username, password) VALUES (?,?)", ('Darshan', '1235'))
cur.execute("INSERT INTO users (username, password) VALUES (?,?)", ('Lowen', '123'))

conn.commit()
conn.close()