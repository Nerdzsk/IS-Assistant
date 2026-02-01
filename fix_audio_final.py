#!/usr/bin/env python3
"""Odstránenie starého audio kódu a vloženie Web Speech API"""

# Čítaj súbor
with open('webapp.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Nájdi riadok s "let timerInterval;"
start_line = None
end_line = None

for i, line in enumerate(lines):
    if 'let timerInterval;' in line:
        start_line = i
    if start_line is not None and 'let companyCount = 1;' in line:
        end_line = i
        break

if start_line is not None and end_line is not None:
    print(f"Nájdená audio sekcia: riadky {start_line+1} až {end_line+1}")
    
    # Vytvor nový Web Speech API kód
    new_code = '''        let timerInterval;
        
        // Web Speech API - rozpoznávanie reči priamo v prehliadači
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognition = null;
        
        if (SpeechRecognition) {
            recognition = new SpeechRecognition();
            recognition.lang = 'sk-SK';
            recognition.continuous = false;
            recognition.interimResults = true;
            
            recognition.onstart = () => {
                console.log('Počúvam...');
                showAudioStatus('Počúvam... hovor teraz', 'info');
                document.getElementById('recordBtn').textContent = 'Počúvam...';
                document.getElementById('recordBtn').style.background = '#ff9800';
            };
            
            recognition.onresult = (event) => {
                let transcript = '';
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    transcript += event.results[i][0].transcript;
                }
                
                if (event.isFinal) {
                    const textarea = document.getElementById('summaryTextarea');
                    if (textarea.value.trim()) {
                        textarea.value += '\\n\\n' + transcript;
                    } else {
                        textarea.value = transcript;
                    }
                    
                    showAudioStatus('OK! Text bol pridaný. Klikni znova pre ďalší zvuk.', 'success');
                    console.log('Finálny text:', transcript);
                }
            };
            
            recognition.onerror = (event) => {
                console.error('Speech Error:', event.error);
                let errorMsg = 'Chyba: ' + event.error;
                if (event.error === 'no-speech') {
                    errorMsg = 'Nič som nepoužul. Skús znova.';
                } else if (event.error === 'network') {
                    errorMsg = 'Problém so sieťou. Skúť neskôr.';
                }
                showAudioStatus(errorMsg, 'error');
                document.getElementById('recordBtn').textContent = 'Zacat nahravanie';
                document.getElementById('recordBtn').style.background = '#ef5350';
            };
            
            recognition.onend = () => {
                console.log('Ukončené');
                document.getElementById('recordBtn').textContent = 'Zacat nahravanie';
                document.getElementById('recordBtn').style.background = '#ef5350';
            };
        } else {
            console.warn('Web Speech API nie je podporovaná');
        }
        
        document.getElementById('recordBtn').addEventListener('click', function() {
            console.log('Record button clicked, recognition:', recognition);
            if (!recognition) {
                showAudioStatus('Tvoj prehliadač nepodporuje rozpoznávanie reči. Skús Chrome, Edge alebo Firefox.', 'error');
                return;
            }
            try {
                recognition.start();
            } catch (e) {
                console.error('Chyba pri štarte:', e);
            }
        });
        
        // Skry stop tlačidlo
        const stopBtn = document.getElementById('stopBtn');
        if (stopBtn) stopBtn.style.display = 'none';
        
        // Skry upload button
        const uploadBtn = document.getElementById('uploadAudioBtn');
        if (uploadBtn) uploadBtn.style.display = 'none';
        
        let companyCount = 1;
'''
    
    # Nahraď
    new_lines = lines[:start_line] + [new_code + '\n'] + lines[end_line:]
    
    # Zapíš
    with open('webapp.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("✓ Audio sekcia nahradená Web Speech API")
else:
    print("✗ Nenašiel som audio sekciu")
