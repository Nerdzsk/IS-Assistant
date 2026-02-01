
import sqlite3
from typing import Optional, List, Dict

DB_PATH = 'database/is_data.db'

class Module:
    """
    Trieda reprezentuje modul IS.
    """
    def __init__(self, name: str, description: str = '', version: str = '1.0', parent_module_id: Optional[int] = None):
        self.name = name
        self.description = description
        self.version = version
        self.parent_module_id = parent_module_id

    def save(self) -> int:
        """Uloží modul do databázy a vráti jeho ID."""
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute(
                """
                INSERT INTO modules (name, description, version, parent_module_id)
                VALUES (?, ?, ?, ?)
                """,
                (self.name, self.description, self.version, self.parent_module_id)
            )
            conn.commit()
            return c.lastrowid

    @staticmethod
    def get_by_id(module_id: int) -> Optional[Dict]:
        """Vráti modul podľa ID."""
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM modules WHERE id = ?", (module_id,))
            row = c.fetchone()
            if row:
                return dict(zip([col[0] for col in c.description], row))
            return None

    @staticmethod
    def get_all() -> List[Dict]:
        """Vráti všetky moduly."""
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM modules")
            rows = c.fetchall()
            return [dict(zip([col[0] for col in c.description], row)) for row in rows]

    @staticmethod
    def update(module_id: int, name: str, description: str, version: str, parent_module_id: Optional[int]) -> None:
        """Aktualizuje modul podľa ID."""
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute(
                """
                UPDATE modules SET name=?, description=?, version=?, parent_module_id=?, updated_at=CURRENT_TIMESTAMP WHERE id=?
                """,
                (name, description, version, parent_module_id, module_id)
            )
            conn.commit()

    @staticmethod
    def delete(module_id: int) -> None:
        """Vymaže modul podľa ID."""
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM modules WHERE id = ?", (module_id,))
            conn.commit()


class Functionality:
    """
    Trieda reprezentuje funkcionalitu modulu.
    """
    def __init__(self, module_id: int, name: str, description: str = '', code_example: str = ''):
        self.module_id = module_id
        self.name = name
        self.description = description
        self.code_example = code_example

    def save(self) -> int:
        """Uloží funkcionalitu do databázy a vráti jej ID."""
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute(
                """
                INSERT INTO functionalities (module_id, name, description, code_example)
                VALUES (?, ?, ?, ?)
                """,
                (self.module_id, self.name, self.description, self.code_example)
            )
            conn.commit()
            return c.lastrowid

    @staticmethod
    def get_by_id(func_id: int) -> Optional[Dict]:
        """Vráti funkcionalitu podľa ID."""
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM functionalities WHERE id = ?", (func_id,))
            row = c.fetchone()
            if row:
                return dict(zip([col[0] for col in c.description], row))
            return None

    @staticmethod
    def get_all() -> List[Dict]:
        """Vráti všetky funkcionality."""
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM functionalities")
            rows = c.fetchall()
            return [dict(zip([col[0] for col in c.description], row)) for row in rows]

    @staticmethod
    def update(func_id: int, name: str, description: str, code_example: str) -> None:
        """Aktualizuje funkcionalitu podľa ID."""
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute(
                """
                UPDATE functionalities SET name=?, description=?, code_example=? WHERE id=?
                """,
                (name, description, code_example, func_id)
            )
            conn.commit()

    @staticmethod
    def delete(func_id: int) -> None:
        """Vymaže funkcionalitu podľa ID."""
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM functionalities WHERE id = ?", (func_id,))
            conn.commit()
