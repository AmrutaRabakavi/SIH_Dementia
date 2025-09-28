import sqlite3

conn = sqlite3.connect("transcribe.db")
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in database:", tables)

# Print all data from each table
for table in tables:
    print(f"\nData in table '{table[0]}':")
    cursor.execute(f"SELECT * FROM {table[0]}")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

conn.close()
