#!/usr/bin/env python3
"""Opraví všetky neescape-ované ${} vzorce v JavaScript časti"""

import re

with open('webapp.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Nájdi všetky `${...}` vzorce ktoré nie sú escapované (\$)
# Ale sú v JavaScript backtick stringoch

# Spôsob: nájdi všetky ${...} a nahraď ich s \$
# Skúsim regex na najdenie neescape-ovaných ${}
pattern = r'\$\{([^}]+)\}'
replacement = r'\${\1}'

# Počítaj matches
matches = list(re.finditer(pattern, content))
print(f"Nájdených neescape-ovaných ${{}}: {len(matches)}")

# Pokiaľ existujú neescape-ované ${}, nahraď ich
if matches:
    content_new = re.sub(r'(?<!\\)\$\{([^}]+)\}', r'\\\${\1}', content)
    
    with open('webapp.py', 'w', encoding='utf-8') as f:
        f.write(content_new)
    
    print(f"✓ Všetky ${{}} vzorce boli escapované")
else:
    print("✓ Žiadne neescape-ované ${{}} vzorce neboli nájdené")
