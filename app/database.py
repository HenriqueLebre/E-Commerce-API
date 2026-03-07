import sqlite3

try:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT sqlite_version()")
    version = cursor.fetchone()
    print(f"SQLite version: {version[0]}")

except sqlite3.Error as e:

    print(f"Error occurred: {e}")

finally:
    if conn:
        conn.close()
        print("Database connection closed.")