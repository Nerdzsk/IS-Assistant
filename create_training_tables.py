import sqlite3

conn = sqlite3.connect('database/is_data.db')
c = conn.cursor()

# Tabuľka pre školenia
c.execute('''
CREATE TABLE IF NOT EXISTS training_cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    module_name TEXT,
    difficulty TEXT DEFAULT 'beginner',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Kroky školenia
c.execute('''
CREATE TABLE IF NOT EXISTS training_steps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER NOT NULL,
    step_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    image_path TEXT,
    branch_id INTEGER,
    is_decision INTEGER DEFAULT 0
)
''')

# Vetvy pre školenia
c.execute('''
CREATE TABLE IF NOT EXISTS training_branches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER NOT NULL,
    parent_step_id INTEGER NOT NULL,
    branch_name TEXT NOT NULL,
    branch_color TEXT DEFAULT '#20c997',
    display_order INTEGER DEFAULT 0
)
''')

# Komplikácie/poznámky pre školenia
c.execute('''
CREATE TABLE IF NOT EXISTS training_complications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    solution TEXT,
    branch_id INTEGER
)
''')

conn.commit()

# Over
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
print('Tabulky:', [t[0] for t in c.fetchall()])

conn.close()
print('HOTOVO - tabulky vytvorene!')
