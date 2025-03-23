import sqlite3

# Connect to the database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Check the first 5 stored passwords
cursor.execute("SELECT id, username, password FROM users LIMIT 5;")
users = cursor.fetchall()

# Print stored password hashes
for user in users:
    print(f"ID: {user[0]}, Username: {user[1]}, Password Hash: {user[2]}")

conn.close()