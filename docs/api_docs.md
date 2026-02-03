# API dokumentácia IS-Assistant

**Verzia:** 1.0  
**Posledná aktualizácia:** Február 2026

---

## 📖 Obsah

1. [Prehľad](#prehľad)
2. [Endpointy](#endpointy)
3. [Autentifikácia](#autentifikácia)
4. [Príklady](#príklady)

---

## Prehľad

IS-Assistant poskytuje REST API pre integráciu s inými systémami. Všetky odpovede sú vo formáte JSON.

**Base URL:** `http://localhost:5000`

---

## Endpointy

### Stránky (HTML)

| Metóda | Endpoint | Popis |
|--------|----------|-------|
| GET | `/` | Hlavná stránka (dashboard) |
| GET | `/new-customer` | Formulár nového zákazníka |
| GET | `/customers` | Zoznam zákazníkov |
| GET | `/ai-chat` | AI Chat rozhranie |
| GET | `/wiki` | Wiki dokumentácia |
| GET | `/service` | Zoznam servisných prípadov s vyhľadávaním |
| GET | `/service/<id>` | Detail servisného prípadu s vetvením |
| POST | `/service/add` | Pridať nový servisný prípad |
| POST | `/service/<id>/add-step` | Pridať krok (vrátane vetvy) |
| POST | `/service/<id>/add-decision` | Pridať rozhodnutie s vetvami |
| POST | `/service/<id>/add-branch` | Pridať novú vetvu |
| POST | `/service/<id>/add-complication` | Pridať komplikáciu |
| POST | `/service/<id>/edit-step/<step_id>` | Upraviť existujúci krok |
| POST | `/service/<id>/delete-step/<step_id>` | Vymazať krok |

---

### API Endpointy (JSON)

#### POST `/ai-parse-summary`

Parsuje textový súhrn a extrahuje údaje pomocou AI.

**Request:**
```json
{
    "summary": "Text súhrnu zo stretnutia..."
}
```

**Response:**
```json
{
    "contact_name": "Ján Novák",
    "contact_email": "jan@firma.sk",
    "contact_phone": "+421 900 123 456",
    "companies": [
        {
            "name": "ABC s.r.o.",
            "ico": "12345678"
        }
    ],
    "branches": [
        {
            "name": "Reštaurácia Centrum",
            "address": "Hlavná 123, 811 01 Bratislava",
            "type": ["restauracia"],
            "location_hint": "centrum Bratislavy"
        }
    ]
}
```

**Možné typy pobočiek:**
- `restauracia` - Reštaurácia / Gastronómia
- `obchod` - Kamenný obchod
- `eshop` - E-shop / Online predaj
- `sklad` - Sklad
- `kancelaria` - Kancelária / Administratíva
- `vyrobna` - Výrobňa
- `servis` - Servisné stredisko
- `ine` - Iné

---

#### POST `/transcribe-audio`

Konvertuje audio súbor na text pomocou Whisper.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `audio` - audio súbor (WebM, WAV, MP3)

**Response:**
```json
{
    "text": "Rozpoznaný text z audio súboru..."
}
```

---

#### POST `/ai-chat` (AJAX)

Odošle správu AI asistentovi.

**Request:**
```json
{
    "message": "Čo je to informačný systém?"
}
```

**Response:**
```json
{
    "response": "Informačný systém je..."
}
```

---

## Autentifikácia

Momentálne API nepožaduje autentifikáciu. V budúcnosti bude pridaná podpora pre API kľúče.

---

## Príklady

### Python - Parsovanie súhrnu

```python
import requests

url = "http://localhost:5000/ai-parse-summary"
data = {
    "summary": "Stretol som sa s Jánom Novákom z firmy ABC s.r.o. (IČO 12345678). Majú reštauráciu na Hlavnej ulici v Bratislave."
}

response = requests.post(url, json=data)
result = response.json()

print(f"Kontakt: {result['contact_name']}")
print(f"Firmy: {result['companies']}")
print(f"Pobočky: {result['branches']}")
```

### JavaScript - Fetch API

```javascript
fetch('/ai-parse-summary', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        summary: 'Text súhrnu...'
    })
})
.then(response => response.json())
.then(data => {
    console.log('Parsované údaje:', data);
});
```

### cURL

```bash
curl -X POST http://localhost:5000/ai-parse-summary \
  -H "Content-Type: application/json" \
  -d '{"summary": "Text súhrnu..."}'
```

---

## Chybové odpovede

### 400 Bad Request
```json
{
    "error": "Žiadny súhrn nezadaný"
}
```

### 500 Internal Server Error
```json
{
    "error": "Popis chyby..."
}
```

---

## Konfigurácia

API konfigurácia sa nachádza v `config/settings.json`:

```json
{
    "ai": {
        "provider": "groq",
        "api_key": "YOUR_API_KEY",
        "model": "llama-3.3-70b-versatile"
    }
}
```

---

## Changelog

### v1.1 (Február 2026)
- SERVIS sekcia s prípadovými štúdiami
- Vetvenie postupov (rozhodnutia s možnosťami)
- Vyhľadávanie v prípadových štúdiách
- Editácia a mazanie krokov
- Wiki s kolapsibilnou štruktúrou

### v1.0 (Február 2026)
- Základné API endpointy
- AI parsovanie súhrnov
- Hlasová transkripcia (Whisper)
- AI Chat
