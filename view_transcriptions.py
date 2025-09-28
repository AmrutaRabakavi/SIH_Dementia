# view_transcriptions.py
import sqlite3

# Connect to the database
conn = sqlite3.connect("transcribe.db")
cursor = conn.cursor()

# Fetch all rows from the transcriptions table
cursor.execute("SELECT * FROM transcriptions")
rows = cursor.fetchall()

# Print all transcriptions
if len(rows) == 0:
    print("No transcriptions found in the database.")
else:
    print("All saved transcriptions:\n")
    for row in rows:
        print(f"ID: {row[0]}")
        print(f"User ID: {row[1]}")
        print(f"Audio File: {row[2]}")
        print(f"Transcription: {row[3]}")
        print(f"Language: {row[4]}")
        print(f"Created At: {row[5]}")
        print("-" * 40)

# Close the database connection
conn.close()
