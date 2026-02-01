#!/usr/bin/env python3
"""Zmena event listeneru pre recordBtn na Web Speech API"""

with open('webapp.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Starý event listener
old_listener = '''        document.getElementById('recordBtn').addEventListener('click', async function() {
            console.log('Record button clicked');
            showAudioStatus('Ziadam o pristup k mikrofonu...', 'info');
            
            try {
                if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                    throw new Error('Vas prehliadac nepodporuje nahravanie zvuku. Skuste Chrome alebo Edge.');
                }
                
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                console.log('Got microphone access');
                
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];
                
                mediaRecorder.ondataavailable = event => audioChunks.push(event.data);
                mediaRecorder.onstop = async () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                    const formData = new FormData();
                    formData.append('audio', audioBlob, 'recording.webm');
                    
                    showAudioStatus('Konvertujem zvuk na text...', 'info');
                    document.getElementById('uploadAudioBtn').style.display = 'none';
                    
                    try {
                        const response = await fetch('/transcribe-audio', {
                            method: 'POST',
                            body: formData
                        });
                        
                        const data = await response.json();
                        
                        if (!response.ok) {
                            let errorMsg = data.error || 'Chyba pri konverzii';
                            if (data.details) {
                                console.error('Full error details:', data.details);
                                errorMsg += ' Details: ' + data.details;
                            }
                            throw new Error(errorMsg);
                        }
                        
                        // Pridaj text do textarey
                        const textarea = document.getElementById('summaryTextarea');
                        if (textarea.value.trim()) {
                            textarea.value += '\\n\\n' + data.text;
                        } else {
                            textarea.value = data.text;
                        }
                        
                        showAudioStatus('Zvuk bol uspesne konvertovany!', 'success');
                        
                    } catch (error) {
                        showAudioStatus('Chyba: ' + error.message, 'error');
                    }
                    
                    // Vrat stream
                    stream.getTracks().forEach(track => track.stop());
                };
                
                mediaRecorder.start();
                recordingStartTime = Date.now();
                
                document.getElementById('recordBtn').style.display = 'none';
                document.getElementById('stopBtn').style.display = 'inline-block';
                document.getElementById('recordingTime').textContent = '0:00';
                
                timerInterval = setInterval(() => {
                    const elapsed = Math.floor((Date.now() - recordingStartTime) / 1000);
                    const minutes = Math.floor(elapsed / 60);
                    const seconds = elapsed % 60;
                    document.getElementById('recordingTime').textContent = 
                        minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
                }, 100);
                
            } catch (error) {
                console.error('Microphone error:', error);
                showAudioStatus('Chyba pri pristupe k mikrofonu: ' + error.message, 'error');
                
                // Reset buttons
                document.getElementById('recordBtn').style.display = 'inline-block';
                document.getElementById('stopBtn').style.display = 'none';
            }
        });'''

new_listener = '''        // Web Speech API
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognition = null;
        
        if (SpeechRecognition) {
            recognition = new SpeechRecognition();
            recognition.lang = 'sk-SK';
            recognition.continuous = false;
            recognition.interimResults = true;
            
            recognition.onstart = () => {
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
                }
            };
            
            recognition.onerror = (event) => {
                showAudioStatus('Chyba: ' + event.error, 'error');
                document.getElementById('recordBtn').textContent = 'Zacat nahravanie';
                document.getElementById('recordBtn').style.background = '#ef5350';
            };
            
            recognition.onend = () => {
                document.getElementById('recordBtn').textContent = 'Zacat nahravanie';
                document.getElementById('recordBtn').style.background = '#ef5350';
            };
        }
        
        document.getElementById('recordBtn').addEventListener('click', function() {
            if (!recognition) {
                showAudioStatus('Tvoj prehliadač nepodporuje Web Speech API. Skús Chrome alebo Edge.', 'error');
                return;
            }
            recognition.start();
        });'''

if old_listener in content:
    content = content.replace(old_listener, new_listener)
    print("✓ Event listener nahradený")
else:
    print("✗ Nenašiel som event listener")

with open('webapp.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Hotovo!")
