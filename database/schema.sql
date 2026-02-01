
-- Tabuľka: Moduly
CREATE TABLE IF NOT EXISTS modules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    version TEXT DEFAULT '1.0',
    parent_module_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_module_id) REFERENCES modules(id)
);

-- Tabuľka: Funkcionality
CREATE TABLE IF NOT EXISTS functionalities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    code_example TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE
);

-- Tabuľka: Nastavenia
CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_id INTEGER NOT NULL,
    setting_key TEXT NOT NULL,
    setting_value TEXT,
    description TEXT,
    FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE,
    UNIQUE(module_id, setting_key)
);

-- Tabuľka: Vzťahy medzi modulmi
CREATE TABLE IF NOT EXISTS module_relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_from_id INTEGER NOT NULL,
    module_to_id INTEGER NOT NULL,
    relationship_type TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY (module_from_id) REFERENCES modules(id) ON DELETE CASCADE,
    FOREIGN KEY (module_to_id) REFERENCES modules(id) ON DELETE CASCADE
);
