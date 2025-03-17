import sqlite3

# Create a connection to the database (this will create the database file if it doesn't exist)
conn = sqlite3.connect('aiaa.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create a user table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()