# IS-Assistant
AI-powered assistant for Information System management. Local database-driven tool for IS specifications, personalized training modules, customer onboarding with HW specifications, and intelligent guidance.

## 🎯 Cieľ projektu

Vytvoriť inteligentného asistenta pre správu a prácu s informačnými systémami (IS), ktorý pomôže používateľom:
- Ukladať a spravovať špecifikácie IS v lokálnych súboroch
- Poskytovať personalizované školenia pomocou AI
- Spravovať zákazníkov a ich HW špecifikácie
- Poskytovať inteligentné návody a podporu

## 🆕 Aktuálny stav (Február 2026)

### ✅ Implementované funkcie:
- **Web aplikácia** - Flask server s moderným UI
- **Správa zákazníkov** - pridávanie, editácia, zobrazenie zákazníkov
- **AI Chat** - integrácia s Groq API (Llama model)
- **Wiki** - dokumentácia a návody
- **Hlasové nahrávanie** - Web Speech API pre prevod reči na text
- **AI parsovanie** - automatické rozpoznanie údajov zo súhrnu (firmy, pobočky, kontakty)
- **Google Maps integrácia** - zobrazenie adries pobočiek na mape
- **Formulár nového zákazníka** - s hlasovým vstupom a AI asistenciou

### 🚀 Spustenie aplikácie

```bash
# 1. Aktivuj virtuálne prostredie
.venv\Scripts\activate

# 2. Spusti aplikáciu
python webapp.py

# 3. Otvor v prehliadači
http://localhost:5000
```

### 📱 Dostupné stránky:
- `/` - Hlavná stránka (dashboard)
- `/new-customer` - Pridanie nového zákazníka
- `/customers` - Zoznam zákazníkov
- `/ai-chat` - AI asistent (chat)
- `/wiki` - Wiki dokumentácia

## 📋 Hlavné funkcionality

### 1. Správa špecifikácií IS
- Ukladanie funkčných modelov informačného systému
- Popis modulov a procesov
- História zmien a verziovanie
- Export/import špecifikácií

### 2. AI-podporované školenia
- Personalizované školiace moduly podľa užívateľskej úrovne
- Interaktívne tutoriály pre jednotlivé časti IS
- Virtuálny asistent na otázky a odpovede
- Sledovanie pokroku v školení

### 3. Správa zákazníkov
- Evidencia zákazníkov
- HW špecifikácie a požiadavky
- Nastavenia a konfigurácie
- História komunikácie a riešení

### 4. Lokálna databáza
- SQLite databáza pre offline prácu
- Rýchly prístup k informáciám
- Zálohovanie a obnova dát
- Import z rôznych formátov (JSON, CSV, XML)

## 🏗️ Štruktúra projektu

```
IS-Assistant/
├── database/              # Lokálna databáza a skripty
│   ├── schema.sql         # SQL schéma databázy
│   ├── is_data.db         # Hlavná databáza
│   └── migrations/        # Migračné skripty
│
├── modules/               # Hlavné moduly programu
│   ├── specifications.py  # Správa špecifikácií IS
│   ├── training.py        # AI školenia
│   ├── customers.py       # Správa zákazníkov
│   └── ai_assistant.py    # AI integrácia
│
├── training/              # Školiace materiály
│   ├── templates/         # Šablóny školení
│   └── content/           # Obsah kurzov
│
├── config/                # Konfiguračné súbory
│   ├── settings.json      # Základné nastavenia
│   └── ai_config.json     # AI konfigurácia
│
├── docs/                  # Dokumentácia
│   ├── user_guide.md      # Používateľská príručka
│   └── api_docs.md        # API dokumentácia
│
├── main.py                # Hlavný program
├── requirements.txt       # Python závislosti
├── .gitignore
├── LICENSE
└── README.md
```

## 🚀 Začíname - Krok za krokom

### 1. Naklonuj repozitár
```bash
git clone https://github.com/Nerdzsk/IS-Assistant.git
cd IS-Assistant
```

### 2. Nainštaluj závislosti
```bash
pip install -r requirements.txt
```

### 3. Inicializuj databázu
```bash
python database/init_db.py
```

### 4. Spusti program
```bash
python main.py
```

## 📚 Technológie

- **Python 3.9+** - Hlavný programovací jazyk
- **SQLite** - Lokálna databáza
- **OpenAI API / Local LLM** - AI integrácia
- **JSON** - Formát pre špecifikácie

## 🛠️ Vývojové plány (Roadmap)

### Fáza 1: Základná infrastruktúra (Aktuálne)
- [x] Vytvorenie GitHub repozitára
- [x] Základná dokumentácia
- [ ] Vytvorenie priecinkovej štruktúry
- [ ] Implementácia lokálnej databázy (SQLite)
- [ ] Základné CRUD operácie pre špecifikácie

### Fáza 2: AI Integrácia
- [ ] Prepájanie s AI API
- [ ] Základný chatbot
- [ ] Generóvanie školícich materiálov
- [ ] Personalizované odpovede podľa kontextu IS

### Fáza 3: Školenia a Training
- [ ] Systém školení
- [ ] Sledovanie pokroku
- [ ] Interaktívne tutoriály
- [ ] Testy a certifikáty

### Fáza 4: Správa zákazníkov
- [ ] Databáza zákazníkov
- [ ] HW špecifikácie
- [ ] Reporty a štatistiky
- [ ] Export dát

## 📝 Príklad použitia

```python
# Príklad: Pridať novú špecifikáciu IS
from modules.specifications import ISSpecification

# Vytvor novú špecifikáciu
spec = ISSpecification()
spec.name = "Moj IS System"
spec.version = "1.0"
spec.add_module("Užívatelia", "Správa užívateľských účtov")
spec.save()

# Opožiadaj AI o vysvetlenie
from modules.ai_assistant import AIAssistant

ai = AIAssistant()
response = ai.explain_module("Užívatelia")
print(response)
```

## 🤝 Ako prispieť

1. Fork-ni projekt
2. Vytvor branch (`git checkout -b feature/NovaFunkcia`)
3. Commit zmeny (`git commit -m 'Pridana nova funkcia'`)
4. Push do branchu (`git push origin feature/NovaFunkcia`)
5. Otvor Pull Request

## 💬 Návod pre začiatočníkov

**Si začiatočník?** Žiadny problém!

1. **Naklonuj projekt** vo Visual Studiu (File → Clone Repository)
2. **Otvor AI asistenta** (napr. GitHub Copilot)
3. **Požiadaj AI** o pomoc: "Vytvor základnú štruktúru pre tento projekt"
4. **Sleduj tento README** - každá sekcia ti pove, čo máš vytvoriť

## 📞 Kontakt

Pre otázky a návrhy:
- GitHub Issues: [Otvor issue](https://github.com/Nerdzsk/IS-Assistant/issues)
- Email: [tvoj-email]

## 📜 Licencia

MIT License - viď [LICENSE](LICENSE) súbor

---

**Vytvorené s ❤️ pre lepšiu prácu s informačnými systémami**
