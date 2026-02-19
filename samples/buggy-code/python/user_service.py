# user_service.py - Sample code with intentional bugs for practice
# Use this file to practice code review and debugging with GitHub Copilot CLI
#
# Try these commands:
#   copilot --allow-all -p "Review @samples/buggy-code/python/user_service.py for security issues"
#   copilot --allow-all -p "Find all bugs in @samples/buggy-code/python/user_service.py"

import sqlite3
import hashlib

# BUG 1: SQL Injection
# The user_id is directly interpolated into the query string
def get_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    return cursor.fetchone()


# BUG 2: Race Condition
# Multiple requests can trigger parallel database calls before cache is set
user_cache = {}

def get_cached_user(user_id):
    if user_id not in user_cache:
        user_cache[user_id] = get_user(user_id)
    return user_cache[user_id]


# BUG 3: SQL Injection + No Error Handling
# String interpolation in SQL and no try/except
def update_user(user_id, data):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"UPDATE users SET name = '{data['name']}' WHERE id = {user_id}")
    conn.commit()
    return get_user(user_id)


# BUG 4: Sensitive Data in Logs
# Password is logged in plain text
def login(email, password):
    print(f"Login attempt: {email} / {password}")
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
    user = cursor.fetchone()
    if user and user['password'] == password:
        return {"success": True, "user": user}
    return {"success": False}


# BUG 5: Weak Password Comparison
# Using == for password comparison (timing attack vulnerable) and plain text passwords
def verify_password(input_password, stored_password):
    return input_password == stored_password


# BUG 6: No Input Validation
# Directly using user input without any validation
def create_user(user_data):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"INSERT INTO users (name, email, password) VALUES ('{user_data['name']}', '{user_data['email']}', '{user_data['password']}')"
    cursor.execute(query)
    conn.commit()


# BUG 7: Hardcoded Secret
# JWT secret should be in environment variables
JWT_SECRET = "super-secret-key-12345"

def generate_token(user_id):
    import jwt
    return jwt.encode({"user_id": user_id}, JWT_SECRET, algorithm="HS256")


# BUG 8: Missing Authentication Check
# This function should verify the user is authorized to delete
def delete_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM users WHERE id = {user_id}")
    conn.commit()


# BUG 9: Weak Hashing (Python-specific)
# MD5 is cryptographically broken for password hashing
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


# BUG 10: Pickle Deserialization (Python-specific)
# Deserializing untrusted data with pickle is dangerous
import pickle
import base64

def load_user_preferences(encoded_data):
    decoded = base64.b64decode(encoded_data)
    return pickle.loads(decoded)  # Remote code execution vulnerability!
