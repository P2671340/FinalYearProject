import sqlite3
from werkzeug.security import generate_password_hash

# Connect to the database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Find users with scrypt passwords
cursor.execute("SELECT id, username, password FROM users WHERE password LIKE 'scrypt:%'")
users = cursor.fetchall()

# Loop through and update each user's password
for user in users:
    user_id = user[0]
    username = user[1]
    
    print(f"Resetting password for user: {username}")

    # Prompt for new password (REMOVE THIS IF YOU HAVE PLAIN PASSWORDS STORED)
    new_password = input(f"Enter new password for {username}: ")

    # Rehash the password using pbkdf2:sha256
    new_hashed_password = generate_password_hash(new_password)

    # Update database
    cursor.execute("UPDATE users SET password = ? WHERE id = ?", (new_hashed_password, user_id))

# Save changes
conn.commit()
conn.close()

print("Password migration complete!")
