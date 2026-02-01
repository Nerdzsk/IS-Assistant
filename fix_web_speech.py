#!/usr/bin/env python3
"""Zmena audio kódu na Web Speech API"""

# Čítaj súbor
with open('webapp.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Vyhľadaj a zamen celu audio sekciu
old_audio = '''        let companyCount = 1;
        
        function addCompanyForm() {'''

new_audio = '''        // Web Speech API pre rozpoznávanie reči
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognition = null;
        
        if (SpeechRecognition) {
            recognition = new SpeechRecognition();
            recognition.lang = 'sk-SK';
            recognition.continuous = false;
            recognition.interimResults = false;
            
            recognition.onstart = () => {
                showAudioStatus('Počúvam...', 'info');
                document.getElementById('recordBtn').style.background = '#ef5350';
                document.getElementById('recordBtn').textContent = 'Pocuvam...';
            };
            
            recognition.onresult = (event) => {
                const transcript = Array.from(event.results)
                    .map(result => result[0].transcript)
                    .join(' ');
                
                const textarea = document.getElementById('summaryTextarea');
                if (textarea.value.trim()) {
                    textarea.value += '\\n\\n' + transcript;
                } else {
                    textarea.value = transcript;
                }
                
                showAudioStatus('Pripravene! Klikni znova pre viac zvuku.', 'success');
                document.getElementById('recordBtn').style.background = '#ef5350';
                document.getElementById('recordBtn').textContent = '● Zacat nahravanie';
            };
            
            recognition.onerror = (event) => {
                showAudioStatus('Chyba: ' + event.error, 'error');
                document.getElementById('recordBtn').style.background = '#ef5350';
                document.getElementById('recordBtn').textContent = '● Zacat nahravanie';
            };
            
            recognition.onend = () => {
                document.getElementById('recordBtn').style.background = '#ef5350';
                document.getElementById('recordBtn').textContent = '● Zacat nahravanie';
            };
        }
        
        document.getElementById('recordBtn').addEventListener('click', function() {
            if (!recognition) {
                showAudioStatus('Tvoj prehliadac nepodporuje rozpoznavanie reči. Skuste Chrome, Edge alebo Firefox.', 'error');
                return;
            }
            recognition.start();
        });
        
        // Zmaž staré event listenery pre stopBtn
        document.getElementById('stopBtn').style.display = 'none';
        
        let companyCount = 1;
        
        function addCompanyForm() {'''

# Nájdi presný kód na výmenu
if old_audio in content:
    content = content.replace(old_audio, new_audio)
    print("✓ Audio kód zmenený na Web Speech API")
else:
    print("✗ Nenašiel som presný kód")
    # Skúsim nájsť komplet audio sekciu
    if 'let timerInterval;' in content:
        # Nájdi začiatok audio sekcie
        start_idx = content.find('let timerInterval;')
        # Nájdi koniec (pred addCompanyForm)
        end_idx = content.find('let companyCount = 1;', start_idx)
        if start_idx != -1 and end_idx != -1:
            # Náhrada
            new_section = '''let timerInterval;
        
        // Web Speech API pre rozpoznávanie reči
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognition = null;
        
        if (SpeechRecognition) {
            recognition = new SpeechRecognition();
            recognition.lang = 'sk-SK';
            recognition.continuous = false;
            recognition.interimResults = false;
            
            recognition.onstart = () => {
                showAudioStatus('Počúvam...', 'info');
                document.getElementById('recordBtn').style.background = '#ef5350';
                document.getElementById('recordBtn').textContent = 'Pocuvam...';
            };
            
            recognition.onresult = (event) => {
                const transcript = Array.from(event.results)
                    .map(result => result[0].transcript)
                    .join(' ');
                
                const textarea = document.getElementById('summaryTextarea');
                if (textarea.value.trim()) {
                    textarea.value += '\\n\\n' + transcript;
                } else {
                    textarea.value = transcript;
                }
                
                showAudioStatus('Pripravene! Klikni znova pre viac zvuku.', 'success');
                document.getElementById('recordBtn').style.background = '#ef5350';
                document.getElementById('recordBtn').textContent = '● Zacat nahravanie';
            };
            
            recognition.onerror = (event) => {
                showAudioStatus('Chyba: ' + event.error, 'error');
                document.getElementById('recordBtn').style.background = '#ef5350';
                document.getElementById('recordBtn').textContent = '● Zacat nahravanie';
            };
            
            recognition.onend = () => {
                document.getElementById('recordBtn').style.background = '#ef5350';
                document.getElementById('recordBtn').textContent = '● Zacat nahravanie';
            };
        }
        
        document.getElementById('recordBtn').addEventListener('click', function() {
            if (!recognition) {
                showAudioStatus('Tvoj prehliadac nepodporuje rozpoznavanie reči. Skuste Chrome, Edge alebo Firefox.', 'error');
                return;
            }
            recognition.start();
        });
        
        // Skry stop tlačidlo
        document.getElementById('stopBtn').style.display = 'none';
        
        let companyCount = 1;'''
            
            # Nájdi konce do "let companyCount = 1;"
            content = content[:start_idx] + new_section + content[end_idx:]
            print("✓ Audio sekcia nahradená Web Speech API")

# Zapíš späť
with open('webapp.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Súbor bol uložený!")
