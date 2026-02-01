
import os
import sqlite3
from typing import Optional, Dict
import requests

DB_PATH = 'database/is_data.db'

class AIAssistant:
    """
    AI asistent pre IS-Assistant. Vie odpovedať na otázky pomocou Groq API
    aj vyhľadávať v databáze moduly a funkcionality.
    """
    def __init__(self, api_key_path: str = 'config/groq_api_key.txt'):
        self.api_key = self._load_api_key(api_key_path)

    def _load_api_key(self, path: str) -> Optional[str]:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            print(f"API kľúč nebol nájdený v {path}.")
            return None

    def ask(self, question: str) -> str:
        """
        Pošle otázku na Groq API a vráti odpoveď.
        """
        if not self.api_key:
            return "API kľúč nie je nastavený."
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "openai/gpt-oss-20b",
            "messages": [
                {"role": "user", "content": question}
            ]
        }
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            return f"Chyba pri volaní Groq API: {e}"

    def find_module(self, name: str) -> Optional[Dict]:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM modules WHERE name LIKE ?", (f"%{name}%",))
            row = c.fetchone()
            if row:
                return dict(zip([col[0] for col in c.description], row))
            return None

    def find_functionality(self, name: str) -> Optional[Dict]:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM functionalities WHERE name LIKE ?", (f"%{name}%",))
            row = c.fetchone()
            if row:
                return dict(zip([col[0] for col in c.description], row))
            return None

    def explain_module(self, module_name: str) -> str:
        module = self.find_module(module_name)
        if module:
            return f"Modul: {module['name']}\nPopis: {module['description']}\nVerzia: {module['version']}"
        return "Modul nebol nájdený."

    def explain_functionality(self, func_name: str) -> str:
        func = self.find_functionality(func_name)
        if func:
            return f"Funkcionalita: {func['name']}\nPopis: {func['description']}"
        return "Funkcionalita nebola nájdená."
