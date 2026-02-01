#!/usr/bin/env python3
"""
Aplikačný monitor - spúšťa Flask a monitoruje ho.
Ak aplikácia spadne, automaticky ju reštartuje.
"""

import subprocess
import time
import os
import sys
from datetime import datetime

APP_DIR = r"e:\AI\IS- Assistent\IS-Assistant"
PYTHON_EXE = os.path.join(APP_DIR, ".venv", "Scripts", "python.exe")
WEBAPP_PY = os.path.join(APP_DIR, "webapp.py")
LOG_FILE = os.path.join(APP_DIR, "app_monitor.log")

def log(message):
    """Zapíš správu do logu a konzoly"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{timestamp}] {message}"
    print(msg)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')

def start_app():
    """Spusti Flask aplikáciu"""
    log("=" * 60)
    log("Zapínam Flask aplikáciu...")
    log(f"Python: {PYTHON_EXE}")
    log(f"Súbor: {WEBAPP_PY}")
    
    process = subprocess.Popen(
        [PYTHON_EXE, WEBAPP_PY],
        cwd=APP_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return process

def monitor():
    """Monitoruj aplikáciu a reštartuj ju ak spadne"""
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    
    log("=== MONITOR APLIKÁCIE SPUSTENÝ ===")
    log("Monitorujem: http://127.0.0.1:5000")
    log("Aplikácia sa automaticky reštartuje ak spadne")
    log("")
    
    restart_count = 0
    
    while True:
        try:
            process = start_app()
            restart_count += 1
            log(f"Aplikácia spustená (pokus #{restart_count})")
            
            # Čakaj aby sa aplikácia spustila
            time.sleep(3)
            
            # Monitoruj proces
            while process.poll() is None:
                # Proces stále beží
                time.sleep(5)
            
            # Proces spadol
            log(f"⚠️  APLIKÁCIA SPADLA (exit code: {process.returncode})")
            
            # Čakaj pred reštartom
            log("Čakám 3 sekundy pred reštartom...")
            time.sleep(3)
            
        except Exception as e:
            log(f"❌ CHYBA: {str(e)}")
            time.sleep(3)

if __name__ == '__main__':
    try:
        monitor()
    except KeyboardInterrupt:
        log("\nMonitor zastavený používateľom (Ctrl+C)")
        sys.exit(0)
