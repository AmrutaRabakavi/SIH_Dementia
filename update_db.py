import sqlite3

DB_NAME = "transcribe.db"

# Connect to the database
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Add dementia_score column if it doesn't exist
try:
    cursor.execute("ALTER TABLE transcriptions ADD COLUMN dementia_score REAL")
    print("Added column: dementia_score")
except sqlite3.OperationalError:
    print("Column 'dementia_score' already exists")

# Add risk_label column if it doesn't exist
try:
    cursor.execute("ALTER TABLE transcriptions ADD COLUMN risk_label TEXT")
    print("Added column: risk_label")
except sqlite3.OperationalError:
    print("Column 'risk_label' already exists")

# Commit changes and close
conn.commit()
conn.close()
print("Database update complete!")
