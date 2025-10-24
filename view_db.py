import sqlite3
from tabulate import tabulate

import os
db_path = os.path.join(os.path.dirname(__file__), "app.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT name, encrypted_message, key FROM messages;")
rows = cursor.fetchall()

print(tabulate(rows, headers=["Name", "Encrypted", "Key"], tablefmt="grid"))
conn.close()
