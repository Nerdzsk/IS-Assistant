import sqlite3

conn = sqlite3.connect('database/is_data.db')
c = conn.cursor()

with open('database/schema.sql', 'r', encoding='utf-8') as f:
    c.executescript(f.read())

conn.commit()
conn.close()
print('Databáza bola inicializovaná.')
