# IS-Assistant – Fáza 1: Checklist

Tento checklist slúži na sledovanie pokroku v základnej implementácii podľa špecifikácie.

**Posledná aktualizácia:** Február 2026

## ✅ Dokončené úlohy

- [x] **Príprava prostredia**
    - [x] Skontrolovať a doinštalovať závislosti (Python 3.14+, SQLite, requirements.txt)
    - [x] Inicializovať git repozitár a nastaviť štruktúru adresárov
    - [x] Vytvoriť virtuálne prostredie (.venv)

- [x] **Návrh a implementácia databázy**
    - [x] Vytvoriť tabuľky podľa SPECIFICATION.md (modules, submodules, functionalities, relations, history)
    - [x] Pripraviť a otestovať SQL schému v database/schema.sql
    - [x] Implementovať inicializačný skript (init_db.py)
    - [x] Pridať tabuľku pre zákazníkov (customers)

- [x] **Základné Python moduly**
    - [x] Vytvoriť triedy a CRUD operácie pre moduly, podmoduly, funkcionality (modules/)
    - [x] Použiť PEP8, typovanie, docstringy
    - [x] Implementovať AI asistenta (modules/ai_assistant.py)

- [x] **Web aplikácia (webapp.py)**
    - [x] Flask server s moderným UI
    - [x] Dashboard (hlavná stránka)
    - [x] Formulár nového zákazníka
    - [x] Zoznam zákazníkov
    - [x] AI Chat rozhranie
    - [x] Wiki stránka

- [x] **AI poradca**
    - [x] Integrácia s Groq API (Llama model)
    - [x] AI parsovanie súhrnov (rozpoznanie firiem, pobočiek, kontaktov)
    - [x] Potvrdzovací modal pred vyplnením formulára

- [x] **Hlasové funkcie**
    - [x] Web Speech API pre rozpoznávanie reči
    - [x] Kontinuálne nahrávanie (kým nekliknete Zastaviť)
    - [x] Real-time zobrazenie rozpoznávaného textu

- [x] **Mapy a geolokácia**
    - [x] Google Maps embed pre adresy pobočiek
    - [x] Dynamická aktualizácia mapy pri zmene adresy

## 🔄 V procese

- [ ] **Testovanie a dokumentácia**
    - [ ] Pridať unit testy pre CRUD a AI logiku
    - [x] Doplniť dokumentáciu (README.md, user_guide.md)
    - [ ] Pridať príklady použitia

## 📋 Plánované

- [ ] **Iteratívne rozširovanie**
    - [ ] Pridať školiace moduly
    - [ ] Export/import údajov (CSV, JSON)
    - [ ] Pokročilé AI odpovede
    - [ ] Vizualizácia vzťahov medzi modulmi

---

Tento súbor bude priebežne aktualizovaný podľa stavu riešenia jednotlivých úloh.
