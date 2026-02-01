#!/usr/bin/env python3
"""Oprava audio formátu z WAV na WebM"""

# Čítaj súbor
with open('webapp.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Zmena v JavaScripte - zmení WAV na WebM
old_js = "const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });\n                    const formData = new FormData();\n                    formData.append('audio', audioBlob, 'recording.wav');"

new_js = "const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });\n                    const formData = new FormData();\n                    formData.append('audio', audioBlob, 'recording.webm');"

if old_js in content:
    content = content.replace(old_js, new_js)
    print("✓ JavaScript kód zmenený na WebM")
else:
    print("✗ JavaScript kód nenájdený")

# 2. Zmena v backend kóde - čítaj webm namiesto wav
old_backend = '''        file_size = os.path.getsize(temp_path)
        if file_size == 0:
            return jsonify({'error': 'Audio súbor je prazdny'}), 400
        
        # Čítaj audio pomocou scipy bez FFmpeg
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

new_backend = '''        file_size = os.path.getsize(temp_path)
        if file_size == 0:
            return jsonify({'error': 'Audio súbor je prazdny'}), 400
        
        # Whisper dokáže čítať WebM priamo
        import whisper
        
        try:
            # Načítaj model
            model = whisper.load_model('base', device='cpu')
            
            # Whisper vie čítať WebM súbory priamo
            result = model.transcribe(temp_path, language='sk', fp16=False)
            text = result.get('text', '').strip()
        except Exception as read_error:
            return jsonify({'error': f'Nemožno spracovať audio: {str(read_error)}'}), 400
        '''

if old_backend in content:
    content = content.replace(old_backend, new_backend)
    print("✓ Backend kód zmenený na WebM")
else:
    print("✗ Backend kód nenájdený")

# Zapíš späť
with open('webapp.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Súbor bol uložený!")
