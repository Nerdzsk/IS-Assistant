#!/usr/bin/env python3
"""Oprava Whisper kódu aby čítał audio bez FFmpeg"""

import re

# Čítaj súbor
with open('webapp.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Vyhľadaj a zamen kód
old_code = '''        # Konvertuj pomocou Whisper - použijeme súbor priamo
        import whisper
        
        # Načítaj model
        model = whisper.load_model('base', device='cpu')
        
        # Whisper vie pracovať priamo so súborom (netreba librosa)
        result = model.transcribe(temp_path, language='sk', fp16=False)
        text = result.get('text', '').strip()'''

new_code = '''        # Čítaj audio pomocou scipy bez FFmpeg
        import whisper
        import numpy as np
        from scipy.io import wavfile
        
        try:
            # Čítaj WAV súbor
            sr, audio_data = wavfile.read(temp_path)
            
            # Konvertuj na float32 a normalizuj
            if audio_data.dtype == np.int16:
                audio_data = audio_data.astype(np.float32) / 32768.0
            elif audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32)
            
            # Ak stereo, konvertuj na mono
            if len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data, axis=1)
            
            # Resample na 16kHz ak treba
            if sr != 16000:
                import librosa
                audio_data = librosa.resample(audio_data, orig_sr=sr, target_sr=16000)
        except Exception as read_error:
            return jsonify({'error': f'Nemožno čítať audio: {str(read_error)}'}), 400
        
        # Načítaj a používaj Whisper
        model = whisper.load_model('base', device='cpu')
        
        # Whisper teraz bude mať audio pole namiesto cesty
        result = model.transcribe(audio=audio_data, language='sk', fp16=False)
        text = result.get('text', '').strip()'''

# Zamen
if old_code in content:
    content = content.replace(old_code, new_code)
    # Zapíš späť
    with open('webapp.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Kód bol úspešne opravený!")
else:
    print("✗ Nepodarilo sa nájsť kód na opravu")
