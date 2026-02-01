#!/usr/bin/env python3
"""Oprava audio čítania - používaj pydub namiesto Whisper audio čítacieho"""

# Čítaj súbor
with open('webapp.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Zmena backend kódu na použitie pydub
old_backend = '''        # Whisper dokáže čítať WebM priamo
        import whisper
        
        try:
            # Načítaj model
            model = whisper.load_model('base', device='cpu')
            
            # Whisper vie čítať WebM súbory priamo
            result = model.transcribe(temp_path, language='sk', fp16=False)
            text = result.get('text', '').strip()
        except Exception as read_error:
            return jsonify({'error': f'Nemožno spracovať audio: {str(read_error)}'}), 400'''

new_backend = '''        # Čítaj WebM pomocou pydub a konvertuj na raw audio
        import whisper
        import numpy as np
        from pydub import AudioSegment
        
        try:
            # Načítaj WebM pomocou pydub
            audio = AudioSegment.from_file(temp_path, format='webm')
            
            # Konvertuj na mono ak je stereo
            if audio.channels > 1:
                audio = audio.set_channels(1)
            
            # Konvertuj na 16kHz ak je iná vzorkovacia frekvencia
            if audio.frame_rate != 16000:
                audio = audio.set_frame_rate(16000)
            
            # Konvertuj na numpy array
            samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
            
            # Normalizuj na rozsah [-1, 1]
            samples = samples / (2**15)
            
            # Načítaj model
            model = whisper.load_model('base', device='cpu')
            
            # Whisper teraz dostane raw audio pole
            result = model.transcribe(audio=samples, language='sk', fp16=False)
            text = result.get('text', '').strip()
        except Exception as read_error:
            return jsonify({'error': f'Nemožno spracovať audio: {str(read_error)}'}), 400'''

if old_backend in content:
    content = content.replace(old_backend, new_backend)
    print("✓ Backend kód zmenený na pydub + Whisper")
else:
    print("✗ Backend kód nenájdený")

# Zapíš späť
with open('webapp.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Súbor bol uložený!")
