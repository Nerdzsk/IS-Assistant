# IS-Assistant - Detailná špecifikácia

## 🎯 Hlavný cieľ aplikácie

**IS-Assistant** je inteligentný systém pre správu znalostí o informačnom systéme (IS). Umožňuje vytvárať, organizovať a prehľadávať informácie o moduloch, podmoduloch a ich funkcionálitach pomocou AI poradcu.

---

## 📋 Funkčný popis - Fáza 1: AI Poradca

### Hlavné komponenty:

#### 1. **Knowledge Base (Lokálna databáza)**
- Ukladanie štruktúry modulov a podmodulov
- Opis funkčných vzťahov medzi modulmi
- Detailné informácie o nastaveniach
- História zmien a verzií

#### 2. **AI Poradca**
- Prehľadávanie všetkých dát v databáze
- Inteligentne odpovedie na otázky užívateľa
- Kontextové vysvetľovanie vzťahov medzi modulmi
- Poskytovanie príkladov použitia

#### 3. **Užívateľské rozhranie**
- Pekné, intuitívne prostredie
- Chatové rozhranie pre otázky
- Vizualizácia vzťahov medzi modulmi
- Príklady a nápovedá

---

## 🛠️ Štruktúra dát

### Hierarchia:
```
Informačný Systém
├── Modul 1
│   ├── Podmodul 1.1
│   │   ├── Funkcionalita A
│   │   └── Funkcionalita B
│   └── Podmodul 1.2
│       └── Funkcionalita C
├── Modul 2
│   └── Podmodul 2.1
│       ├── Funkcionalita D
│       └── Funkcionalita E
└── Vzťahy
    ├── Modul 1 ↔ Modul 2 (cez Funkcionalitu X)
    └── Podmodul 1.1 ↔ Podmodul 2.1 (zdielajú dáta)
```

### Databázová štruktúra:

```sql
-- Tabuľka: Moduly
CREATE TABLE modules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    version TEXT DEFAULT '1.0',
    parent_module_id INTEGER,  -- NULL pre hlavné moduly
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_module_id) REFERENCES modules(id)
);

-- Tabuľka: Funkcionality
CREATE TABLE functionalities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    code_example TEXT,  -- Príklady kódu/konfigurácie
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE
);

-- Tabuľka: Nastavenia
CREATE TABLE settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_id INTEGER NOT NULL,
    setting_key TEXT NOT NULL,
    setting_value TEXT,
    description TEXT,
    FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE,
    UNIQUE(module_id, setting_key)
);

-- Tabuľka: Vzťahy medzi modulmi
CREATE TABLE module_relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_from_id INTEGER NOT NULL,
    module_to_id INTEGER NOT NULL,
    relationship_type TEXT NOT NULL,  -- 'depends_on', 'shares_data', 'calls', etc.
    description TEXT,
    FOREIGN KEY (module_from_id) REFERENCES modules(id) ON DELETE CASCADE,
    FOREIGN KEY (module_to_id) REFERENCES modules(id) ON DELETE CASCADE
);

-- Tabuľka: História konverzacií s AI
CREATE TABLE ai_conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_question TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    context_modules TEXT,  -- JSON zoznam relevantných modulov
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==============================================
-- SERVIS - Technické prípadové štúdie
-- ==============================================

-- Tabuľka: Servisné prípady (case studies)
CREATE TABLE service_cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabuľka: Kroky v servisnom prípade
CREATE TABLE service_steps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER NOT NULL,
    step_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    image_path TEXT,          -- Cesta k obrázku
    branch_id INTEGER,        -- NULL = hlavná vetva, inak ID vetvy
    is_decision INTEGER DEFAULT 0,  -- 1 = rozhodovací bod
    FOREIGN KEY (case_id) REFERENCES service_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (branch_id) REFERENCES service_branches(id) ON DELETE CASCADE
);

-- Tabuľka: Vetvy (pre rozhodnutia)
CREATE TABLE service_branches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER NOT NULL,
    parent_step_id INTEGER NOT NULL,  -- ID rozhodovacieho kroku
    branch_name TEXT NOT NULL,        -- Napr. "Áno", "Nie"
    branch_color TEXT DEFAULT '#6c757d',  -- Farba vetvy
    display_order INTEGER DEFAULT 0,
    FOREIGN KEY (case_id) REFERENCES service_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_step_id) REFERENCES service_steps(id) ON DELETE CASCADE
);

-- Tabuľka: Komplikácie
CREATE TABLE service_complications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    solution TEXT,
    branch_id INTEGER,  -- NULL = všeobecná, inak pre konkrétnu vetvu
    FOREIGN KEY (case_id) REFERENCES service_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (branch_id) REFERENCES service_branches(id) ON DELETE CASCADE
);
```

---

## 🖥️ Užívateľské rozhranie

### Hlavná obrazovka:

```
╭──────────────────────────────────────────╮
│    IS-Assistant - AI Poradca pre IS     │
╰──────────────────────────────────────────╯

╭──────────────╮  ╭────────────────────────╮
│ 📚 Moduly   │  │  🤖 AI Chat          │
├──────────────┤  ├────────────────────────┤
│ ▶ Užívatelia │  │                      │
│ ▼ Produkty   │  │ Ty: Ako funguje      │
│   ▸ Sklad    │  │     modul Produkty?  │
│   ▸ Ceny     │  │                      │
│ ▶ Faktury    │  │ AI: Modul Produkty   │
│               │  │     spravuje sklad│
│               │  │     produkty,
