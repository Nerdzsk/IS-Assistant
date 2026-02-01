# Používateľská príručka IS-Assistant

**Verzia:** 1.0  
**Posledná aktualizácia:** Február 2026

---

## 📖 Obsah

1. [Úvod](#úvod)
2. [Inštalácia a spustenie](#inštalácia-a-spustenie)
3. [Hlavné funkcie](#hlavné-funkcie)
4. [Pridanie nového zákazníka](#pridanie-nového-zákazníka)
5. [Hlasové nahrávanie](#hlasové-nahrávanie)
6. [AI parsovanie](#ai-parsovanie)
7. [AI Chat](#ai-chat)
8. [Wiki](#wiki)

---

## Úvod

IS-Assistant je webová aplikácia pre správu informačných systémov a zákazníkov. Aplikácia využíva AI pre inteligentné spracovanie údajov a hlasový vstup.

---

## Inštalácia a spustenie

### Požiadavky
- Python 3.9 alebo novší
- Internetové pripojenie (pre AI a mapy)
- Prehliadač s podporou Web Speech API (Chrome, Edge, Firefox)

### Inštalácia

```bash
# Klonovanie repozitára
git clone https://github.com/Nerdzsk/IS-Assistant.git
cd IS-Assistant

# Vytvorenie virtuálneho prostredia
python -m venv .venv

# Aktivácia (Windows)
.venv\Scripts\activate

# Inštalácia závislostí
pip install -r requirements.txt
```

### Spustenie

```bash
python webapp.py
```

Aplikácia bude dostupná na: **http://localhost:5000**

---

## Hlavné funkcie

### Dashboard (/)
- Prehľad systému
- Navigácia na ďalšie sekcie

### Zákazníci (/customers)
- Zoznam všetkých zákazníkov
- Vyhľadávanie a filtrovanie
- Detaily zákazníka

### Nový zákazník (/new-customer)
- Formulár pre pridanie zákazníka
- Hlasový vstup
- AI asistencia

### AI Chat (/ai-chat)
- Konverzácia s AI asistentom
- Otázky o informačných systémoch

### Wiki (/wiki)
- Dokumentácia
- Návody a tipy

---

## Pridanie nového zákazníka

### Postup:

1. **Prejdi na** `/new-customer`

2. **Zhrnutie** - Môžeš:
   - Napísať text manuálne
   - Použiť hlasové nahrávanie (klikni "Začať nahrávanie")

3. **AI parsovanie** - Klikni "Nech AI parseuje súhrn"
   - AI rozpozná: meno, email, telefón, firmy, pobočky
   - Zobrazí sa potvrdzovací modal
   - Môžeš upraviť hodnoty pred potvrdením

4. **Doplň údaje** - Vyplň zostávajúce polia

5. **Ulož** - Klikni "Uložiť zákazníka"

---

## Hlasové nahrávanie

### Ako používať:

1. Klikni **"● Začať nahrávanie"**
2. Hovor do mikrofónu
3. Text sa zobrazuje v reálnom čase
4. Klikni **"⏹ Zastaviť"** keď skončíš

### Podporované prehliadače:
- ✅ Google Chrome
- ✅ Microsoft Edge
- ✅ Firefox
- ❌ Safari (čiastočná podpora)

### Tipy:
- Hovor zreteľne a v slovenčine
- Ak je ticho dlhšie ako 60 sekúnd, nahrávanie sa automaticky reštartuje
- Rozpoznaný text sa pridáva do textového poľa priebežne

---

## AI parsovanie

AI dokáže automaticky rozpoznať:

### Kontaktné údaje:
- Meno kontaktnej osoby
- Email
- Telefónne číslo

### Firmy:
- Názov firmy
- IČO

### Pobočky/Prevádzky:
- Názov pobočky
- Adresa (ak je kompletná)
- Typ podnikania (reštaurácia, obchod, e-shop, sklad, kancelária, výrobňa, servis)

### Potvrdzovací modal:
- Zobrazí rozpoznané údaje
- Môžeš upraviť hodnoty
- Google Maps mapa pre adresy
- Checkboxy pre typ podnikania

---

## AI Chat

### Ako používať:

1. Prejdi na `/ai-chat`
2. Napíš otázku do textového poľa
3. Stlač Enter alebo klikni "Odoslať"
4. AI odpovie do niekoľkých sekúnd

### Príklady otázok:
- "Čo je to informačný systém?"
- "Ako pridať nového zákazníka?"
- "Aké moduly má náš IS?"

---

## Wiki

Wiki obsahuje dokumentáciu a návody pre prácu s IS-Assistant.

### Sekcie:
- Návody pre používateľov
- Technická dokumentácia
- FAQ

---

## Riešenie problémov

### Hlasové nahrávanie nefunguje
- Skontroluj, či máš povolený mikrofón v prehliadači
- Použi Chrome alebo Edge
- Skontroluj internetové pripojenie

### AI neodpovedá
- Skontroluj internetové pripojenie
- Skontroluj API kľúč v `config/settings.json`

### Mapa sa nezobrazuje
- Zadaj kompletnú adresu (ulica, číslo, mesto)
- Skontroluj internetové pripojenie

---

## Kontakt a podpora

Pre otázky a podporu kontaktujte správcu systému.
