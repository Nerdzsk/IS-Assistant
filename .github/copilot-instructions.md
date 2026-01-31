# GitHub Copilot Instructions for IS-Assistant

## Project Overview
You are working on **IS-Assistant**, an AI-powered tool for Information System management with local database storage.

## Core Technologies
- **Language:** Python 3.9+
- **Database:** SQLite (local storage)
- **AI Integration:** OpenAI API or Local LLM
- **Data Formats:** JSON, CSV, XML

## Project Structure
Always maintain this structure:
```
IS-Assistant/
├── database/              # Database files and schemas
├── modules/               # Core Python modules
├── training/              # Training materials
├── config/                # Configuration files
├── docs/                  # Documentation
└── main.py                # Entry point
```

## Coding Standards

### 1. Python Style
- Follow PEP 8 conventions
- Use type hints for all functions
- Write docstrings for all classes and functions
- Use meaningful variable names in Slovak or English

### 2. Database Operations
- Always use parameterized queries (prevent SQL injection)
- Handle database connections in context managers
- Create separate functions for CRUD operations
- Example:
```python
def get_specification(spec_id: int) -> dict:
    """Retrieve IS specification by ID."""
    with sqlite3.connect('database/is_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM specifications WHERE id = ?",
            (spec_id,)
        )
        return cursor.fetchone()
```

### 3. AI Integration
- Keep AI prompts in separate template files
- Use environment variables for API keys
- Implement error handling for API failures
- Cache AI responses when possible

### 4. File Organization
- One class per file
- Group related functions in modules
- Keep configuration separate from code

## Specific Guidelines

### When Creating Database Code:
1. Always create schema first in `database/schema.sql`
2. Use migrations for schema changes
3. Add indexes for frequently queried fields
4. Include created_at and updated_at timestamps

### When Creating Training Modules:
1. Store templates in `training/templates/`
2. Make content modular and reusable
3. Include progress tracking
4. Support multiple user levels (beginner, intermediate, advanced)

### When Creating Customer Management:
1. Separate customer data from specifications
2. Include HW specifications as JSON fields
3. Track all interactions and changes
4. Support export to multiple formats

## Code Examples

### Database Connection
```python
import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    """Context manager for database connections."""
    conn = sqlite3.connect('database/is_data.db')
    conn.row_factory = sqlite3.Row  # Return rows as dicts
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
```

### Specification Class
```python
from dataclasses import dataclass
from typing import List, Dict
import json

@dataclass
class ISSpecification:
    """Represents an Information System specification."""
    id: int = None
    name: str = ""
    version: str = "1.0"
    modules: List[Dict] = None
    
    def __post_init__(self):
        if self.modules is None:
            self.modules = []
    
    def add_module(self, name: str, description: str):
        """Add a module to the specification."""
        self.modules.append({
            "name": name,
            "description": description
        })
    
    def save(self):
        """Save specification to database."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO specifications (name, version, modules)
                   VALUES (?, ?, ?)""",
                (self.name, self.version, json.dumps(self.modules))
            )
            self.id = cursor.lastrowid
```

## Important Reminders

### Always:
- ✅ Use type hints
- ✅ Write docstrings
- ✅ Handle errors gracefully
- ✅ Use context managers for resources
- ✅ Follow the project structure
- ✅ Keep database operations separate
- ✅ Store sensitive data in environment variables
- ✅ Write tests for critical functions

### Never:
- ❌ Hardcode API keys or passwords
- ❌ Use string concatenation for SQL queries
- ❌ Create files outside the project structure
- ❌ Mix business logic with database code
- ❌ Ignore error handling

## Testing Guidelines

### Unit Tests
- Create tests in `tests/` directory
- Test each module independently
- Use pytest framework
- Mock external dependencies (AI API, etc.)

### Example Test
```python
import pytest
from modules.specifications import ISSpecification

def test_specification_creation():
    """Test creating a new specification."""
    spec = ISSpecification(name="Test IS", version="1.0")
    spec.add_module("Users", "User management")
    
    assert spec.name == "Test IS"
    assert len(spec.modules) == 1
    assert spec.modules[0]["name"] == "Users"
```

## Slovak Language Support

### UI Messages
- Keep all user-facing messages in Slovak
- Store strings in `config/messages_sk.json`
- Support easy translation to other languages

### Example
```python
import json

class Messages:
    def __init__(self, lang="sk"):
        with open(f'config/messages_{lang}.json', 'r', encoding='utf-8') as f:
            self.messages = json.load(f)
    
    def get(self, key: str) -> str:
        return self.messages.get(key, key)

msg = Messages()
print(msg.get("welcome"))  # "Vítajte v IS-Assistant!"
```

## When User Asks for Help

If the user asks you to:
- **Create structure**: Generate all folders and __init__.py files
- **Create database**: Generate schema.sql with all tables
- **Create module**: Follow the class template above
- **Add feature**: Ask what functionality they need
- **Fix error**: Request the full error message and relevant code

## Priority Order
1. Security (SQL injection, API keys)
2. Code quality (type hints, docstrings)
3. Project structure (correct folders)
4. Error handling
5. Performance

---

**Remember:** This is a project for a beginner developer. Be helpful, explain your suggestions, and write clean, well-documented code.
