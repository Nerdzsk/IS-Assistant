#!/usr/bin/env python3
"""Odstránenie duplicitného audio kódu"""

with open('webapp.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Nájdi "let timerInterval;"
start = None
for i, line in enumerate(lines):
    if 'let timerInterval;' in line and i > 1200:  # Len druhú inštanciu (po riadku 1200)
        start = i
        break

# Nájdi koniec - "let companyCount = 1;" - ale hľadaj ďalšie ako teraz
if start:
    # Zmaž od "let timerInterval;" až do "let companyCount = 1;"
    end = None
    for i in range(start, len(lines)):
        if 'let companyCount = 1;' in lines[i] and i > start + 10:
            # To je tá ako za ním sú funkcie
            # Hľadaj kde končí starý kód - keď narazíš na "function addCompanyForm"
            # V linke file vidím že na 1137 (plus 3 = 1140) je function addCompanyForm
            # To je duplikat
            # Skúsme len zmazať zátvorkové kódy
            pass
    
    # Lepší prístup - zmaž všetko od "let timerInterval" do pred "function addCompanyForm"
    # alebo do pred "let companyCount"
    end = start
    for i in range(start, len(lines)):
        # Hľadaj "document.getElementById('stopBtn').addEventListener"
        if "document.getElementById('stopBtn').addEventListener" in lines[i]:
            end = i + 20  # Zmaž aj handler
            break
    
    if end and end > start:
        print(f"Mažem riadky {start+1} až {end+1}")
        new_lines = lines[:start] + lines[end:]
        
        with open('webapp.py', 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print("✓ Duplikátny kód zmazaný")
    else:
        print("✗ Nemožno nájsť koniec kódu")
else:
    print("✗ Nenašiel som timerInterval")
