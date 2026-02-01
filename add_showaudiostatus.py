#!/usr/bin/env python3
"""Pridaj showAudioStatus funkciu"""

with open('webapp.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Nájdi riadok s event listenerom
old_code = '''        document.getElementById('recordBtn').addEventListener('click', function() {
            if (!recognition) {
                showAudioStatus('Tvoj prehliadac nepodporuje rozpoznavanie reči. Skuste Chrome, Edge alebo Firefox.', 'error');
                return;
            }
            recognition.start();
        });'''

new_code = '''        function showAudioStatus(message, type) {
            const statusDiv = document.getElementById('audioStatus');
            if (!statusDiv) return;
            
            statusDiv.textContent = message;
            statusDiv.style.display = 'block';
            
            if (type === 'success') {
                statusDiv.style.background = '#d4edda';
                statusDiv.style.color = '#155724';
                statusDiv.style.border = '1px solid #c3e6cb';
            } else if (type === 'error') {
                statusDiv.style.background = '#f8d7da';
                statusDiv.style.color = '#721c24';
                statusDiv.style.border = '1px solid #f5c6cb';
            } else {
                statusDiv.style.background = '#d1ecf1';
                statusDiv.style.color = '#0c5460';
                statusDiv.style.border = '1px solid #bee5eb';
            }
        }
        
        document.getElementById('recordBtn').addEventListener('click', function() {
            if (!recognition) {
                showAudioStatus('Tvoj prehliadac nepodporuje rozpoznavanie reči. Skuste Chrome, Edge alebo Firefox.', 'error');
                return;
            }
            recognition.start();
        });'''

if old_code in content:
    content = content.replace(old_code, new_code)
    print("✓ showAudioStatus funkcia pridaná")
else:
    print("✗ Nenašiel som event listener")

with open('webapp.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Hotovo!")
