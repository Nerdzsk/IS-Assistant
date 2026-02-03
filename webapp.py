from flask import Flask, render_template_string, request, jsonify, redirect
from modules.ai_assistant import AIAssistant

app = Flask(__name__)
ai = AIAssistant()


# HTML šablóna pre vyhľadávanie
HTML = '''
<!doctype html>
<html lang="sk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IS-Assistant | Vyhľadávanie</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2d3436 0%, #636e72 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: #1e272e;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            padding: 40px;
            max-width: 600px;
            width: 100%;
        }
        h1 {
            color: #74b9ff;
            margin-bottom: 30px;
            text-align: center;
            font-size: 2em;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            color: #b2bec3;
            font-weight: 600;
            margin-bottom: 8px;
        }
        select, input {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #636e72;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s;
            background: #2d3436;
            color: #dfe6e9;
        }
        select:focus, input:focus {
            outline: none;
            border-color: #74b9ff;
            box-shadow: 0 0 0 3px rgba(116,185,255,0.2);
        }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #0984e3 0%, #74b9ff 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(116,185,255,0.4);
        }
        button:active {
            transform: translateY(0);
        }
        .nav-link {
            display: inline-block;
            margin-top: 15px;
            margin-right: 15px;
            color: #74b9ff;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s;
        }
        .nav-link:hover {
            color: #0984e3;
        }
        .result {
            margin-top: 30px;
            padding: 20px;
            background: #2d3436;
            border-radius: 10px;
            border-left: 4px solid #74b9ff;
        }
        .result h2 {
            color: #74b9ff;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        .result pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            color: #dfe6e9;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 IS-Assistant</h1>
        <form method="post">
            <div class="form-group">
                <label>Typ vyhľadávania:</label>
                <select name="typ">
                    <option value="module">Modul</option>
                    <option value="functionality">Funkcionalita</option>
                </select>
            </div>
            <div class="form-group">
                <label>Názov:</label>
                <input name="nazov" required placeholder="Zadajte názov...">
            </div>
            <button type="submit">🔎 Vyhľadať</button>
        </form>
        <div style="margin-top: 20px;">
            <a href="/ai-chat" class="nav-link">💬 AI asistent</a>
            <a href="/wiki" class="nav-link">📚 Wiki</a>
            <a href="/new-customer" class="nav-link">👤 Nový zákazník</a>
            <a href="/customers" class="nav-link">👥 Zákazníci</a>
            <a href="/service" class="nav-link">🔧 Servis</a>
            <a href="/training" class="nav-link">🎓 Školenia</a>
        </div>
        {% if vysledok %}
        <div class="result">
            <h2>Výsledok:</h2>
            <pre>{{ vysledok }}</pre>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

# HTML šablóna pre AI chat
AI_CHAT_HTML = '''
<!doctype html>
<html lang="sk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IS-Assistant | AI Asistent</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2d3436 0%, #636e72 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: #1e272e;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            padding: 40px;
            max-width: 800px;
            width: 100%;
        }
        h1 {
            color: #74b9ff;
            margin-bottom: 30px;
            text-align: center;
            font-size: 2em;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            color: #b2bec3;
            font-weight: 600;
            margin-bottom: 8px;
        }
        textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #636e72;
            border-radius: 10px;
            font-size: 16px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            resize: vertical;
            transition: all 0.3s;
            background: #2d3436;
            color: #dfe6e9;
        }
        textarea:focus {
            outline: none;
            border-color: #74b9ff;
            box-shadow: 0 0 0 3px rgba(116,185,255,0.2);
        }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #0984e3 0%, #74b9ff 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(116,185,255,0.4);
        }
        button:active {
            transform: translateY(0);
        }
        .nav-link {
            display: inline-block;
            margin-top: 20px;
            color: #74b9ff;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s;
            margin-right: 15px;
        }
        .nav-link:hover {
            color: #0984e3;
        }
        .answer-box {
            margin-top: 30px;
            padding: 25px;
            background: linear-gradient(135deg, #2d3436 0%, #353b48 100%);
            border-radius: 15px;
            border-left: 5px solid #74b9ff;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        .answer-box h2 {
            color: #74b9ff;
            margin-bottom: 15px;
            font-size: 1.3em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .answer-box pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            color: #dfe6e9;
            line-height: 1.8;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .icon {
            font-size: 1.5em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>💬 AI Asistent</h1>
        <form method="post">
            <div class="form-group">
                <label>Vaša otázka:</label>
                <textarea name="otazka" rows="4" required placeholder="Napríklad: Aké máme moduly? Čo robí modulUsers?">{{ otazka or '' }}</textarea>
            </div>
            <button type="submit">🚀 Opýtať sa AI</button>
        </form>
        <div style="margin-top: 20px;">
            <a href="/" class="nav-link">← Späť na vyhľadávanie</a>
            <a href="/wiki" class="nav-link">📚 Wiki</a>
            <a href="/new-customer" class="nav-link">👤 Nový zákazník</a>
            <a href="/customers" class="nav-link">👥 Zákazníci</a>
            <a href="/service" class="nav-link">🔧 Servis</a>
            <a href="/training" class="nav-link">🎓 Školenia</a>
        </div>
        {% if odpoved %}
        <div class="answer-box">
            <h2><span class="icon">🤖</span> Odpoveď AI:</h2>
            <pre>{{ odpoved }}</pre>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

# HTML šablóna pre Wiki / Štruktúru
WIKI_HTML = '''
<!doctype html>
<html lang="sk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IS-Assistant | Wiki</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2d3436 0%, #636e72 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .admin-panel {
            background: #1e272e;
            border: 2px dashed #74b9ff;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 30px;
        }
        .admin-panel h2 {
            color: #74b9ff;
            margin-bottom: 15px;
        }
        .admin-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }
        .admin-card {
            background: #2d3436;
            border-radius: 12px;
            padding: 15px;
            border-left: 4px solid #74b9ff;
        }
        .admin-card h3 {
            color: #81ecec;
            margin-bottom: 10px;
        }
        .admin-card label {
            display: block;
            font-weight: 600;
            margin-top: 10px;
            margin-bottom: 6px;
            color: #b2bec3;
        }
        .admin-card input, .admin-card select, .admin-card textarea {
            width: 100%;
            padding: 10px;
            border: 2px solid #636e72;
            border-radius: 8px;
            font-size: 14px;
            background: #1e272e;
            color: #dfe6e9;
        }
        .admin-card button {
            margin-top: 12px;
            width: 100%;
            padding: 10px;
            background: linear-gradient(135deg, #0984e3 0%, #74b9ff 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
        }
        .admin-note {
            margin-top: 10px;
            font-size: 0.9em;
            color: #b2bec3;
        }
        .message {
            padding: 12px 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .message.success {
            background: #00b894;
            color: white;
            border: 1px solid #00cec9;
        }
        .message.error {
            background: #d63031;
            color: white;
            border: 1px solid #ff7675;
        }
        .submodules {
            margin-top: 15px;
            padding-left: 20px;
            border-left: 2px dashed #636e72;
        }
        .submodules-header {
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            padding: 10px;
            background: #2d3436;
            border-radius: 8px;
            margin-bottom: 10px;
            transition: background 0.3s;
            color: #dfe6e9;
        }
        .submodules-header:hover {
            background: #353b48;
        }
        .toggle-btn {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            background: linear-gradient(135deg, #0984e3 0%, #74b9ff 100%);
            color: white;
            border: none;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.3s;
        }
        .toggle-btn.collapsed {
            transform: rotate(0deg);
        }
        .toggle-btn.expanded {
            transform: rotate(45deg);
        }
        .submodules-content {
            overflow: hidden;
            transition: max-height 0.4s ease-out;
        }
        .submodules-content.collapsed {
            max-height: 0;
        }
        .submodules-content.expanded {
            max-height: 5000px;
        }
        .submodule-item {
            margin-bottom: 5px;
        }
        .submodule-name {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 12px 15px;
            background: linear-gradient(135deg, #2d3436 0%, #353b48 100%);
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            color: #81ecec;
            transition: all 0.3s;
            border-left: 3px solid #81ecec;
        }
        .submodule-name:hover {
            background: linear-gradient(135deg, #353b48 0%, #485460 100%);
            transform: translateX(5px);
        }
        .submodule-arrow {
            font-size: 0.8em;
            transition: transform 0.3s;
            color: #74b9ff;
        }
        .submodule-arrow.expanded {
            transform: rotate(90deg);
        }
        .submodule-detail {
            overflow: hidden;
            transition: max-height 0.3s ease-out, opacity 0.3s;
        }
        .submodule-detail.collapsed {
            max-height: 0;
            opacity: 0;
        }
        .submodule-detail.expanded {
            max-height: 2000px;
            opacity: 1;
        }
        .submodule-card {
            background: #2d3436;
            border-radius: 12px;
            padding: 15px;
            margin: 10px 0 12px 25px;
            border-left: 4px solid #81ecec;
        }
        .relationships {
            margin-top: 15px;
            padding-left: 50px;
        }
        .relationship-item {
            background: #2d3436;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 8px;
            border-left: 3px solid #74b9ff;
            font-size: 0.95em;
            color: #dfe6e9;
        }
        .container {
            background: #1e272e;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            padding: 40px;
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: #74b9ff;
            margin-bottom: 30px;
            text-align: center;
            font-size: 2.5em;
        }
        .nav-links {
            margin-bottom: 30px;
            text-align: center;
        }
        .nav-link {
            display: inline-block;
            margin: 0 10px;
            color: #74b9ff;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s;
        }
        .nav-link:hover {
            color: #0984e3;
        }
        .modules-list {
            margin-top: 20px;
        }
        .module-item {
            margin-bottom: 8px;
        }
        .module-name {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 15px 20px;
            background: linear-gradient(135deg, #0984e3 0%, #74b9ff 100%);
            border-radius: 10px;
            cursor: pointer;
            color: white;
            font-weight: 600;
            font-size: 1.1em;
            transition: all 0.3s;
            box-shadow: 0 3px 10px rgba(116,185,255,0.3);
        }
        .module-name:hover {
            transform: translateX(5px);
            box-shadow: 0 5px 15px rgba(116,185,255,0.4);
        }
        .module-arrow {
            font-size: 0.9em;
            transition: transform 0.3s;
        }
        .module-arrow.expanded {
            transform: rotate(90deg);
        }
        .module-icon {
            font-size: 1.3em;
        }
        .module-title-text {
            flex: 1;
        }
        .module-badge {
            background: rgba(255,255,255,0.2);
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 500;
        }
        .module-detail {
            overflow: hidden;
            transition: max-height 0.4s ease-out, opacity 0.3s;
        }
        .module-detail.collapsed {
            max-height: 0;
            opacity: 0;
        }
        .module-detail.expanded {
            max-height: 10000px;
            opacity: 1;
        }
        .module-card {
            background: linear-gradient(135deg, #2d3436 0%, #353b48 100%);
            border-radius: 15px;
            padding: 25px;
            margin: 10px 0 15px 20px;
            border-left: 5px solid #74b9ff;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        .module-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
        }
        .module-title {
            flex: 1;
        }
        .module-title h2 {
            color: #74b9ff;
            font-size: 1.5em;
            margin-bottom: 5px;
        }
        .module-version {
            background: #74b9ff;
            color: #1e272e;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }
        .module-description {
            color: #b2bec3;
            line-height: 1.6;
            margin-bottom: 20px;
            padding-left: 50px;
        }
        .functionalities {
            padding-left: 50px;
        }
        .functionalities h3 {
            color: #81ecec;
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        .functionality-item {
            background: #1e272e;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            border-left: 3px solid #81ecec;
            transition: all 0.3s;
        }
        .functionality-item:hover {
            box-shadow: 0 3px 10px rgba(129,236,236,0.2);
            transform: translateX(5px);
        }
        .functionality-name {
            color: #81ecec;
            font-weight: 600;
            margin-bottom: 5px;
        }
        .functionality-description {
            color: #b2bec3;
            font-size: 0.95em;
            line-height: 1.5;
        }
        .no-data {
            text-align: center;
            color: #636e72;
            padding: 40px;
            font-style: italic;
        }
        .stats {
            background: linear-gradient(135deg, #0984e3 0%, #74b9ff 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 30px;
            text-align: center;
        }
        .stats h3 {
            font-size: 1.1em;
            margin-bottom: 10px;
        }
        .stats-numbers {
            display: flex;
            justify-content: center;
            gap: 40px;
            flex-wrap: wrap;
        }
        .stat-item {
            font-size: 1.5em;
            font-weight: 600;
        }
        .stat-label {
            font-size: 0.7em;
            opacity: 0.9;
        }
        .voice-controls {
            display: flex;
            gap: 8px;
            align-items: center;
            margin-top: 8px;
            flex-wrap: wrap;
        }
        .voice-btn {
            padding: 6px 12px;
            border: none;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            font-size: 0.85em;
            transition: all 0.2s;
        }
        .voice-btn.record {
            background: #ef5350;
            color: white;
        }
        .voice-btn.record:hover {
            background: #d32f2f;
        }
        .voice-btn.stop {
            background: #ff9800;
            color: white;
        }
        .voice-btn.stop:hover {
            background: #f57c00;
        }
        .voice-status {
            font-size: 0.8em;
            color: #b2bec3;
            padding: 4px 8px;
            background: #2d3436;
            border-radius: 4px;
        }
        .voice-status.recording {
            background: #d63031;
            color: white;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 IS-Assistant Wiki</h1>
        <div class="nav-links">
            <a href="/" class="nav-link">🔍 Vyhľadávanie</a>
            <a href="/ai-chat" class="nav-link">💬 AI Asistent</a>
            <a href="/new-customer" class="nav-link">👤 Nový zákazník</a>
            <a href="/customers" class="nav-link">👥 Existujúci zákazníci</a>
            <a href="/service" class="nav-link">🔧 Servis</a>
            <a href="/training" class="nav-link">🎓 Školenia</a>
        </div>
        
        {% if success_message %}
        <div class="message success">{{ success_message }}</div>
        {% endif %}
        {% if error_message %}
        <div class="message error">{{ error_message }}</div>
        {% endif %}
        
        <div class="stats">
            <h3>📊 Prehľad databázy</h3>
            <div class="stats-numbers">
                <div class="stat-item">
                    {{ total_modules }}
                    <div class="stat-label">modulov</div>
                </div>
                <div class="stat-item">
                    {{ total_functionalities }}
                    <div class="stat-label">funkcionalít</div>
                </div>
            </div>
            <div style="margin-top: 15px;">
                <a href="/wiki/admin" style="color: white; background: rgba(255,255,255,0.2); padding: 8px 20px; border-radius: 20px; text-decoration: none; font-weight: 600;">🛠️ Správa modulov (admin)</a>
            </div>
        </div>

        {% if modules %}
            <div class="modules-list">
            {% for module in modules %}
            <div class="module-item">
                <div class="module-name" onclick="toggleModuleDetail(this, 'module_{{ module.id }}')">
                    <span class="module-arrow">▶</span>
                    <span class="module-icon">📦</span>
                    <span class="module-title-text">{{ module.name }}</span>
                    {% if module.submodules %}
                    <span class="module-badge">{{ module.submodules|length }} podmodulov</span>
                    {% endif %}
                </div>
                <div class="module-detail collapsed" id="module_{{ module.id }}">
                    <div class="module-card">
                        <div class="module-description">
                            {{ module.description }}
                        </div>
                        <div class="admin-card" style="margin-left: 50px;">
                            <h3>✏️ Upraviť modul</h3>
                            <form method="post">
                                <input type="hidden" name="action" value="update_module">
                                <input type="hidden" name="module_id" value="{{ module.id }}">
                                <label>Názov</label>
                                <input name="name" value="{{ module.name }}" required>
                                <label>Popis</label>
                                <textarea name="description" id="editModuleDesc_{{ module.id }}" rows="3">{{ module.description }}</textarea>
                                <div class="voice-controls">
                                    <button type="button" class="voice-btn record" onclick="startRecording('editModuleDesc_{{ module.id }}')">🎙️ Nahrať</button>
                                    <button type="button" class="voice-btn stop" id="stop_editModuleDesc_{{ module.id }}" onclick="stopRecording('editModuleDesc_{{ module.id }}')" style="display:none;">⏹ Stop</button>
                                    <span class="voice-status" id="status_editModuleDesc_{{ module.id }}"></span>
                                </div>
                                <button type="submit">Uložiť zmeny</button>
                            </form>
                        </div>
                {% if module.functionalities %}
                <div class="functionalities">
                    <h3>⚙️ Funkcionality ({{ module.functionalities|length }})</h3>
                    {% for func in module.functionalities %}
                    <div class="functionality-item">
                        <div class="functionality-name">{{ func.name }}</div>
                        <div class="functionality-description">{{ func.description }}</div>
                    </div>
                    {% endfor %}
                </div>
                {% endif %}
                {% if module.relationships %}
                <div class="relationships">
                    <h3>🔗 Súvislosti</h3>
                    {% for rel in module.relationships %}
                    <div class="relationship-item">
                        {{ rel.relationship_type }} → {{ rel.to_module_name }}
                        {% if rel.description %}
                        <div style="color:#b2bec3;">{{ rel.description }}</div>
                        {% endif %}
                    </div>
                    {% endfor %}
                </div>
                {% endif %}
                {% if module.submodules %}
                <div class="submodules">
                    <div class="submodules-header" onclick="toggleSubmodules(this, 'submodules_{{ module.id }}')">
                        <button type="button" class="toggle-btn collapsed" id="btn_{{ module.id }}">+</button>
                        <h3 style="margin: 0;">🧩 Podmoduly ({{ module.submodules|length }})</h3>
                    </div>
                    <div class="submodules-content collapsed" id="submodules_{{ module.id }}">
                    {% for sub in module.submodules %}
                    <div class="submodule-item">
                        <div class="submodule-name" onclick="toggleSubmoduleDetail(this, 'subdetail_{{ sub.id }}')">
                            <span class="submodule-arrow">▶</span>
                            <span>🧩 {{ sub.name }}</span>
                        </div>
                        <div class="submodule-detail collapsed" id="subdetail_{{ sub.id }}">
                            <div class="submodule-card">
                                <div class="module-description">{{ sub.description }}</div>
                                <div class="admin-card">
                                    <h3>✏️ Upraviť podmodul</h3>
                                    <form method="post">
                                        <input type="hidden" name="action" value="update_module">
                                        <input type="hidden" name="module_id" value="{{ sub.id }}">
                                        <label>Názov</label>
                                        <input name="name" value="{{ sub.name }}" required>
                                        <label>Popis</label>
                                        <textarea name="description" id="editSubDesc_{{ sub.id }}" rows="3">{{ sub.description }}</textarea>
                                        <div class="voice-controls">
                                            <button type="button" class="voice-btn record" onclick="startRecording('editSubDesc_{{ sub.id }}')">🎙️ Nahrať</button>
                                            <button type="button" class="voice-btn stop" id="stop_editSubDesc_{{ sub.id }}" onclick="stopRecording('editSubDesc_{{ sub.id }}')" style="display:none;">⏹ Stop</button>
                                            <span class="voice-status" id="status_editSubDesc_{{ sub.id }}"></span>
                                        </div>
                                        <button type="submit">Uložiť zmeny</button>
                                    </form>
                                </div>
                                {% if sub.functionalities %}
                                <div class="functionalities">
                                    <h3>⚙️ Funkcionality ({{ sub.functionalities|length }})</h3>
                                    {% for func in sub.functionalities %}
                                    <div class="functionality-item">
                                        <div class="functionality-name">{{ func.name }}</div>
                                        <div class="functionality-description">{{ func.description }}</div>
                                    </div>
                                    {% endfor %}
                                </div>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                    </div>
                </div>
                {% endif %}
                    </div>
                </div>
            </div>
            {% endfor %}
            </div>
        {% else %}
            <div class="no-data">
                Žiadne moduly v databáze.
            </div>
        {% endif %}
    </div>
    <script>
        function toggleModuleDetail(nameEl, detailId) {
            const detail = document.getElementById(detailId);
            const arrow = nameEl.querySelector('.module-arrow');
            
            if (detail.classList.contains('collapsed')) {
                detail.classList.remove('collapsed');
                detail.classList.add('expanded');
                arrow.classList.add('expanded');
                arrow.textContent = '▼';
            } else {
                detail.classList.remove('expanded');
                detail.classList.add('collapsed');
                arrow.classList.remove('expanded');
                arrow.textContent = '▶';
            }
        }
        
        function toggleSubmodules(header, contentId) {
            const content = document.getElementById(contentId);
            const btn = header.querySelector('.toggle-btn');
            
            if (content.classList.contains('collapsed')) {
                content.classList.remove('collapsed');
                content.classList.add('expanded');
                btn.classList.remove('collapsed');
                btn.classList.add('expanded');
                btn.textContent = '−';
            } else {
                content.classList.remove('expanded');
                content.classList.add('collapsed');
                btn.classList.remove('expanded');
                btn.classList.add('collapsed');
                btn.textContent = '+';
            }
        }
        
        function toggleSubmoduleDetail(nameEl, detailId) {
            const detail = document.getElementById(detailId);
            const arrow = nameEl.querySelector('.submodule-arrow');
            
            // Zatvor ostatne otvorene podmoduly v rovnakom module
            const parent = nameEl.closest('.submodules-content');
            const allDetails = parent.querySelectorAll('.submodule-detail.expanded');
            const allArrows = parent.querySelectorAll('.submodule-arrow.expanded');
            
            allDetails.forEach(d => {
                if (d.id !== detailId) {
                    d.classList.remove('expanded');
                    d.classList.add('collapsed');
                }
            });
            allArrows.forEach(a => {
                if (a !== arrow) {
                    a.classList.remove('expanded');
                    a.textContent = '▶';
                }
            });
            
            // Toggle aktualny
            if (detail.classList.contains('collapsed')) {
                detail.classList.remove('collapsed');
                detail.classList.add('expanded');
                arrow.classList.add('expanded');
                arrow.textContent = '▼';
            } else {
                detail.classList.remove('expanded');
                detail.classList.add('collapsed');
                arrow.classList.remove('expanded');
                arrow.textContent = '▶';
            }
        }
        
        // Hlasové nahrávanie pomocou Web Speech API
        let recognition = null;
        let currentTextareaId = null;
        
        function startRecording(textareaId) {
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
                alert('Váš prehliadač nepodporuje hlasové nahrávanie. Použite Chrome alebo Edge.');
                return;
            }
            
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            recognition.lang = 'sk-SK';
            recognition.continuous = true;
            recognition.interimResults = true;
            
            currentTextareaId = textareaId;
            const textarea = document.getElementById(textareaId);
            const stopBtn = document.getElementById('stop_' + textareaId);
            const status = document.getElementById('status_' + textareaId);
            const recordBtn = event.target;
            
            recordBtn.style.display = 'none';
            stopBtn.style.display = 'inline-block';
            status.textContent = '🔴 Nahrávam...';
            status.classList.add('recording');
            
            let finalTranscript = textarea.value;
            if (finalTranscript && !finalTranscript.endsWith(' ')) {
                finalTranscript += ' ';
            }
            
            recognition.onresult = function(event) {
                let interimTranscript = '';
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    if (event.results[i].isFinal) {
                        finalTranscript += event.results[i][0].transcript + ' ';
                    } else {
                        interimTranscript += event.results[i][0].transcript;
                    }
                }
                textarea.value = finalTranscript + interimTranscript;
            };
            
            recognition.onerror = function(event) {
                console.error('Speech recognition error:', event.error);
                status.textContent = 'Chyba: ' + event.error;
                status.classList.remove('recording');
            };
            
            recognition.onend = function() {
                recordBtn.style.display = 'inline-block';
                stopBtn.style.display = 'none';
                status.textContent = '✓ Hotovo';
                status.classList.remove('recording');
                textarea.value = finalTranscript.trim();
            };
            
            recognition.start();
        }
        
        function stopRecording(textareaId) {
            if (recognition) {
                recognition.stop();
                recognition = null;
            }
        }
    </script>
</body>
</html>
'''

# HTML šablóna pre Wiki Admin - Správa modulov
WIKI_ADMIN_HTML = '''
<!doctype html>
<html lang="sk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IS-Assistant | Správa modulov</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2d3436 0%, #636e72 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            background: #1e272e;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            padding: 40px;
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: #74b9ff;
            margin-bottom: 30px;
            text-align: center;
            font-size: 2.5em;
        }
        .nav-links {
            margin-bottom: 30px;
            text-align: center;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 15px;
        }
        .nav-link {
            color: #74b9ff;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s;
        }
        .nav-link:hover {
            color: #81ecec;
        }
        .admin-panel {
            background: #1e272e;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
        }
        .admin-panel h2 {
            color: #81ecec;
            margin-bottom: 15px;
        }
        .admin-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }
        .admin-card {
            background: #2d3436;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #636e72;
        }
        .admin-card h3 {
            color: #74b9ff;
            margin-bottom: 15px;
        }
        .admin-card label {
            display: block;
            font-size: 0.9em;
            margin-bottom: 6px;
            color: #b2bec3;
        }
        .admin-card input, .admin-card select, .admin-card textarea {
            width: 100%;
            padding: 10px;
            border: 2px solid #636e72;
            border-radius: 8px;
            font-size: 14px;
            background: #1e272e;
            color: #dfe6e9;
            margin-bottom: 12px;
        }
        .admin-card input:focus, .admin-card select:focus, .admin-card textarea:focus {
            outline: none;
            border-color: #74b9ff;
        }
        .admin-card button {
            width: 100%;
            padding: 10px;
            background: linear-gradient(135deg, #0984e3 0%, #74b9ff 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .admin-card button:hover {
            transform: translateY(-2px);
        }
        .admin-note {
            margin-top: 10px;
            font-size: 0.9em;
            color: #b2bec3;
            text-align: center;
            margin-bottom: 20px;
        }
        .message {
            padding: 12px 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .message.success {
            background: #00b894;
            color: white;
            border: 1px solid #00cec9;
        }
        .message.error {
            background: #d63031;
            color: white;
            border: 1px solid #ff7675;
        }
        .voice-controls {
            display: flex;
            gap: 8px;
            align-items: center;
            margin-bottom: 12px;
            flex-wrap: wrap;
        }
        .voice-btn {
            padding: 6px 12px;
            border: none;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            font-size: 0.85em;
            transition: all 0.2s;
        }
        .voice-btn.record {
            background: #ef5350;
            color: white;
        }
        .voice-btn.record:hover {
            background: #d32f2f;
        }
        .voice-btn.stop {
            background: #ff9800;
            color: white;
        }
        .voice-btn.stop:hover {
            background: #f57c00;
        }
        .voice-status {
            font-size: 0.8em;
            color: #b2bec3;
            padding: 4px 8px;
            background: #2d3436;
            border-radius: 4px;
        }
        .voice-status.recording {
            background: #d63031;
            color: white;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .stats {
            background: linear-gradient(135deg, #0984e3 0%, #74b9ff 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 30px;
            text-align: center;
        }
        .stats h3 {
            font-size: 1.1em;
            margin-bottom: 10px;
        }
        .stats-numbers {
            display: flex;
            justify-content: center;
            gap: 40px;
            flex-wrap: wrap;
        }
        .stat-item {
            font-size: 1.5em;
            font-weight: 600;
        }
        .stat-label {
            font-size: 0.7em;
            opacity: 0.9;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛠️ Správa modulov</h1>
        <div class="nav-links">
            <a href="/" class="nav-link">🔍 Vyhľadávanie</a>
            <a href="/wiki" class="nav-link">📚 Wiki</a>
            <a href="/ai-chat" class="nav-link">💬 AI Asistent</a>
            <a href="/new-customer" class="nav-link">👤 Nový zákazník</a>
            <a href="/customers" class="nav-link">👥 Existujúci zákazníci</a>
            <a href="/service" class="nav-link">🔧 Servis</a>
            <a href="/training" class="nav-link">🎓 Školenia</a>
        </div>
        
        {% if success_message %}
        <div class="message success">{{ success_message }}</div>
        {% endif %}
        {% if error_message %}
        <div class="message error">{{ error_message }}</div>
        {% endif %}
        
        <div class="stats">
            <h3>📊 Prehľad databázy</h3>
            <div class="stats-numbers">
                <div class="stat-item">
                    {{ total_modules }}
                    <div class="stat-label">modulov</div>
                </div>
                <div class="stat-item">
                    {{ total_functionalities }}
                    <div class="stat-label">funkcionalít</div>
                </div>
            </div>
        </div>
        
        <div class="admin-note">📌 Táto sekcia je dostupná len pre administrátorov.</div>

        <div class="admin-panel">
            <div class="admin-grid">
                <div class="admin-card">
                    <h3>➕ Nový modul</h3>
                    <form method="post">
                        <input type="hidden" name="action" value="add_module">
                        <label>Názov modulu</label>
                        <input name="name" required>
                        <label>Popis</label>
                        <textarea name="description" id="moduleDesc" rows="3"></textarea>
                        <div class="voice-controls">
                            <button type="button" class="voice-btn record" onclick="startRecording('moduleDesc')">🎙️ Nahrať</button>
                            <button type="button" class="voice-btn stop" id="stop_moduleDesc" onclick="stopRecording('moduleDesc')" style="display:none;">⏹ Stop</button>
                            <span class="voice-status" id="status_moduleDesc"></span>
                        </div>
                        <button type="submit">Pridať modul</button>
                    </form>
                </div>
                <div class="admin-card">
                    <h3>🧩 Nový podmodul</h3>
                    <form method="post">
                        <input type="hidden" name="action" value="add_submodule">
                        <label>Rodičovský modul</label>
                        <select name="parent_module_id" required>
                            <option value="">-- vyber modul --</option>
                            {% for m in all_modules if not m.parent_module_id %}
                            <option value="{{ m.id }}">{{ m.name }}</option>
                            {% endfor %}
                        </select>
                        <label>Názov podmodulu</label>
                        <input name="name" required>
                        <label>Popis</label>
                        <textarea name="description" id="submoduleDesc" rows="3"></textarea>
                        <div class="voice-controls">
                            <button type="button" class="voice-btn record" onclick="startRecording('submoduleDesc')">🎙️ Nahrať</button>
                            <button type="button" class="voice-btn stop" id="stop_submoduleDesc" onclick="stopRecording('submoduleDesc')" style="display:none;">⏹ Stop</button>
                            <span class="voice-status" id="status_submoduleDesc"></span>
                        </div>
                        <button type="submit">Pridať podmodul</button>
                    </form>
                </div>
                <div class="admin-card">
                    <h3>⚙️ Nová funkcionalita</h3>
                    <form method="post">
                        <input type="hidden" name="action" value="add_functionality">
                        <label>Modul / Podmodul</label>
                        <select name="module_id" required>
                            <option value="">-- vyber --</option>
                            {% for m in all_modules %}
                            <option value="{{ m.id }}">{{ m.name }}{% if m.parent_module_id %} (podmodul){% endif %}</option>
                            {% endfor %}
                        </select>
                        <label>Názov funkcionality</label>
                        <input name="name" required>
                        <label>Popis</label>
                        <textarea name="description" id="funcDesc" rows="3"></textarea>
                        <div class="voice-controls">
                            <button type="button" class="voice-btn record" onclick="startRecording('funcDesc')">🎙️ Nahrať</button>
                            <button type="button" class="voice-btn stop" id="stop_funcDesc" onclick="stopRecording('funcDesc')" style="display:none;">⏹ Stop</button>
                            <span class="voice-status" id="status_funcDesc"></span>
                        </div>
                        <button type="submit">Pridať funkcionalitu</button>
                    </form>
                </div>
                <div class="admin-card">
                    <h3>🔗 Nová súvislosť</h3>
                    <form method="post">
                        <input type="hidden" name="action" value="add_relationship">
                        <label>Od modulu</label>
                        <select name="module_from_id" required>
                            <option value="">-- vyber modul --</option>
                            {% for m in all_modules %}
                            <option value="{{ m.id }}">{{ m.name }}</option>
                            {% endfor %}
                        </select>
                        <label>Na modul</label>
                        <select name="module_to_id" required>
                            <option value="">-- vyber modul --</option>
                            {% for m in all_modules %}
                            <option value="{{ m.id }}">{{ m.name }}</option>
                            {% endfor %}
                        </select>
                        <label>Typ súvislosti</label>
                        <input name="relationship_type" placeholder="napr. závisí od">
                        <label>Popis</label>
                        <textarea name="description" id="relDesc" rows="3"></textarea>
                        <div class="voice-controls">
                            <button type="button" class="voice-btn record" onclick="startRecording('relDesc')">🎙️ Nahrať</button>
                            <button type="button" class="voice-btn stop" id="stop_relDesc" onclick="stopRecording('relDesc')" style="display:none;">⏹ Stop</button>
                            <span class="voice-status" id="status_relDesc"></span>
                        </div>
                        <button type="submit">Pridať súvislosť</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Hlasové nahrávanie pomocou Web Speech API
        let recognition = null;
        let currentTextareaId = null;
        
        function startRecording(textareaId) {
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
                alert('Váš prehliadač nepodporuje hlasové nahrávanie. Použite Chrome alebo Edge.');
                return;
            }
            
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            recognition.lang = 'sk-SK';
            recognition.continuous = true;
            recognition.interimResults = true;
            
            currentTextareaId = textareaId;
            const textarea = document.getElementById(textareaId);
            const stopBtn = document.getElementById('stop_' + textareaId);
            const status = document.getElementById('status_' + textareaId);
            const recordBtn = event.target;
            
            recordBtn.style.display = 'none';
            stopBtn.style.display = 'inline-block';
            status.textContent = '🔴 Nahrávam...';
            status.classList.add('recording');
            
            let finalTranscript = textarea.value;
            if (finalTranscript && !finalTranscript.endsWith(' ')) {
                finalTranscript += ' ';
            }
            
            recognition.onresult = function(event) {
                let interimTranscript = '';
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    if (event.results[i].isFinal) {
                        finalTranscript += event.results[i][0].transcript + ' ';
                    } else {
                        interimTranscript += event.results[i][0].transcript;
                    }
                }
                textarea.value = finalTranscript + interimTranscript;
            };
            
            recognition.onerror = function(event) {
                console.error('Speech recognition error:', event.error);
                status.textContent = 'Chyba: ' + event.error;
                status.classList.remove('recording');
            };
            
            recognition.onend = function() {
                recordBtn.style.display = 'inline-block';
                stopBtn.style.display = 'none';
                status.textContent = '✓ Hotovo';
                status.classList.remove('recording');
                textarea.value = finalTranscript.trim();
            };
            
            recognition.start();
        }
        
        function stopRecording(textareaId) {
            if (recognition) {
                recognition.stop();
                recognition = null;
            }
        }
    </script>
</body>
</html>
'''

# HTML šablóna pre Nový zákazník
NEW_CUSTOMER_HTML = '''
<!doctype html>
<html lang="sk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IS-Assistant | Nový zákazník</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2d3436 0%, #636e72 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            background: #1e272e;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            padding: 40px;
            max-width: 800px;
            margin: 0 auto;
        }
        h1 {
            color: #74b9ff;
            margin-bottom: 30px;
            text-align: center;
            font-size: 2em;
        }
        .nav-links {
            margin-bottom: 30px;
            text-align: center;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 15px;
        }
        .nav-link {
            color: #74b9ff;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s;
        }
        .nav-link:hover {
            color: #81ecec;
        }
        .form-step {
            margin-bottom: 25px;
            padding: 20px;
            background: #2d3436;
            border-radius: 10px;
            border-left: 4px solid #74b9ff;
        }
        .form-step.hidden {
            display: none;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            color: #b2bec3;
            font-weight: 600;
            margin-bottom: 8px;
            font-size: 1.1em;
        }
        input, select, textarea {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #636e72;
            border-radius: 10px;
            font-size: 16px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            transition: all 0.3s;
            background: #1e272e;
            color: #dfe6e9;
        }
        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: #74b9ff;
            box-shadow: 0 0 0 3px rgba(116,185,255,0.2);
        }
        button {
            padding: 14px 30px;
            background: linear-gradient(135deg, #0984e3 0%, #74b9ff 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            margin-right: 10px;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(116,185,255,0.4);
        }
        button.secondary {
            background: #636e72;
        }
        .success-message {
            margin-top: 20px;
            padding: 20px;
            background: #00b894;
            border: 1px solid #00cec9;
            border-radius: 10px;
            color: white;
        }
        .checkbox-group {
            margin: 15px 0;
        }
        .checkbox-item {
            display: flex;
            align-items: center;
            margin-bottom: 12px;
        }
        .checkbox-item input[type="checkbox"] {
            width: auto;
            margin-right: 10px;
            cursor: pointer;
        }
        .checkbox-item label {
            margin: 0;
            font-weight: normal;
            cursor: pointer;
            flex: 1;
            color: #dfe6e9;
        }
        .company-box {
            background: #353b48;
            border: 2px solid #74b9ff;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            position: relative;
        }
        .company-box h4 {
            color: #74b9ff;
            margin-bottom: 15px;
            margin-top: 0;
        }
        .remove-company {
            position: absolute;
            top: 10px;
            right: 10px;
            background: #dc3545;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 8px 12px;
            cursor: pointer;
            font-size: 0.9em;
        }
        .remove-company:hover {
            background: #c82333;
        }
        .add-company-btn {
            background: #28a745;
            margin: 20px 0;
        }
        .add-company-btn:hover {
            background: #218838;
        }
        .section-title {
            font-size: 1.2em;
            color: #74b9ff;
            font-weight: 600;
            margin-top: 30px;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #74b9ff;
        }
        h2 {
            color: #81ecec;
        }
        p {
            color: #b2bec3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>👤 Nový zákazník</h1>
        <div class="nav-links">
            <a href="/" class="nav-link">🔍 Vyhľadávanie</a>
            <a href="/ai-chat" class="nav-link">💬 AI Asistent</a>
            <a href="/wiki" class="nav-link">📚 Wiki</a>
            <a href="/customers" class="nav-link">👥 Existujúci zákazníci</a>
            <a href="/service" class="nav-link">🔧 Servis</a>
            <a href="/training" class="nav-link">🎓 Školenia</a>
        </div>
        
        {% if success %}
        <div class="success-message">
            ✓ Zákazník bol úspešne pridaný do databázy!
        </div>
        {% endif %}
        
        <form method="post" id="customerForm">
            <!-- Počiatočný súhrn zo stretnutia -->
            <div class="form-step" id="step0">
                <h2><span class="question-number">1</span> 📝 Počiatočný súhrn zo stretnutia</h2>
                <p style="color: #b2bec3; margin-bottom: 15px;">Zadajte textový súhrn z vášho stretnutia so zákazníkom. AI ho neskôr môže spracovať a doplniť jednotlivé údaje.</p>
                <div class="form-group">
                    <label>Súhrn stretnutia *</label>
                    <textarea id="summaryTextarea" name="initial_summary" required placeholder="Napr. Stretol som sa s Jánom Novákom z ABC s.r.o. so sídlom v Bratislave. Majú reštauráciu v centre s kapacitou 80 ľudí. Zákazník chce implementovať systém na rezervácie stolkov a správu inventára..." style="min-height: 120px; resize: vertical;"></textarea>
                </div>
                
                <!-- Audio nahrávanie -->
                <div style="margin-top: 15px; padding: 15px; background: #353b48; border-radius: 8px;">
                    <h4 style="margin-top: 0; color: #81ecec;">🎙️ Alebo nahrajte zvuk:</h4>
                    <div style="display: flex; gap: 10px; flex-wrap: wrap; align-items: center;">
                        <button type="button" id="recordBtn" style="background: #ef5350; color: white; border: none; padding: 10px 15px; border-radius: 6px; cursor: pointer; font-weight: 600;">● Začať nahrávanie</button>
                        <button type="button" id="stopBtn" style="background: #ff9800; color: white; border: none; padding: 10px 15px; border-radius: 6px; cursor: pointer; font-weight: 600; display: none;">⏹ Zastaviť</button>
                        <span id="recordingTime" style="color: #b2bec3; font-weight: 600;"></span>
                    </div>
                    <input type="file" id="audioFile" accept="audio/*" style="margin-top: 10px; display: none;">
                    <button type="button" id="uploadAudioBtn" style="background: #4caf50; color: white; border: none; padding: 10px 15px; border-radius: 6px; cursor: pointer; margin-top: 10px; font-weight: 600; display: none;">🔄 Konvertovať zvuk na text</button>
                    <div id="audioStatus" style="margin-top: 10px; display: none; padding: 10px; border-radius: 6px;"></div>
                </div>
                
                <button type="button" id="parseBtn" style="background: #6c63ff; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; margin-top: 10px; font-weight: 600;">🤖 Nech AI parseuje súhrn</button>
                <div id="parseStatus" style="margin-top: 10px; display: none; padding: 10px; border-radius: 6px;"></div>
            </div>
            
            <!-- Základné informácie o kontaktnej osobe -->
            <div class="form-step" id="step1">
                <h2><span class="question-number">2</span> Základné údaje kontaktnej osoby</h2>
                <div class="form-group">
                    <label>Meno kontaktnej osoby *</label>
                    <input type="text" name="name" required placeholder="Napr. Ján Novák">
                </div>
                <div class="form-group">
                    <label>Email *</label>
                    <input type="email" name="email" placeholder="jan.novak@firma.sk">
                </div>
                <div class="form-group">
                    <label>Telefón</label>
                    <input type="tel" name="phone" placeholder="+421 xxx xxx xxx">
                </div>
            </div>
            
            <!-- Informácie o firmách -->
            <div class="form-step" id="step2">
                <h2><span class="question-number">3</span> Informácie o firme(ах)</h2>
                <div id="companiesContainer">
                    <div class="company-box" data-company="0">
                        <h4>🏢 Firma č. 1</h4>
                        <div class="form-group">
                            <label>Názov firmy *</label>
                            <input type="text" name="company_name_0" placeholder="Napr. ABC s.r.o.">
                        </div>
                        <div class="form-group">
                            <label>IČO (identifikačné číslo) *</label>
                            <input type="text" name="company_ico_0" placeholder="Napr. 12345678">
                        </div>
                    </div>
                </div>
                <button type="button" class="add-company-btn" onclick="addCompanyForm()">➕ Pridať ďalšiu firmu</button>
            </div>
            
            <!-- Pobočky -->
            <div class="form-step" id="step3">
                <h2><span class="question-number">4</span> Pobočky</h2>
                <p style="color: #666; margin-bottom: 20px;">Pobočka je konkrétne miesto kde zákazník podniká. Na pobočku sa viažu moduly systému.</p>
                <div id="branchesContainer">
                    <div class="company-box" data-branch="0">
                        <h4>📍 Pobočka č. 1</h4>
                        <div class="form-group">
                            <label>Názov pobočky *</label>
                            <input type="text" name="branch_name_0" placeholder="Napr. Reštaurácia Centrum">
                        </div>
                        <div class="form-group">
                            <label>Adresa *</label>
                            <input type="text" name="branch_address_0" placeholder="Napr. Hlavná 123, Bratislava">
                        </div>
                        <div class="form-group">
                            <label>Typ podnikania na tejto pobočke (môžete zvoliť viac) *</label>
                            <div class="checkbox-group">
                                <div class="checkbox-item">
                                    <input type="checkbox" name="branch_type_0" value="restauracia">
                                    <label>Reštaurácia / Gastronómia</label>
                                </div>
                                <div class="checkbox-item">
                                    <input type="checkbox" name="branch_type_0" value="obchod">
                                    <label>Kamenný obchod</label>
                                </div>
                                <div class="checkbox-item">
                                    <input type="checkbox" name="branch_type_0" value="eshop">
                                    <label>E-shop / Online predaj</label>
                                </div>
                                <div class="checkbox-item">
                                    <input type="checkbox" name="branch_type_0" value="sklad">
                                    <label>Sklad</label>
                                </div>
                                <div class="checkbox-item">
                                    <input type="checkbox" name="branch_type_0" value="kancelaria">
                                    <label>Kancelária / Administratíva</label>
                                </div>
                                <div class="checkbox-item">
                                    <input type="checkbox" name="branch_type_0" value="vyrobna">
                                    <label>Výrobňa</label>
                                </div>
                                <div class="checkbox-item">
                                    <input type="checkbox" name="branch_type_0" value="servis">
                                    <label>Servisné stredisko</label>
                                </div>
                                <div class="checkbox-item">
                                    <input type="checkbox" name="branch_type_0" value="eventova_agentura">
                                    <label>Eventová agentúra</label>
                                </div>
                                <div class="checkbox-item">
                                    <input type="checkbox" name="branch_type_0" value="ine">
                                    <label>Iné</label>
                                </div>
                            </div>
                        </div>
                        <div class="form-group">
                            <label>Poznámka (voliteľné)</label>
                            <textarea name="branch_info_0" rows="2" placeholder="Doplňujúce informácie..."></textarea>
                        </div>
                    </div>
                </div>
                <button type="button" class="add-company-btn" onclick="addBranchForm()">➕ Pridať ďalšiu pobočku</button>
            </div>
            
            <!-- Všeobecné požiadavky -->
            <div class="form-step" id="stepFinal">
                <h2><span class="question-number">4</span> Vaše požiadavky</h2>
                <div class="form-group">
                    <label>Čo očakávate od informačného systému?</label>
                    <textarea name="expectations" rows="5" placeholder="Popíšte, čo potrebujete..."></textarea>
                </div>
                <div class="form-group">
                    <label>Plánovaný termín nasadenia</label>
                    <input type="text" name="timeline" placeholder="Napr. Do 3 mesiacov">
                </div>
            </div>
            
            <button type="submit">💾 Uložiť zákazníka</button>
            <a href="/customers"><button type="button" class="secondary">Zrušiť</button></a>
        </form>
    </div>
    
    <script>
        // Web Speech API pre rozpoznávanie reči
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognition = null;
        let isRecording = false;
        
        if (SpeechRecognition) {
            recognition = new SpeechRecognition();
            recognition.lang = 'sk-SK';
            recognition.continuous = true;
            recognition.interimResults = true;
            
            recognition.onstart = () => {
                isRecording = true;
                showAudioStatus('Nahravanie... Hovorte.', 'info');
                document.getElementById('recordBtn').style.display = 'none';
                document.getElementById('stopBtn').style.display = 'inline-block';
            };
            
            recognition.onresult = (event) => {
                let finalTranscript = '';
                let interimTranscript = '';
                
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    if (event.results[i].isFinal) {
                        finalTranscript += event.results[i][0].transcript + ' ';
                    } else {
                        interimTranscript += event.results[i][0].transcript;
                    }
                }
                
                const textarea = document.getElementById('summaryTextarea');
                if (finalTranscript) {
                    textarea.value += finalTranscript;
                }
                
                showAudioStatus('Nahravanie... ' + (interimTranscript ? '(rozpozavam: ' + interimTranscript + ')' : ''), 'info');
            };
            
            recognition.onerror = (event) => {
                if (event.error === 'no-speech') {
                    showAudioStatus('Nepocul som nic. Skuste znova hovorit.', 'info');
                    if (isRecording) {
                        recognition.start();
                    }
                } else {
                    showAudioStatus('Chyba: ' + event.error, 'error');
                    stopRecording();
                }
            };
            
            recognition.onend = () => {
                if (isRecording) {
                    recognition.start();
                } else {
                    document.getElementById('recordBtn').style.display = 'inline-block';
                    document.getElementById('stopBtn').style.display = 'none';
                    showAudioStatus('Nahravanie ukoncene.', 'success');
                }
            };
        }
        
        function stopRecording() {
            isRecording = false;
            if (recognition) {
                recognition.stop();
            }
            document.getElementById('recordBtn').style.display = 'inline-block';
            document.getElementById('stopBtn').style.display = 'none';
        }
        
        function showAudioStatus(message, type) {
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
                showAudioStatus('Tvoj prehliadac nepodporuje rozpoznavanie reci. Skuste Chrome, Edge alebo Firefox.', 'error');
                return;
            }
            recognition.start();
        });
        
        document.getElementById('stopBtn').addEventListener('click', function() {
            stopRecording();
        });
        
        // Inicializacia - skry stopBtn
        document.getElementById('stopBtn').style.display = 'none';
        
        let companyCount = 1;
        
        function addCompanyForm() {
            const container = document.getElementById('companiesContainer');
            const newCompanyBox = document.createElement('div');
            newCompanyBox.className = 'company-box';
            newCompanyBox.setAttribute('data-company', companyCount);
            const html = '<button type="button" class="remove-company" onclick="removeCompanyForm(' + companyCount + ')">X Odstranit</button>' +
                '<h4>Firma c. ' + (companyCount + 1) + '</h4>' +
                '<div class="form-group">' +
                '<label>Nazov firmy *</label>' +
                '<input type="text" name="company_name_' + companyCount + '" placeholder="Napr. ABC s.r.o.">' +
                '</div>' +
                '<div class="form-group">' +
                '<label>ICO (identifikacne cislo) *</label>' +
                '<input type="text" name="company_ico_' + companyCount + '" placeholder="Napr. 12345678">' +
                '</div>';
            newCompanyBox.innerHTML = html;
            container.appendChild(newCompanyBox);
            companyCount++;
        }
        
        function removeCompanyForm(companyNum) {
            const box = document.querySelector('[data-company="' + companyNum + '"]');
            if (box) {
                box.remove();
            }
        }
        
        // Funkcie pre pobočky
        let branchCount = 1;
        
        function addBranchForm() {
            const container = document.getElementById('branchesContainer');
            const newBranchBox = document.createElement('div');
            newBranchBox.className = 'company-box';
            newBranchBox.setAttribute('data-branch', branchCount);
            const html = '<button type="button" class="remove-company" onclick="removeBranchForm(' + branchCount + ')">X Odstranit</button>' +
                '<h4>Pobocka c. ' + (branchCount + 1) + '</h4>' +
                '<div class="form-group">' +
                '<label>Nazov pobocky *</label>' +
                '<input type="text" name="branch_name_' + branchCount + '" placeholder="Napr. Restauracia Centrum">' +
                '</div>' +
                '<div class="form-group">' +
                '<label>Adresa *</label>' +
                '<input type="text" name="branch_address_' + branchCount + '" placeholder="Napr. Hlavna 123, Bratislava">' +
                '</div>' +
                '<div class="form-group">' +
                '<label>Typ podnikania na tejto pobocke (mozete zvolit viac) *</label>' +
                '<div class="checkbox-group">' +
                '<div class="checkbox-item"><input type="checkbox" name="branch_type_' + branchCount + '" value="restauracia"><label>Restauracia / Gastronomia</label></div>' +
                '<div class="checkbox-item"><input type="checkbox" name="branch_type_' + branchCount + '" value="obchod"><label>Kamenny obchod</label></div>' +
                '<div class="checkbox-item"><input type="checkbox" name="branch_type_' + branchCount + '" value="eshop"><label>E-shop / Online predaj</label></div>' +
                '<div class="checkbox-item"><input type="checkbox" name="branch_type_' + branchCount + '" value="sklad"><label>Sklad</label></div>' +
                '<div class="checkbox-item"><input type="checkbox" name="branch_type_' + branchCount + '" value="kancelaria"><label>Kancelaria / Administrativa</label></div>' +
                '<div class="checkbox-item"><input type="checkbox" name="branch_type_' + branchCount + '" value="vyrobna"><label>Vyrobna</label></div>' +
                '<div class="checkbox-item"><input type="checkbox" name="branch_type_' + branchCount + '" value="servis"><label>Servisne stredisko</label></div>' +
                '<div class="checkbox-item"><input type="checkbox" name="branch_type_' + branchCount + '" value="eventova_agentura"><label>Eventova agentura</label></div>' +
                '<div class="checkbox-item"><input type="checkbox" name="branch_type_' + branchCount + '" value="ine"><label>Ine</label></div>' +
                '</div>' +
                '</div>' +
                '<div class="form-group">' +
                '<label>Poznamka (volitelne)</label>' +
                '<textarea name="branch_info_' + branchCount + '" rows="2" placeholder="Doplnujuce informacie..."></textarea>' +
                '</div>';
            newBranchBox.innerHTML = html;
            container.appendChild(newBranchBox);
            branchCount++;
        }
        
        function removeBranchForm(branchNum) {
            const box = document.querySelector('[data-branch="' + branchNum + '"]');
            if (box) {
                box.remove();
            }
        }
        
        // AI Parsing suhrnu
        document.getElementById('parseBtn').addEventListener('click', async function() {
            const summary = document.getElementById('summaryTextarea').value.trim();
            if (!summary) {
                showParseStatus('Zadajte suhrn pred parseovanim', 'error');
                return;
            }
            
            const parseBtn = document.getElementById('parseBtn');
            parseBtn.disabled = true;
            parseBtn.textContent = 'Spracovavam...';
            showParseStatus('AI parsuje vas suhrn...', 'info');
            
            try {
                const response = await fetch('/ai-parse-summary', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({summary: summary})
                });
                
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || 'Chyba pri parsovani');
                }
                
                // Uloz data do globalnej premennej a zobraz potvrdenie
                window.parsedData = data;
                showParsedDataConfirmation(data);
                
                showParseStatus('AI rozpoznala udaje. Skontrolujte a potvrdte.', 'info');
                
            } catch (error) {
                showParseStatus('Chyba: ' + error.message, 'error');
            } finally {
                parseBtn.disabled = false;
                parseBtn.textContent = 'Nech AI parseuje suhrn';
            }
        });
        
        // Zobraz rozpoznane udaje na potvrdenie
        function showParsedDataConfirmation(data) {
            const existingModal = document.getElementById('confirmModal');
            if (existingModal) existingModal.remove();
            
            const modal = document.createElement('div');
            modal.id = 'confirmModal';
            modal.style.cssText = 'position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center; z-index: 1000; overflow-y: auto; padding: 20px;';
            
            let content = '<div style="background: white; border-radius: 12px; padding: 25px; max-width: 600px; width: 100%; max-height: 90vh; overflow-y: auto; box-shadow: 0 10px 40px rgba(0,0,0,0.2);">';
            content += '<h3 style="color: #667eea; margin-bottom: 20px; border-bottom: 2px solid #667eea; padding-bottom: 10px;">AI rozpoznala tieto udaje:</h3>';
            
            // Kontaktna osoba
            content += '<div style="margin-bottom: 20px;">';
            content += '<h4 style="color: #333; margin-bottom: 10px;">Kontaktna osoba:</h4>';
            content += '<div style="background: #f5f5f5; padding: 15px; border-radius: 8px;">';
            content += '<div style="margin-bottom: 8px;"><strong>Meno:</strong> <input type="text" id="confirm_name" value="' + (data.contact_name || '') + '" style="width: 60%; padding: 5px; border: 1px solid #ddd; border-radius: 4px;"></div>';
            content += '<div style="margin-bottom: 8px;"><strong>Email:</strong> <input type="text" id="confirm_email" value="' + (data.contact_email || '') + '" style="width: 60%; padding: 5px; border: 1px solid #ddd; border-radius: 4px;"></div>';
            content += '<div><strong>Telefon:</strong> <input type="text" id="confirm_phone" value="' + (data.contact_phone || '') + '" style="width: 60%; padding: 5px; border: 1px solid #ddd; border-radius: 4px;"></div>';
            content += '</div></div>';
            
            // Firmy
            if (data.companies && data.companies.length > 0) {
                content += '<div style="margin-bottom: 20px;">';
                content += '<h4 style="color: #333; margin-bottom: 10px;">Firmy (' + data.companies.length + '):</h4>';
                data.companies.forEach((company, idx) => {
                    content += '<div style="background: #e8f4fd; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #667eea;">';
                    content += '<div style="margin-bottom: 8px;"><strong>Nazov:</strong> <input type="text" id="confirm_company_name_' + idx + '" value="' + (company.name || '') + '" style="width: 60%; padding: 5px; border: 1px solid #ddd; border-radius: 4px;"></div>';
                    content += '<div><strong>ICO:</strong> <input type="text" id="confirm_company_ico_' + idx + '" value="' + (company.ico || '') + '" style="width: 40%; padding: 5px; border: 1px solid #ddd; border-radius: 4px;"></div>';
                    content += '</div>';
                });
                content += '</div>';
            }
            
            // Pobocky
            if (data.branches && data.branches.length > 0) {
                content += '<div style="margin-bottom: 20px;">';
                content += '<h4 style="color: #333; margin-bottom: 10px;">Pobocky / Prevadzky (' + data.branches.length + '):</h4>';
                data.branches.forEach((branch, idx) => {
                    const addressEncoded = encodeURIComponent(branch.address || '');
                    const hasAddress = branch.address && branch.address.trim().length > 0;
                    const locationHint = branch.location_hint || '';
                    
                    content += '<div style="background: #fff3e0; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #ff9800;">';
                    content += '<div style="margin-bottom: 8px;"><strong>Nazov pobocky:</strong> <input type="text" id="confirm_branch_name_' + idx + '" value="' + (branch.name || '') + '" style="width: 60%; padding: 5px; border: 1px solid #ddd; border-radius: 4px;"></div>';
                    content += '<div style="margin-bottom: 8px;"><strong>Adresa:</strong> <input type="text" id="confirm_branch_address_' + idx + '" value="' + (branch.address || '') + '" style="width: 80%; padding: 5px; border: 1px solid #ddd; border-radius: 4px;" onchange="updateBranchMap(' + idx + ', this.value)" placeholder="' + (locationHint ? 'Hint: ' + locationHint : 'Zadajte adresu...') + '"></div>';
                    
                    // Zobraz location_hint ak nie je adresa
                    if (!hasAddress && locationHint) {
                        content += '<div style="margin-bottom: 8px; padding: 8px; background: #fff9c4; border-radius: 4px; font-size: 0.9em;"><strong>Napoveda:</strong> ' + locationHint + ' <em>(doplnte presnu adresu)</em></div>';
                    }
                    
                    // Google Maps - len ak je adresa
                    if (hasAddress) {
                        content += '<div id="map_container_' + idx + '" style="margin: 10px 0; border-radius: 8px; overflow: hidden; border: 2px solid #ddd;">';
                        content += '<iframe id="map_frame_' + idx + '" width="100%" height="200" frameborder="0" style="border:0" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q=' + addressEncoded + '&markers=color:red%7C' + addressEncoded + '&output=embed&z=15"></iframe>';
                        content += '</div>';
                    } else {
                        content += '<div id="map_container_' + idx + '" style="display: none; margin: 10px 0; border-radius: 8px; overflow: hidden; border: 2px solid #ddd;">';
                        content += '<iframe id="map_frame_' + idx + '" width="100%" height="200" frameborder="0" style="border:0" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src=""></iframe>';
                        content += '</div>';
                    }
                    
                    content += '<div><strong>Typ podnikania:</strong></div>';
                    content += '<div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 5px;">';
                    const branchTypes = branch.type ? (Array.isArray(branch.type) ? branch.type : [branch.type]) : [];
                    content += '<label style="display: flex; align-items: center; gap: 4px; font-size: 0.9em;"><input type="checkbox" name="confirm_branch_type_' + idx + '" value="restauracia"' + (branchTypes.includes('restauracia') ? ' checked' : '') + '> Restauracia</label>';
                    content += '<label style="display: flex; align-items: center; gap: 4px; font-size: 0.9em;"><input type="checkbox" name="confirm_branch_type_' + idx + '" value="obchod"' + (branchTypes.includes('obchod') ? ' checked' : '') + '> Obchod</label>';
                    content += '<label style="display: flex; align-items: center; gap: 4px; font-size: 0.9em;"><input type="checkbox" name="confirm_branch_type_' + idx + '" value="eshop"' + (branchTypes.includes('eshop') ? ' checked' : '') + '> E-shop</label>';
                    content += '<label style="display: flex; align-items: center; gap: 4px; font-size: 0.9em;"><input type="checkbox" name="confirm_branch_type_' + idx + '" value="sklad"' + (branchTypes.includes('sklad') ? ' checked' : '') + '> Sklad</label>';
                    content += '<label style="display: flex; align-items: center; gap: 4px; font-size: 0.9em;"><input type="checkbox" name="confirm_branch_type_' + idx + '" value="kancelaria"' + (branchTypes.includes('kancelaria') ? ' checked' : '') + '> Kancelaria</label>';
                    content += '<label style="display: flex; align-items: center; gap: 4px; font-size: 0.9em;"><input type="checkbox" name="confirm_branch_type_' + idx + '" value="vyrobna"' + (branchTypes.includes('vyrobna') ? ' checked' : '') + '> Vyrobna</label>';
                    content += '<label style="display: flex; align-items: center; gap: 4px; font-size: 0.9em;"><input type="checkbox" name="confirm_branch_type_' + idx + '" value="servis"' + (branchTypes.includes('servis') ? ' checked' : '') + '> Servis</label>';
                    content += '<label style="display: flex; align-items: center; gap: 4px; font-size: 0.9em;"><input type="checkbox" name="confirm_branch_type_' + idx + '" value="eventova_agentura"' + (branchTypes.includes('eventova_agentura') ? ' checked' : '') + '> Eventova agentura</label>';
                    content += '<label style="display: flex; align-items: center; gap: 4px; font-size: 0.9em;"><input type="checkbox" name="confirm_branch_type_' + idx + '" value="ine"' + (branchTypes.includes('ine') ? ' checked' : '') + '> Ine</label>';
                    content += '</div>';
                    content += '</div>';
                });
                content += '</div>';
            }
            
            // Tlacidla
            content += '<div style="display: flex; gap: 10px; margin-top: 20px;">';
            content += '<button onclick="closeConfirmModal()" style="flex: 1; padding: 12px; background: #dc3545; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: 600;">X Zrusit</button>';
            content += '<button onclick="applyParsedData()" style="flex: 1; padding: 12px; background: #28a745; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: 600;">OK Potvrdit a vyplnit</button>';
            content += '</div>';
            
            content += '</div>';
            modal.innerHTML = content;
            document.body.appendChild(modal);
        }
        
        // Aktualizuj mapu ked sa zmeni adresa
        function updateBranchMap(idx, address) {
            const mapContainer = document.getElementById('map_container_' + idx);
            const mapFrame = document.getElementById('map_frame_' + idx);
            
            if (address && address.trim().length > 0) {
                const addressEncoded = encodeURIComponent(address);
                mapFrame.src = 'https://maps.google.com/maps?q=' + addressEncoded + '&markers=color:red%7C' + addressEncoded + '&output=embed&z=15';
                mapContainer.style.display = 'block';
            } else {
                mapContainer.style.display = 'none';
                mapFrame.src = '';
            }
        }
        
        function closeConfirmModal() {
            const modal = document.getElementById('confirmModal');
            if (modal) modal.remove();
            showParseStatus('Zrusene. Mozete upravit suhrn a skusit znova.', 'info');
        }
        
        function applyParsedData() {
            const data = window.parsedData;
            if (!data) return;
            
            // Nacitaj upravene hodnoty z modalneho okna
            const confirmedName = document.getElementById('confirm_name').value;
            const confirmedEmail = document.getElementById('confirm_email').value;
            const confirmedPhone = document.getElementById('confirm_phone').value;
            
            // Vyplň kontaktne údaje
            if (confirmedName) document.querySelector('input[name="name"]').value = confirmedName;
            if (confirmedEmail) document.querySelector('input[name="email"]').value = confirmedEmail;
            if (confirmedPhone) document.querySelector('input[name="phone"]').value = confirmedPhone;
            
            // Vyplň firmy
            if (data.companies && data.companies.length > 0) {
                const companiesContainer = document.getElementById('companiesContainer');
                
                for (let i = 0; i < data.companies.length; i++) {
                    if (i > 0) addCompanyForm();
                    const confirmedCompanyName = document.getElementById('confirm_company_name_' + i).value;
                    const confirmedCompanyIco = document.getElementById('confirm_company_ico_' + i).value;
                    
                    const nameInput = companiesContainer.querySelector('input[name="company_name_' + i + '"]');
                    const icoInput = companiesContainer.querySelector('input[name="company_ico_' + i + '"]');
                    if (nameInput) nameInput.value = confirmedCompanyName;
                    if (icoInput) icoInput.value = confirmedCompanyIco;
                }
            }
            
            // Vyplň pobocky
            if (data.branches && data.branches.length > 0) {
                const branchesContainer = document.getElementById('branchesContainer');
                
                for (let i = 0; i < data.branches.length; i++) {
                    if (i > 0) addBranchForm();
                    const confirmedBranchName = document.getElementById('confirm_branch_name_' + i).value;
                    const confirmedBranchAddress = document.getElementById('confirm_branch_address_' + i).value;
                    
                    // Ziskaj zaskrtnute checkboxy
                    const confirmedTypes = [];
                    document.querySelectorAll('input[name="confirm_branch_type_' + i + '"]:checked').forEach(cb => {
                        confirmedTypes.push(cb.value);
                    });
                    
                    const nameInput = branchesContainer.querySelector('input[name="branch_name_' + i + '"]');
                    const addressInput = branchesContainer.querySelector('input[name="branch_address_' + i + '"]');
                    
                    if (nameInput) nameInput.value = confirmedBranchName;
                    if (addressInput) addressInput.value = confirmedBranchAddress;
                    
                    // Zaskrtni checkboxy v hlavnom formulari
                    confirmedTypes.forEach(typeVal => {
                        const checkbox = branchesContainer.querySelector('input[name="branch_type_' + i + '"][value="' + typeVal + '"]');
                        if (checkbox) checkbox.checked = true;
                    });
                }
            }
            
            // Zatvor modal
            closeConfirmModal();
            showParseStatus('Udaje boli uspesne vyplnene!', 'success');
        }
        
        function showParseStatus(message, type) {
            const statusDiv = document.getElementById('parseStatus');
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
        
        // Zobrazenie návrhov adries
        function showAddressSuggestions(suggestions) {
            const existingModal = document.getElementById('suggestionModal');
            if (existingModal) existingModal.remove();
            
            const modal = document.createElement('div');
            modal.id = 'suggestionModal';
            modal.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0,0,0,0.5);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 1000;
            `;
            
            let content = '<div style="background: white; border-radius: 12px; padding: 25px; max-width: 500px; box-shadow: 0 10px 40px rgba(0,0,0,0.2);">';
            content += '<h3 style="color: #667eea; margin-bottom: 15px;">Navrhy adries:</h3>';
            content += '<p style="color: #666; margin-bottom: 15px;">AI nasla mozne adresy na zaklade mestnosti. Potvrdit?</p>';
            
            suggestions.forEach((sugg, idx) => {
                content += '<div style="background: #f5f5f5; padding: 12px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #667eea;">';
                content += '<div style="font-weight: 600; color: #333;">' + sugg.name + '</div>';
                content += '<div style="color: #666; font-size: 0.9em; margin-top: 5px;">Adresa: ' + sugg.address + '</div>';
                content += '</div>';
            });
            
            content += '<div style="display: flex; gap: 10px; margin-top: 20px;">';
            content += '<button onclick="closeModal()" style="flex: 1; padding: 10px; background: #dc3545; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: 600;">X Zmenit rucne</button>';
            content += '<button onclick="confirmAddressSuggestions()" style="flex: 1; padding: 10px; background: #28a745; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: 600;">OK Ano potvrzujem</button>';
            content += '</div>';
            
            content += '</div>';
            modal.innerHTML = content;
            
            // Uloz navrhy do global premennej
            window.pendingSuggestions = suggestions;
            
            document.body.appendChild(modal);
        }
        
        function closeModal() {
            const modal = document.getElementById('suggestionModal');
            if (modal) modal.remove();
        }
        
        function confirmAddressSuggestions() {
            if (!window.pendingSuggestions) return;
            
            const branchesContainer = document.getElementById('branchesContainer');
            window.pendingSuggestions.forEach(sugg => {
                branchesContainer.querySelector(`input[name="branch_address_${sugg.index}"]`).value = sugg.address;
            });
            
            document.getElementById('suggestionModal').remove();
            showParseStatus('Adresy boli potvrdene!', 'success');
        }
    </script>
</body>
</html>
'''

# HTML šablóna pre Existujúcich zákazníkov
CUSTOMERS_HTML = '''
<!doctype html>
<html lang="sk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IS-Assistant | Existujúci zákazníci</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2d3436 0%, #636e72 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            background: #1e272e;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            padding: 40px;
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: #74b9ff;
            margin-bottom: 30px;
            text-align: center;
            font-size: 2.5em;
        }
        .nav-links {
            margin-bottom: 30px;
            text-align: center;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 15px;
        }
        .nav-link {
            color: #74b9ff;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s;
        }
        .nav-link:hover {
            color: #81ecec;
        }
        .add-button {
            display: inline-block;
            padding: 12px 24px;
            background: linear-gradient(135deg, #0984e3 0%, #74b9ff 100%);
            color: white;
            text-decoration: none;
            border-radius: 10px;
            font-weight: 600;
            transition: transform 0.2s, box-shadow 0.2s;
            margin-bottom: 30px;
        }
        .add-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(116,185,255,0.4);
        }
        .customer-card {
            background: linear-gradient(135deg, #2d3436 0%, #353b48 100%);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            border-left: 5px solid #74b9ff;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .customer-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.4);
        }
        .customer-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .customer-name {
            color: #74b9ff;
            font-size: 1.5em;
            font-weight: 600;
        }
        .customer-type {
            background: #81ecec;
            color: #1e272e;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
        }
        .customer-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 15px;
        }
        .info-item {
            color: #b2bec3;
        }
        .info-label {
            font-weight: 600;
            color: #dfe6e9;
            display: block;
            margin-bottom: 5px;
        }
        .customer-date {
            color: #636e72;
            font-size: 0.9em;
            margin-top: 10px;
        }
        .no-customers {
            text-align: center;
            padding: 60px 20px;
            color: #636e72;
        }
        .no-customers-icon {
            font-size: 4em;
            margin-bottom: 20px;
        }
        .company-items {
            background: #2d3436;
            border-radius: 10px;
            padding: 15px;
            margin-top: 10px;
        }
        .company-item {
            background: #353b48;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 10px;
            border-left: 3px solid #74b9ff;
        }
        .company-item:last-child {
            margin-bottom: 0;
        }
        .company-name {
            font-weight: 600;
            color: #dfe6e9;
            margin-bottom: 5px;
        }
        .company-ico {
            color: #b2bec3;
            font-size: 0.9em;
            margin-bottom: 8px;
        }
        .business-types {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
        }
        .business-tag {
            background: #74b9ff;
            color: #1e272e;
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 0.8em;
        }
        .stats {
            background: linear-gradient(135deg, #0984e3 0%, #74b9ff 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 30px;
            text-align: center;
        }
        .stats-number {
            font-size: 2.5em;
            font-weight: 600;
        }
        .customer-actions {
            display: flex;
            gap: 10px;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #636e72;
        }
        .action-btn {
            padding: 8px 16px;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            font-size: 0.9em;
            text-decoration: none;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 5px;
        }
        .action-btn.edit {
            background: linear-gradient(135deg, #0984e3 0%, #74b9ff 100%);
            color: white;
        }
        .action-btn.edit:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(116,185,255,0.4);
        }
        .action-btn.delete {
            background: linear-gradient(135deg, #d63031 0%, #ff7675 100%);
            color: white;
        }
        .action-btn.delete:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(214,48,49,0.4);
        }
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.7);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }
        .modal.active {
            display: flex;
        }
        .modal-content {
            background: #1e272e;
            border-radius: 15px;
            padding: 30px;
            max-width: 500px;
            width: 90%;
            text-align: center;
        }
        .modal-title {
            color: #dfe6e9;
            margin-bottom: 20px;
            font-size: 1.3em;
        }
        .modal-buttons {
            display: flex;
            gap: 15px;
            justify-content: center;
            margin-top: 20px;
        }
        .modal-btn {
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            font-size: 1em;
        }
        .modal-btn.cancel {
            background: #636e72;
            color: white;
        }
        .modal-btn.confirm {
            background: #d63031;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>👥 Existujúci zákazníci</h1>
        <div class="nav-links">
            <a href="/" class="nav-link">🔍 Vyhľadávanie</a>
            <a href="/ai-chat" class="nav-link">💬 AI Asistent</a>
            <a href="/wiki" class="nav-link">📚 Wiki</a>
            <a href="/new-customer" class="nav-link">👤 Nový zákazník</a>
            <a href="/service" class="nav-link">🔧 Servis</a>
            <a href="/training" class="nav-link">🎓 Školenia</a>
        </div>
        
        <div style="text-align: center;">
            <a href="/new-customer" class="add-button">➕ Pridať nového zákazníka</a>
        </div>
        
        <div class="stats">
            <div class="stats-number">{{ customers|length }}</div>
            <div>celkový počet zákazníkov</div>
        </div>
        
        {% if customers %}
            {% for customer in customers %}
            <div class="customer-card">
                <div class="customer-header">
                    <div class="customer-name">👤 {{ customer.name }}</div>
                </div>
                <div class="customer-info">
                    {% if customer.contact_email %}
                    <div class="info-item">
                        <span class="info-label">📧 Email:</span>
                        {{ customer.contact_email }}
                    </div>
                    {% endif %}
                    {% if customer.contact_phone %}
                    <div class="info-item">
                        <span class="info-label">📱 Telefón:</span>
                        {{ customer.contact_phone }}
                    </div>
                    {% endif %}
                </div>
                
                <!-- Počiatočný súhrn -->
                {% if customer.initial_summary %}
                <div style="background: linear-gradient(135deg, #2d3436 0%, #353b48 100%); padding: 12px; border-radius: 8px; margin-top: 12px; border-left: 4px solid #ff9800;">
                    <h4 style="color: #ffd93d; margin-top: 0; margin-bottom: 8px; font-size: 0.95em;">📝 Súhrn zo stretnutia:</h4>
                    <p style="margin: 0; color: #dfe6e9; font-size: 0.9em; line-height: 1.4;">{{ customer.initial_summary }}</p>
                </div>
                {% endif %}
                
                <div class="customer-info">
                </div>
                
                <!-- Firmy zákazníka -->
                {% if customer.companies %}
                <div class="company-items">
                    <h3 style="color: #667eea; margin-bottom: 10px; font-size: 1em;">🏢 Firmy:</h3>
                    {% for company in customer.companies %}
                    <div class="company-item">
                        <div class="company-name">{{ company.name }}</div>
                        <div class="company-ico">IČO: {{ company.ico }}</div>
                    </div>
                    {% endfor %}
                </div>
                {% elif customer.company_name %}
                <div class="company-items">
                    <h3 style="color: #667eea; margin-bottom: 10px; font-size: 1em;">🏢 Firma:</h3>
                    <div class="company-item">
                        <div class="company-name">{{ customer.company_name }}</div>
                    </div>
                </div>
                {% endif %}
                
                <!-- Pobočky zákazníka -->
                {% if customer.branches %}
                <div class="company-items" style="margin-top: 15px;">
                    <h3 style="color: #74b9ff; margin-bottom: 10px; font-size: 1em;">🏪 Pobočky:</h3>
                    {% for branch in customer.branches %}
                    <div class="company-item" style="background: linear-gradient(135deg, #353b48 0%, #2d3436 100%); border-left: 4px solid #74b9ff;">
                        <div class="company-name" style="font-size: 1em; color: #dfe6e9;">{{ branch.name }}</div>
                        <div class="company-ico" style="color: #b2bec3;">📍 {{ branch.address }}</div>
                        <div class="business-types" style="margin-top: 5px;">
                            <span class="business-tag" style="background: #74b9ff; color: #1e272e;">{{ branch.branch_type }}</span>
                        </div>
                        {% if branch.additional_info %}
                        <div style="margin-top: 8px; padding: 8px; background: rgba(0,0,0,0.2); border-radius: 4px; font-size: 0.85em; color: #b2bec3;">
                            💡 {{ branch.additional_info }}
                        </div>
                        {% endif %}
                    </div>
                    {% endfor %}
                </div>
                {% endif %}
                
                <div class="customer-date">
                    📅 Vytvorené: {{ customer.created_at }}
                </div>
                
                <div class="customer-actions">
                    <a href="/customer/{{ customer.id }}/edit" class="action-btn edit">✏️ Upraviť</a>
                    <button class="action-btn delete" onclick="confirmDelete({{ customer.id }}, '{{ customer.name }}')">🗑️ Zmazať</button>
                </div>
            </div>
            {% endfor %}
        {% else %}
            <div class="no-customers">
                <div class="no-customers-icon">👤</div>
                <h2 style="color: #dfe6e9;">Zatiaľ žiadni zákazníci</h2>
                <p style="margin-top: 10px; color: #b2bec3;">Začnite pridaním prvého zákazníka</p>
            </div>
        {% endif %}
    </div>
    
    <!-- Modal pre potvrdenie zmazania -->
    <div class="modal" id="deleteModal">
        <div class="modal-content">
            <h2 class="modal-title">🗑️ Zmazať zákazníka?</h2>
            <p style="color: #b2bec3;" id="deleteMessage">Ste si istí, že chcete zmazať tohto zákazníka?</p>
            <div class="modal-buttons">
                <button class="modal-btn cancel" onclick="closeDeleteModal()">Zrušiť</button>
                <form id="deleteForm" method="POST" style="display: inline;">
                    <button type="submit" class="modal-btn confirm">Zmazať</button>
                </form>
            </div>
        </div>
    </div>
    
    <script>
        function confirmDelete(customerId, customerName) {
            document.getElementById('deleteMessage').textContent = 
                'Ste si istí, že chcete zmazať zákazníka "' + customerName + '"? Táto akcia je nevratná.';
            document.getElementById('deleteForm').action = '/customer/' + customerId + '/delete';
            document.getElementById('deleteModal').classList.add('active');
        }
        
        function closeDeleteModal() {
            document.getElementById('deleteModal').classList.remove('active');
        }
        
        // Zatvor modal kliknutím mimo
        document.getElementById('deleteModal').onclick = function(e) {
            if (e.target === this) closeDeleteModal();
        }
    </script>
</body>
</html>
'''

# HTML šablóna pre editáciu zákazníka
CUSTOMER_EDIT_HTML = '''
<!doctype html>
<html lang="sk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IS-Assistant | Upraviť zákazníka</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2d3436 0%, #636e72 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            background: #1e272e;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            padding: 40px;
            max-width: 900px;
            margin: 0 auto;
        }
        h1 {
            color: #74b9ff;
            margin-bottom: 30px;
            text-align: center;
            font-size: 2em;
        }
        .nav-links {
            margin-bottom: 30px;
            text-align: center;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 15px;
        }
        .nav-link {
            color: #74b9ff;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s;
        }
        .nav-link:hover {
            color: #81ecec;
        }
        .form-section {
            background: #2d3436;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 20px;
            border-left: 4px solid #74b9ff;
        }
        .form-section h2 {
            color: #81ecec;
            margin-bottom: 20px;
            font-size: 1.3em;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            color: #b2bec3;
            font-weight: 600;
            margin-bottom: 8px;
        }
        input, textarea, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #636e72;
            border-radius: 8px;
            font-size: 1em;
            background: #1e272e;
            color: #dfe6e9;
            font-family: inherit;
        }
        input:focus, textarea:focus, select:focus {
            outline: none;
            border-color: #74b9ff;
        }
        .company-box, .branch-box {
            background: #353b48;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            border-left: 4px solid #74b9ff;
            position: relative;
        }
        .branch-box {
            border-left-color: #81ecec;
        }
        .company-box h3, .branch-box h3 {
            color: #81ecec;
            margin-bottom: 15px;
            font-size: 1.1em;
        }
        .remove-btn {
            position: absolute;
            top: 10px;
            right: 10px;
            background: #d63031;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 5px 10px;
            cursor: pointer;
            font-size: 0.85em;
        }
        .remove-btn:hover {
            background: #c0392b;
        }
        .add-btn {
            background: #00b894;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            margin-top: 10px;
        }
        .add-btn:hover {
            background: #00a383;
        }
        .checkbox-group {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 10px;
        }
        .checkbox-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .checkbox-item input[type="checkbox"] {
            width: auto;
            cursor: pointer;
        }
        .checkbox-item label {
            margin: 0;
            font-weight: normal;
            cursor: pointer;
            color: #dfe6e9;
        }
        .button-group {
            display: flex;
            gap: 15px;
            margin-top: 30px;
        }
        button {
            padding: 14px 30px;
            border: none;
            border-radius: 10px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
        }
        .btn-save {
            background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
            color: white;
            flex: 1;
        }
        .btn-cancel {
            background: #636e72;
            color: white;
        }
        .message {
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .message.success {
            background: #00b894;
            color: white;
        }
        .message.error {
            background: #d63031;
            color: white;
        }
        .row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        @media (max-width: 600px) {
            .row { grid-template-columns: 1fr; }
            .checkbox-group { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>✏️ Upraviť zákazníka</h1>
        <div class="nav-links">
            <a href="/customers" class="nav-link">← Späť na zákazníkov</a>
        </div>
        
        {% if success_message %}
        <div class="message success">{{ success_message }}</div>
        {% endif %}
        {% if error_message %}
        <div class="message error">{{ error_message }}</div>
        {% endif %}
        
        <form method="POST">
            <!-- Kontaktné údaje -->
            <div class="form-section">
                <h2>👤 Kontaktné údaje</h2>
                <div class="form-group">
                    <label>Meno kontaktnej osoby *</label>
                    <input type="text" name="name" value="{{ customer.name }}" required>
                </div>
                <div class="row">
                    <div class="form-group">
                        <label>Email</label>
                        <input type="email" name="email" value="{{ customer.contact_email or '' }}">
                    </div>
                    <div class="form-group">
                        <label>Telefón</label>
                        <input type="tel" name="phone" value="{{ customer.contact_phone or '' }}">
                    </div>
                </div>
            </div>
            
            <!-- Súhrn zo stretnutia -->
            <div class="form-section">
                <h2>📝 Súhrn zo stretnutia</h2>
                <div class="form-group">
                    <textarea name="initial_summary" rows="5" placeholder="Poznámky zo stretnutia so zákazníkom...">{{ customer.initial_summary or '' }}</textarea>
                </div>
            </div>
            
            <!-- Firmy -->
            <div class="form-section">
                <h2>🏢 Firmy</h2>
                <div id="companiesContainer">
                    {% for company in companies %}
                    <div class="company-box" data-company-index="{{ loop.index0 }}">
                        <button type="button" class="remove-btn" onclick="removeCompany(this)">✕ Odstrániť</button>
                        <h3>🏢 Firma č. {{ loop.index }}</h3>
                        <div class="row">
                            <div class="form-group">
                                <label>Názov firmy</label>
                                <input type="text" name="company_name_{{ loop.index0 }}" value="{{ company.name or '' }}">
                            </div>
                            <div class="form-group">
                                <label>IČO</label>
                                <input type="text" name="company_ico_{{ loop.index0 }}" value="{{ company.ico or '' }}">
                            </div>
                        </div>
                    </div>
                    {% else %}
                    <div class="company-box" data-company-index="0">
                        <h3>🏢 Firma č. 1</h3>
                        <div class="row">
                            <div class="form-group">
                                <label>Názov firmy</label>
                                <input type="text" name="company_name_0" value="{{ customer.company_name or '' }}">
                            </div>
                            <div class="form-group">
                                <label>IČO</label>
                                <input type="text" name="company_ico_0" value="">
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                <button type="button" class="add-btn" onclick="addCompany()">➕ Pridať ďalšiu firmu</button>
            </div>
            
            <!-- Pobočky -->
            <div class="form-section">
                <h2>🏪 Pobočky</h2>
                <div id="branchesContainer">
                    {% for branch in branches %}
                    <div class="branch-box">
                        <h3>📍 Pobočka č. {{ loop.index }}</h3>
                        <div class="form-group">
                            <label>Názov pobočky</label>
                            <input type="text" name="branch_name_{{ branch.id }}" value="{{ branch.name }}">
                        </div>
                        <div class="form-group">
                            <label>Adresa</label>
                            <input type="text" name="branch_address_{{ branch.id }}" value="{{ branch.address or '' }}">
                        </div>
                        <div class="form-group">
                            <label>Typ podnikania</label>
                            <div class="checkbox-group">
                                {% set current_types = (branch.branch_type or '').split(',') %}
                                <div class="checkbox-item">
                                    <input type="checkbox" name="branch_type_{{ branch.id }}" value="restauracia" {{ 'checked' if 'restauracia' in current_types else '' }}>
                                    <label>Reštaurácia / Gastronómia</label>
                                </div>
                                <div class="checkbox-item">
                                    <input type="checkbox" name="branch_type_{{ branch.id }}" value="obchod" {{ 'checked' if 'obchod' in current_types else '' }}>
                                    <label>Kamenný obchod</label>
                                </div>
                                <div class="checkbox-item">
                                    <input type="checkbox" name="branch_type_{{ branch.id }}" value="eshop" {{ 'checked' if 'eshop' in current_types else '' }}>
                                    <label>E-shop / Online predaj</label>
                                </div>
                                <div class="checkbox-item">
                                    <input type="checkbox" name="branch_type_{{ branch.id }}" value="sklad" {{ 'checked' if 'sklad' in current_types else '' }}>
                                    <label>Sklad</label>
                                </div>
                                <div class="checkbox-item">
                                    <input type="checkbox" name="branch_type_{{ branch.id }}" value="kancelaria" {{ 'checked' if 'kancelaria' in current_types else '' }}>
                                    <label>Kancelária / Administratíva</label>
                                </div>
                                <div class="checkbox-item">
                                    <input type="checkbox" name="branch_type_{{ branch.id }}" value="vyrobna" {{ 'checked' if 'vyrobna' in current_types else '' }}>
                                    <label>Výrobňa</label>
                                </div>
                                <div class="checkbox-item">
                                    <input type="checkbox" name="branch_type_{{ branch.id }}" value="servis" {{ 'checked' if 'servis' in current_types else '' }}>
                                    <label>Servisné stredisko</label>
                                </div>
                                <div class="checkbox-item">
                                    <input type="checkbox" name="branch_type_{{ branch.id }}" value="eventova_agentura" {{ 'checked' if 'eventova_agentura' in current_types else '' }}>
                                    <label>Eventová agentúra</label>
                                </div>
                                <div class="checkbox-item">
                                    <input type="checkbox" name="branch_type_{{ branch.id }}" value="ine" {{ 'checked' if 'ine' in current_types else '' }}>
                                    <label>Iné</label>
                                </div>
                            </div>
                        </div>
                        <div class="form-group">
                            <label>Poznámka</label>
                            <textarea name="branch_info_{{ branch.id }}" rows="2">{{ branch.additional_info or '' }}</textarea>
                        </div>
                        <input type="hidden" name="branch_ids" value="{{ branch.id }}">
                    </div>
                    {% else %}
                    <p id="noBranchesMsg" style="color: #b2bec3; padding: 10px;">Zatiaľ nie sú pridané žiadne pobočky.</p>
                    {% endfor %}
                </div>
                <button type="button" class="add-btn" onclick="addBranch()">➕ Pridať pobočku</button>
            </div>
            
            <!-- Požiadavky a termín -->
            <div class="form-section">
                <h2>📋 Požiadavky</h2>
                <div class="form-group">
                    <label>Čo zákazník očakáva od informačného systému?</label>
                    <textarea name="expectations" rows="4" placeholder="Popíšte požiadavky zákazníka...">{{ expectations or '' }}</textarea>
                </div>
                <div class="form-group">
                    <label>Plánovaný termín nasadenia</label>
                    <input type="text" name="timeline" value="{{ timeline or '' }}" placeholder="Napr. Do 3 mesiacov">
                </div>
            </div>
            
            <div class="button-group">
                <a href="/customers" style="text-decoration: none;">
                    <button type="button" class="btn-cancel">Zrušiť</button>
                </a>
                <button type="submit" class="btn-save">💾 Uložiť zmeny</button>
            </div>
        </form>
    </div>
    
    <script>
        let companyCount = {{ companies|length if companies else 1 }};
        
        function addCompany() {
            const container = document.getElementById('companiesContainer');
            const newBox = document.createElement('div');
            newBox.className = 'company-box';
            newBox.setAttribute('data-company-index', companyCount);
            newBox.innerHTML = `
                <button type="button" class="remove-btn" onclick="removeCompany(this)">✕ Odstrániť</button>
                <h3>🏢 Firma č. ${companyCount + 1}</h3>
                <div class="row">
                    <div class="form-group">
                        <label>Názov firmy</label>
                        <input type="text" name="company_name_${companyCount}" placeholder="Napr. ABC s.r.o.">
                    </div>
                    <div class="form-group">
                        <label>IČO</label>
                        <input type="text" name="company_ico_${companyCount}" placeholder="Napr. 12345678">
                    </div>
                </div>
            `;
            container.appendChild(newBox);
            companyCount++;
        }
        
        function removeCompany(btn) {
            const box = btn.closest('.company-box');
            if (document.querySelectorAll('.company-box').length > 1) {
                box.remove();
                renumberCompanies();
            } else {
                alert('Musí zostať aspoň jedna firma.');
            }
        }
        
        function renumberCompanies() {
            const boxes = document.querySelectorAll('.company-box');
            boxes.forEach((box, index) => {
                box.querySelector('h3').textContent = `🏢 Firma č. ${index + 1}`;
            });
        }
        
        // Pobočky - pridávanie nových
        let newBranchCount = 0;
        
        function addBranch() {
            const container = document.getElementById('branchesContainer');
            
            // Skry správu "Zatiaľ nie sú pridané žiadne pobočky"
            const noMsg = document.getElementById('noBranchesMsg');
            if (noMsg) noMsg.style.display = 'none';
            
            const newBox = document.createElement('div');
            newBox.className = 'branch-box';
            newBox.innerHTML = `
                <button type="button" class="remove-btn" onclick="removeBranch(this)">✕ Odstrániť</button>
                <h3>📍 Nová pobočka</h3>
                <div class="form-group">
                    <label>Názov pobočky</label>
                    <input type="text" name="new_branch_name_${newBranchCount}" placeholder="Napr. Reštaurácia Centrum">
                </div>
                <div class="form-group">
                    <label>Adresa</label>
                    <input type="text" name="new_branch_address_${newBranchCount}" placeholder="Napr. Hlavná 123, Bratislava">
                </div>
                <div class="form-group">
                    <label>Typ podnikania</label>
                    <div class="checkbox-group">
                        <div class="checkbox-item">
                            <input type="checkbox" name="new_branch_type_${newBranchCount}" value="restauracia">
                            <label>Reštaurácia / Gastronómia</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" name="new_branch_type_${newBranchCount}" value="obchod">
                            <label>Kamenný obchod</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" name="new_branch_type_${newBranchCount}" value="eshop">
                            <label>E-shop / Online predaj</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" name="new_branch_type_${newBranchCount}" value="sklad">
                            <label>Sklad</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" name="new_branch_type_${newBranchCount}" value="kancelaria">
                            <label>Kancelária / Administratíva</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" name="new_branch_type_${newBranchCount}" value="vyrobna">
                            <label>Výrobňa</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" name="new_branch_type_${newBranchCount}" value="servis">
                            <label>Servisné stredisko</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" name="new_branch_type_${newBranchCount}" value="eventova_agentura">
                            <label>Eventová agentúra</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" name="new_branch_type_${newBranchCount}" value="ine">
                            <label>Iné</label>
                        </div>
                    </div>
                </div>
                <div class="form-group">
                    <label>Poznámka</label>
                    <textarea name="new_branch_info_${newBranchCount}" rows="2" placeholder="Doplňujúce informácie..."></textarea>
                </div>
                <input type="hidden" name="new_branch_ids" value="${newBranchCount}">
            `;
            container.appendChild(newBox);
            newBranchCount++;
        }
        
        function removeBranch(btn) {
            const box = btn.closest('.branch-box');
            box.remove();
        }
    </script>
</body>
</html>
'''

# HTML šablóna pre SERVIS - prípadové štúdie
SERVICE_HTML = '''
<!doctype html>
<html lang="sk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IS-Assistant | Servis</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2d3436 0%, #636e72 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            background: #1e272e;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            padding: 40px;
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 { color: #74b9ff; margin-bottom: 10px; text-align: center; font-size: 2.5em; }
        .subtitle { text-align: center; color: #b2bec3; margin-bottom: 30px; }
        .nav-links {
            margin-bottom: 30px; text-align: center;
            display: flex; flex-wrap: wrap; justify-content: center; gap: 15px;
        }
        .nav-link { color: #74b9ff; text-decoration: none; font-weight: 600; transition: color 0.3s; }
        .nav-link:hover { color: #81ecec; }
        
        .case-list { margin-top: 20px; }
        .case-item {
            display: flex; align-items: center; gap: 15px;
            padding: 20px; margin-bottom: 10px;
            background: linear-gradient(135deg, #2d3436 0%, #353b48 100%);
            border-radius: 12px; border-left: 5px solid #74b9ff;
            cursor: pointer; transition: all 0.3s;
        }
        .case-item:hover { transform: translateX(10px); box-shadow: 0 5px 20px rgba(0,0,0,0.3); }
        .case-icon { font-size: 2em; }
        .case-info { flex: 1; }
        .case-title { font-size: 1.2em; font-weight: 600; color: #dfe6e9; }
        .case-desc { color: #b2bec3; font-size: 0.95em; margin-top: 5px; }
        .case-meta { display: flex; gap: 15px; margin-top: 8px; font-size: 0.85em; color: #636e72; }
        .case-arrow { color: #74b9ff; font-size: 1.5em; }
        
        .add-btn {
            display: inline-flex; align-items: center; gap: 8px;
            padding: 12px 25px; background: linear-gradient(135deg, #0984e3 0%, #74b9ff 100%);
            color: white; border: none; border-radius: 25px;
            font-weight: 600; cursor: pointer; transition: all 0.3s;
            text-decoration: none; margin-bottom: 20px;
        }
        .add-btn:hover { transform: scale(1.05); box-shadow: 0 5px 20px rgba(116,185,255,0.4); }
        
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                 background: rgba(0,0,0,0.7); z-index: 1000; align-items: center; justify-content: center; }
        .modal.active { display: flex; }
        .modal-content {
            background: #1e272e; border-radius: 15px; padding: 30px;
            max-width: 600px; width: 90%; max-height: 80vh; overflow-y: auto;
        }
        .modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .modal-title { font-size: 1.4em; color: #74b9ff; }
        .close-btn { background: none; border: none; font-size: 1.5em; cursor: pointer; color: #636e72; }
        .close-btn:hover { color: #dfe6e9; }
        
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; font-weight: 600; margin-bottom: 5px; color: #b2bec3; }
        .form-group input, .form-group textarea, .form-group select {
            width: 100%; padding: 12px; border: 2px solid #636e72; border-radius: 8px; font-size: 1em;
            background: #2d3436; color: #dfe6e9;
        }
        .form-group input:focus, .form-group textarea:focus, .form-group select:focus { border-color: #74b9ff; outline: none; }
        .submit-btn {
            width: 100%; padding: 15px; background: linear-gradient(135deg, #0984e3 0%, #74b9ff 100%);
            color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;
        }
        
        .no-cases { text-align: center; padding: 60px 20px; color: #636e72; }
        .no-cases-icon { font-size: 4em; margin-bottom: 20px; }
        .no-cases h2 { color: #dfe6e9; }
        .no-cases p { color: #b2bec3; }
        
        .search-box {
            display: flex; gap: 10px; margin-bottom: 25px;
            background: linear-gradient(135deg, #2d3436 0%, #353b48 100%);
            padding: 15px; border-radius: 15px;
        }
        .search-input {
            flex: 1; padding: 12px 20px; border: 2px solid #636e72;
            border-radius: 25px; font-size: 1em; outline: none;
            background: #1e272e; color: #dfe6e9;
        }
        .search-input:focus { border-color: #74b9ff; }
        .search-input::placeholder { color: #636e72; }
        .search-btn {
            padding: 12px 25px; background: linear-gradient(135deg, #0984e3 0%, #74b9ff 100%);
            color: white; border: none; border-radius: 25px;
            font-weight: 600; cursor: pointer; transition: all 0.3s;
        }
        .search-btn:hover { transform: scale(1.05); }
        .clear-btn {
            padding: 12px 20px; background: #636e72; color: white;
            border: none; border-radius: 25px; cursor: pointer;
            text-decoration: none; font-weight: 600;
        }
        .search-results {
            background: #2d3436; padding: 10px 20px; border-radius: 10px;
            margin-bottom: 20px; color: #74b9ff; border-left: 4px solid #74b9ff;
        }
        .highlight { background: #ffd93d; padding: 0 3px; border-radius: 3px; color: #1e272e; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔧 Servis</h1>
        <p class="subtitle">Prípadové štúdie a návody na riešenie technických problémov</p>
        
        <div class="nav-links">
            <a href="/" class="nav-link">🔍 Vyhľadávanie</a>
            <a href="/wiki" class="nav-link">📚 Wiki</a>
            <a href="/ai-chat" class="nav-link">💬 AI Asistent</a>
            <a href="/new-customer" class="nav-link">👤 Nový zákazník</a>
            <a href="/customers" class="nav-link">👥 Zákazníci</a>
        </div>
        
        <form class="search-box" method="GET" action="/service">
            <input type="text" name="q" class="search-input" 
                   placeholder="🔍 Hľadať v prípadových štúdiách (napr. VAROS, certifikát, eKasa...)"
                   value="{{ search_query or '' }}">
            <button type="submit" class="search-btn">Hľadať</button>
            {% if search_query %}
            <a href="/service" class="clear-btn">✕ Zrušiť</a>
            {% endif %}
        </form>
        
        {% if search_query %}
        <div class="search-results">
            🔍 Výsledky pre "<strong>{{ search_query }}</strong>": nájdených <strong>{{ cases|length }}</strong> prípadových štúdií
        </div>
        {% endif %}
        
        <button class="add-btn" onclick="openModal()">➕ Nová prípadová štúdia</button>
        
        <div class="case-list">
            {% if cases %}
                {% for case in cases %}
                <a href="/service/{{ case.id }}" style="text-decoration: none;">
                    <div class="case-item">
                        <div class="case-icon">📋</div>
                        <div class="case-info">
                            <div class="case-title">{{ case.title }}</div>
                            <div class="case-desc">{{ case.description[:100] }}{% if case.description|length > 100 %}...{% endif %}</div>
                            <div class="case-meta">
                                <span>📁 {{ case.category or 'Bez kategórie' }}</span>
                                <span>📅 {{ case.created_at[:10] }}</span>
                                <span>📝 {{ case.steps_count }} krokov</span>
                            </div>
                        </div>
                        <div class="case-arrow">→</div>
                    </div>
                </a>
                {% endfor %}
            {% else %}
                <div class="no-cases">
                    <div class="no-cases-icon">📋</div>
                    <h2>Zatiaľ žiadne prípadové štúdie</h2>
                    <p>Začnite pridaním prvej prípadovej štúdie</p>
                </div>
            {% endif %}
        </div>
    </div>
    
    <div class="modal" id="addModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 class="modal-title">➕ Nová prípadová štúdia</h2>
                <button class="close-btn" onclick="closeModal()">&times;</button>
            </div>
            <form method="POST" action="/service/add">
                <div class="form-group">
                    <label>Názov</label>
                    <input type="text" name="title" required placeholder="Napr. Inštalácia certifikátov do fCHDU VAROS">
                </div>
                <div class="form-group">
                    <label>Kategória</label>
                    <select name="category">
                        <option value="Fiškálne zariadenia">Fiškálne zariadenia</option>
                        <option value="Software">Software</option>
                        <option value="Hardware">Hardware</option>
                        <option value="Sieť">Sieť</option>
                        <option value="Iné">Iné</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Popis</label>
                    <textarea name="description" rows="4" placeholder="Stručný popis problému alebo úlohy..."></textarea>
                </div>
                <button type="submit" class="submit-btn">Vytvoriť</button>
            </form>
        </div>
    </div>
    
    <script>
        function openModal() { document.getElementById('addModal').classList.add('active'); }
        function closeModal() { document.getElementById('addModal').classList.remove('active'); }
        document.getElementById('addModal').onclick = function(e) { if (e.target === this) closeModal(); }
    </script>
</body>
</html>
'''

# HTML šablóna pre detail prípadovej štúdie
SERVICE_DETAIL_HTML = '''
<!doctype html>
<html lang="sk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IS-Assistant | {{ case.title }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2d3436 0%, #636e72 100%);
            min-height: 100vh; padding: 20px;
        }
        .container {
            background: #1e272e; border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            padding: 40px; max-width: 1000px; margin: 0 auto;
        }
        .back-link { color: #74b9ff; text-decoration: none; font-weight: 600; display: inline-flex; align-items: center; gap: 5px; margin-bottom: 20px; }
        .back-link:hover { color: #81ecec; }
        h1 { color: #74b9ff; margin-bottom: 10px; font-size: 2em; }
        .case-meta { color: #b2bec3; margin-bottom: 30px; display: flex; gap: 20px; flex-wrap: wrap; }
        .case-desc { background: #2d3436; padding: 20px; border-radius: 10px; margin-bottom: 30px; line-height: 1.6; color: #dfe6e9; }
        
        .section-title { color: #74b9ff; font-size: 1.4em; margin: 30px 0 20px; display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
        
        .steps-list { margin-bottom: 30px; }
        .step-item {
            background: linear-gradient(135deg, #2d3436 0%, #353b48 100%);
            border-radius: 12px; padding: 20px; margin-bottom: 15px;
            border-left: 5px solid #00b894;
            transition: all 0.3s;
        }
        .step-item.decision {
            border-left-color: #74b9ff;
            background: linear-gradient(135deg, #1e3a5f 0%, #2d3436 100%);
        }
        .step-item.branched {
            margin-left: 30px;
            opacity: 0;
            max-height: 0;
            overflow: hidden;
            margin-bottom: 0;
            padding: 0;
            transition: all 0.4s ease-out;
        }
        .step-item.branched.visible {
            opacity: 1;
            max-height: 1000px;
            padding: 20px;
            margin-bottom: 15px;
        }
        .step-header { display: flex; align-items: center; gap: 15px; margin-bottom: 10px; }
        .step-number {
            width: 35px; height: 35px; background: #00b894; color: white;
            border-radius: 50%; display: flex; align-items: center; justify-content: center;
            font-weight: bold; font-size: 1.1em;
        }
        .step-item.decision .step-number { background: #74b9ff; }
        .step-title { font-weight: 600; font-size: 1.1em; color: #dfe6e9; flex: 1; }
        .step-desc { color: #b2bec3; line-height: 1.6; margin-left: 50px; }
        .step-image { margin-top: 15px; margin-left: 50px; }
        .step-image img { max-width: 100%; border-radius: 8px; box-shadow: 0 3px 15px rgba(0,0,0,0.3); }
        
        /* Vetvenie - výber možností */
        .branch-selector {
            margin: 15px 0 15px 50px;
            padding: 15px;
            background: #2d3436;
            border-radius: 10px;
            border: 2px solid #74b9ff;
        }
        .branch-selector-title {
            font-weight: 600;
            color: #74b9ff;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .branch-options {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        .branch-option {
            padding: 12px 20px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
            border: 3px solid transparent;
        }
        .branch-option:hover {
            transform: scale(1.05);
        }
        .branch-option.selected {
            border-color: #333;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .branch-indicator {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.75em;
            font-weight: 600;
            margin-left: 10px;
        }
        
        .complications-section { background: #3d3d00; border-radius: 12px; padding: 25px; border-left: 5px solid #ffd93d; }
        .complication-group { margin-bottom: 20px; }
        .complication-group-title { font-weight: 600; color: #ffd93d; margin-bottom: 10px; display: flex; align-items: center; gap: 8px; }
        .branched-comp { opacity: 0.7; transition: opacity 0.3s; }
        .branched-comp.highlight { opacity: 1; }
        .complication-item { background: #2d3436; border-radius: 8px; padding: 15px; margin-top: 15px; }
        .complication-title { font-weight: 600; color: #ffd93d; margin-bottom: 10px; }
        .complication-desc { color: #b2bec3; margin-bottom: 10px; }
        .complication-solution { background: #1e4620; padding: 12px; border-radius: 6px; color: #81ecec; }
        .complication-solution strong { display: block; margin-bottom: 5px; color: #00b894; }
        
        .add-btn {
            display: inline-flex; align-items: center; gap: 8px;
            padding: 10px 20px; background: linear-gradient(135deg, #0984e3 0%, #74b9ff 100%);
            color: white; border: none; border-radius: 20px;
            font-weight: 600; cursor: pointer; text-decoration: none; font-size: 0.9em;
        }
        .add-btn:hover { transform: scale(1.05); }
        .add-btn.warning { background: linear-gradient(135deg, #ffd93d 0%, #ff9800 100%); color: #1e272e; }
        .add-btn.success { background: linear-gradient(135deg, #00b894 0%, #00cec9 100%); }
        .add-btn.info { background: linear-gradient(135deg, #0984e3 0%, #74b9ff 100%); }
        
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                 background: rgba(0,0,0,0.7); z-index: 1000; align-items: center; justify-content: center; }
        .modal.active { display: flex; }
        .modal-content {
            background: #1e272e; border-radius: 15px; padding: 30px;
            max-width: 600px; width: 90%; max-height: 80vh; overflow-y: auto;
        }
        .modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .modal-title { font-size: 1.3em; color: #74b9ff; }
        .close-btn { background: none; border: none; font-size: 1.5em; cursor: pointer; color: #636e72; }
        .close-btn:hover { color: #dfe6e9; }
        
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; font-weight: 600; margin-bottom: 5px; color: #b2bec3; }
        .form-group input, .form-group textarea, .form-group select { width: 100%; padding: 12px; border: 2px solid #636e72; border-radius: 8px; background: #2d3436; color: #dfe6e9; }
        .form-group input:focus, .form-group textarea:focus, .form-group select:focus { border-color: #74b9ff; outline: none; }
        .form-group.checkbox-group { display: flex; align-items: center; gap: 10px; }
        .form-group.checkbox-group input { width: auto; }
        .form-group.checkbox-group label { color: #dfe6e9; }
        .submit-btn {
            width: 100%; padding: 15px; background: linear-gradient(135deg, #0984e3 0%, #74b9ff 100%);
            color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;
        }
        
        .no-items { text-align: center; padding: 30px; color: #636e72; font-style: italic; }
        
        .color-picker { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 8px; }
        .color-option {
            width: 30px; height: 30px; border-radius: 50%; cursor: pointer;
            border: 3px solid transparent; transition: all 0.2s;
        }
        .color-option:hover, .color-option.selected { border-color: #333; transform: scale(1.1); }
        
        .step-actions {
            display: flex; gap: 5px; margin-left: 10px;
        }
        .step-action-btn {
            padding: 5px 10px; border: none; border-radius: 5px;
            cursor: pointer; font-size: 0.8em; transition: all 0.2s;
            opacity: 0.7;
        }
        .step-action-btn:hover { opacity: 1; transform: scale(1.1); }
        .step-action-btn.edit { background: #17a2b8; color: white; }
        .step-action-btn.delete { background: #dc3545; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <a href="/service" class="back-link">← Späť na zoznam</a>
        
        <h1>{{ case.title }}</h1>
        <div class="case-meta">
            <span>📁 {{ case.category or 'Bez kategórie' }}</span>
            <span>📅 Vytvorené: {{ case.created_at[:10] }}</span>
        </div>
        
        {% if case.description %}
        <div class="case-desc">{{ case.description }}</div>
        {% endif %}
        
        <div class="section-title">
            📋 Postup krok za krokom
            <button class="add-btn success" onclick="openStepModal()">➕ Pridať krok</button>
            <button class="add-btn info" onclick="openDecisionModal()">🔀 Pridať rozhodnutie</button>
        </div>
        
        <div class="steps-list" id="stepsList">
            {% if steps %}
                {% for step in steps %}
                {% if not step.branch_id %}
                <div class="step-item {% if step.is_decision %}decision{% endif %}" data-step-id="{{ step.id }}">
                    <div class="step-header">
                        <div class="step-number">{{ step.step_number }}</div>
                        <div class="step-title">
                            {{ step.title }}
                            {% if step.is_decision %}
                            <span class="branch-indicator" style="background: #e3f2fd; color: #007bff;">🔀 Rozhodnutie</span>
                            {% endif %}
                        </div>
                        <div class="step-actions">
                            <button class="step-action-btn edit" onclick="openEditStepModal({{ step.id }}, '{{ step.title|e }}', '{{ step.description|e }}', {{ step.is_decision }})">✏️</button>
                            <button class="step-action-btn delete" onclick="deleteStep({{ step.id }})">🗑️</button>
                        </div>
                    </div>
                    <div class="step-desc">{{ step.description }}</div>
                    {% if step.image_path %}
                    <div class="step-image">
                        <img src="/static/uploads/service/{{ step.image_path }}" alt="Obrázok ku kroku {{ step.step_number }}">
                    </div>
                    {% endif %}
                    
                    {% if step.is_decision %}
                    <div class="branch-selector">
                        <div class="branch-selector-title">🔀 Vyberte možnosť pre pokračovanie:</div>
                        <div class="branch-options">
                            {% for branch in branches if branch.parent_step_id == step.id %}
                            <div class="branch-option" 
                                 style="background: {{ branch.branch_color }}; color: white;"
                                 onclick="selectBranch({{ branch.id }}, '{{ branch.branch_color }}')"
                                 data-branch-id="{{ branch.id }}">
                                {{ branch.branch_name }}
                            </div>
                            {% endfor %}
                            <button class="add-btn" style="font-size: 0.8em; padding: 8px 15px;" onclick="openBranchModal({{ step.id }})">➕ Pridať možnosť</button>
                        </div>
                    </div>
                    {% endif %}
                </div>
                
                <!-- Kroky patriace k vetvam tohto rozhodnutia -->
                {% for branch in branches if branch.parent_step_id == step.id %}
                    {% for bstep in steps if bstep.branch_id == branch.id %}
                    <div class="step-item branched {% if bstep.is_decision %}decision{% endif %}" data-branch-id="{{ branch.id }}" style="border-left-color: {{ branch.branch_color }};">
                        <div class="step-header">
                            <div class="step-number" style="background: {{ branch.branch_color }};">{{ bstep.step_number }}</div>
                            <div class="step-title">
                                {{ bstep.title }}
                                <span class="branch-indicator" style="background: {{ branch.branch_color }}; color: white;">{{ branch.branch_name }}</span>
                                {% if bstep.is_decision %}
                                <span class="branch-indicator" style="background: #e3f2fd; color: #007bff;">🔀 Rozhodnutie</span>
                                {% endif %}
                            </div>
                            <div class="step-actions">
                                <button class="step-action-btn edit" onclick="openEditStepModal({{ bstep.id }}, '{{ bstep.title|e }}', '{{ bstep.description|e }}', {{ bstep.is_decision }})">✏️</button>
                                <button class="step-action-btn delete" onclick="deleteStep({{ bstep.id }})">🗑️</button>
                            </div>
                        </div>
                        <div class="step-desc">{{ bstep.description }}</div>
                        {% if bstep.image_path %}
                        <div class="step-image">
                            <img src="/static/uploads/service/{{ bstep.image_path }}" alt="Obrázok ku kroku {{ bstep.step_number }}">
                        </div>
                        {% endif %}
                        
                        {% if bstep.is_decision %}
                        <div class="branch-selector">
                            <div class="branch-selector-title">🔀 Vyberte možnosť pre pokračovanie:</div>
                            <div class="branch-options">
                                {% for subbranch in branches if subbranch.parent_step_id == bstep.id %}
                                <div class="branch-option" 
                                     style="background: {{ subbranch.branch_color }}; color: white;"
                                     onclick="selectBranch({{ subbranch.id }}, '{{ subbranch.branch_color }}')"
                                     data-branch-id="{{ subbranch.id }}">
                                    {{ subbranch.branch_name }}
                                </div>
                                {% endfor %}
                                <button class="add-btn" style="font-size: 0.8em; padding: 8px 15px;" onclick="openBranchModal({{ bstep.id }})">➕ Pridať možnosť</button>
                            </div>
                        </div>
                        {% endif %}
                    </div>
                    
                    <!-- Vnorené kroky pre sub-vetvy -->
                    {% if bstep.is_decision %}
                    {% for subbranch in branches if subbranch.parent_step_id == bstep.id %}
                        {% for substep in steps if substep.branch_id == subbranch.id %}
                        <div class="step-item branched" data-branch-id="{{ subbranch.id }}" style="border-left-color: {{ subbranch.branch_color }}; margin-left: 60px;">
                            <div class="step-header">
                                <div class="step-number" style="background: {{ subbranch.branch_color }};">{{ substep.step_number }}</div>
                                <div class="step-title">
                                    {{ substep.title }}
                                    <span class="branch-indicator" style="background: {{ subbranch.branch_color }}; color: white;">{{ subbranch.branch_name }}</span>
                                </div>
                            </div>
                            <div class="step-desc">{{ substep.description }}</div>
                            {% if substep.image_path %}
                            <div class="step-image">
                                <img src="/static/uploads/service/{{ substep.image_path }}" alt="Obrázok ku kroku {{ substep.step_number }}">
                            </div>
                            {% endif %}
                        </div>
                        {% endfor %}
                    {% endfor %}
                    {% endif %}
                    {% endfor %}
                {% endfor %}
                {% endif %}
                {% endfor %}
            {% else %}
                <div class="no-items">Zatiaľ žiadne kroky. Pridajte prvý krok postupu.</div>
            {% endif %}
        </div>
        
        <div class="section-title">
            ⚠️ Možné komplikácie
            <button class="add-btn warning" onclick="openCompModal()">➕ Pridať komplikáciu</button>
        </div>
        
        <div class="complications-section">
            {% set general_comps = complications|selectattr('branch_id', 'none')|list %}
            {% if general_comps %}
            <div class="complication-group">
                <div class="complication-group-title">📋 Všeobecné komplikácie</div>
                {% for comp in general_comps %}
                <div class="complication-item">
                    <div class="complication-title">{{ comp.title }}</div>
                    <div class="complication-desc">{{ comp.description }}</div>
                    {% if comp.solution %}
                    <div class="complication-solution">
                        <strong>💡 Riešenie:</strong>
                        {{ comp.solution }}
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
            {% endif %}
            
            {% for branch in branches %}
            {% set branch_comps = complications|selectattr('branch_id', 'equalto', branch.id)|list %}
            {% if branch_comps %}
            <div class="complication-group branched-comp" data-branch-id="{{ branch.id }}">
                <div class="complication-group-title" style="border-left: 4px solid {{ branch.branch_color }}; padding-left: 10px;">
                    <span class="branch-indicator" style="background: {{ branch.branch_color }}; color: white;">{{ branch.branch_name }}</span>
                    Komplikácie
                </div>
                {% for comp in branch_comps %}
                <div class="complication-item" style="border-left: 3px solid {{ branch.branch_color }};">
                    <div class="complication-title">{{ comp.title }}</div>
                    <div class="complication-desc">{{ comp.description }}</div>
                    {% if comp.solution %}
                    <div class="complication-solution">
                        <strong>💡 Riešenie:</strong>
                        {{ comp.solution }}
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
            {% endif %}
            {% endfor %}
            
            {% if not complications %}
                <div class="no-items" style="color: #856404;">Zatiaľ žiadne zaznamenané komplikácie.</div>
            {% endif %}
        </div>
    </div>
    
    <!-- Modal pre pridanie kroku -->
    <div class="modal" id="stepModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 class="modal-title">➕ Pridať krok</h2>
                <button class="close-btn" onclick="closeStepModal()">&times;</button>
            </div>
            <form method="POST" action="/service/{{ case.id }}/add-step" enctype="multipart/form-data">
                <div class="form-group">
                    <label>Patrí k vetve (voliteľné)</label>
                    <select name="branch_id" id="stepBranchSelect">
                        <option value="">-- Hlavná vetva --</option>
                        {% for branch in branches %}
                        {% if branch.parent_branch_name %}
                        <option value="{{ branch.id }}">&nbsp;&nbsp;&nbsp;└─ {{ branch.branch_name }} ({{ branch.parent_branch_name }})</option>
                        {% else %}
                        <option value="{{ branch.id }}">🔀 {{ branch.branch_name }}</option>
                        {% endif %}
                        {% endfor %}
                    </select>
                    <small style="color: #28a745; margin-top: 5px; display: block;">📌 Číslovanie sa nastaví automaticky podľa zvolenej vetvy</small>
                </div>
                <div class="form-group">
                    <label>Názov kroku</label>
                    <input type="text" name="title" required placeholder="Napr. Otvorte nastavenia zariadenia">
                </div>
                <div class="form-group">
                    <label>Popis</label>
                    <textarea name="description" rows="4" placeholder="Detailný popis čo treba urobiť..."></textarea>
                </div>
                <div class="form-group">
                    <label>Obrázok (voliteľné)</label>
                    <input type="file" name="image" accept="image/*">
                </div>
                <button type="submit" class="submit-btn">Pridať krok</button>
            </form>
        </div>
    </div>
    
    <!-- Modal pre pridanie rozhodovacieho kroku -->
    <div class="modal" id="decisionModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 class="modal-title">🔀 Pridať rozhodovací bod</h2>
                <button class="close-btn" onclick="closeDecisionModal()">&times;</button>
            </div>
            <form method="POST" action="/service/{{ case.id }}/add-decision">
                <div class="form-group">
                    <label>Patrí k vetve (voliteľné)</label>
                    <select name="branch_id">
                        <option value="">-- Hlavná vetva --</option>
                        {% for branch in branches %}
                        {% if branch.parent_branch_name %}
                        <option value="{{ branch.id }}">&nbsp;&nbsp;&nbsp;└─ {{ branch.branch_name }} ({{ branch.parent_branch_name }})</option>
                        {% else %}
                        <option value="{{ branch.id }}">🔀 {{ branch.branch_name }}</option>
                        {% endif %}
                        {% endfor %}
                    </select>
                    <small style="color: #28a745; margin-top: 5px; display: block;">📌 Číslovanie sa nastaví automaticky podľa zvolenej vetvy</small>
                </div>
                <div class="form-group">
                    <label>Otázka / Názov rozhodnutia</label>
                    <input type="text" name="title" required placeholder="Napr. Aký typ eKasy používate?">
                </div>
                <div class="form-group">
                    <label>Popis (čo má používateľ zistiť)</label>
                    <textarea name="description" rows="3" placeholder="Napr. Zistite typ eKasy podľa štítku na zariadení..."></textarea>
                </div>
                <button type="submit" class="submit-btn">Pridať rozhodnutie</button>
            </form>
        </div>
    </div>
    
    <!-- Modal pre pridanie vetvy/možnosti -->
    <div class="modal" id="branchModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 class="modal-title">➕ Pridať možnosť</h2>
                <button class="close-btn" onclick="closeBranchModal()">&times;</button>
            </div>
            <form method="POST" action="/service/{{ case.id }}/add-branch" id="branchForm">
                <input type="hidden" name="parent_step_id" id="branchParentStep">
                <div class="form-group">
                    <label>Názov možnosti</label>
                    <input type="text" name="branch_name" required placeholder="Napr. eKasa VAROS">
                </div>
                <div class="form-group">
                    <label>Farba vetvy</label>
                    <div class="color-picker">
                        <div class="color-option selected" style="background: #28a745;" onclick="selectColor(this, '#28a745')"></div>
                        <div class="color-option" style="background: #007bff;" onclick="selectColor(this, '#007bff')"></div>
                        <div class="color-option" style="background: #dc3545;" onclick="selectColor(this, '#dc3545')"></div>
                        <div class="color-option" style="background: #ffc107;" onclick="selectColor(this, '#ffc107')"></div>
                        <div class="color-option" style="background: #17a2b8;" onclick="selectColor(this, '#17a2b8')"></div>
                        <div class="color-option" style="background: #6f42c1;" onclick="selectColor(this, '#6f42c1')"></div>
                        <div class="color-option" style="background: #fd7e14;" onclick="selectColor(this, '#fd7e14')"></div>
                        <div class="color-option" style="background: #20c997;" onclick="selectColor(this, '#20c997')"></div>
                    </div>
                    <input type="hidden" name="branch_color" id="branchColor" value="#28a745">
                </div>
                <button type="submit" class="submit-btn">Pridať možnosť</button>
            </form>
        </div>
    </div>
    
    <!-- Modal pre pridanie komplikácie -->
    <div class="modal" id="compModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 class="modal-title">⚠️ Pridať komplikáciu</h2>
                <button class="close-btn" onclick="closeCompModal()">&times;</button>
            </div>
            <form method="POST" action="/service/{{ case.id }}/add-complication">
                <div class="form-group">
                    <label>Názov problému</label>
                    <input type="text" name="title" required placeholder="Napr. Certifikát sa nenačíta">
                </div>
                <div class="form-group">
                    <label>Popis problému</label>
                    <textarea name="description" rows="3" placeholder="Kedy a ako sa problém prejavuje..."></textarea>
                </div>
                <div class="form-group">
                    <label>Riešenie</label>
                    <textarea name="solution" rows="4" placeholder="Ako sa problém rieši..."></textarea>
                </div>
                <div class="form-group">
                    <label>Platí pre vetvu (voliteľné)</label>
                    <select name="branch_id">
                        <option value="">📋 Všeobecná komplikácia</option>
                        {% for branch in branches %}
                        {% if branch.parent_branch_name %}
                        <option value="{{ branch.id }}">&nbsp;&nbsp;&nbsp;└─ {{ branch.branch_name }} ({{ branch.parent_branch_name }})</option>
                        {% else %}
                        <option value="{{ branch.id }}">🔀 {{ branch.branch_name }}</option>
                        {% endif %}
                        {% endfor %}
                    </select>
                    <small style="color: #666; margin-top: 5px; display: block;">Ak je komplikácia špecifická pre určitý typ zariadenia, vyberte príslušnú vetvu.</small>
                </div>
                <button type="submit" class="submit-btn">Pridať komplikáciu</button>
            </form>
        </div>
    </div>
    
    <!-- Modal pre editáciu kroku -->
    <div class="modal" id="editStepModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 class="modal-title">✏️ Upraviť krok</h2>
                <button class="close-btn" onclick="closeEditStepModal()">&times;</button>
            </div>
            <form method="POST" action="" id="editStepForm">
                <input type="hidden" name="step_id" id="editStepId">
                <div class="form-group">
                    <label>Názov</label>
                    <input type="text" name="title" id="editStepTitle" required>
                </div>
                <div class="form-group">
                    <label>Popis</label>
                    <textarea name="description" id="editStepDesc" rows="4"></textarea>
                </div>
                <div style="display: flex; gap: 10px;">
                    <button type="submit" class="submit-btn" style="flex: 1;">💾 Uložiť zmeny</button>
                </div>
            </form>
        </div>
    </div>
    
    <script>
        let selectedBranchId = null;
        
        function openStepModal() { document.getElementById('stepModal').classList.add('active'); }
        function closeStepModal() { document.getElementById('stepModal').classList.remove('active'); }
        function openDecisionModal() { document.getElementById('decisionModal').classList.add('active'); }
        function closeDecisionModal() { document.getElementById('decisionModal').classList.remove('active'); }
        function openCompModal() { document.getElementById('compModal').classList.add('active'); }
        function closeCompModal() { document.getElementById('compModal').classList.remove('active'); }
        function openBranchModal(stepId) { 
            document.getElementById('branchParentStep').value = stepId;
            document.getElementById('branchModal').classList.add('active'); 
        }
        function closeBranchModal() { document.getElementById('branchModal').classList.remove('active'); }
        
        function selectColor(el, color) {
            document.querySelectorAll('.color-option').forEach(o => o.classList.remove('selected'));
            el.classList.add('selected');
            document.getElementById('branchColor').value = color;
        }
        
        function selectBranch(branchId, color) {
            // Odznač všetky možnosti
            document.querySelectorAll('.branch-option').forEach(o => o.classList.remove('selected'));
            // Označ vybranú
            document.querySelector('[data-branch-id="' + branchId + '"]').classList.add('selected');
            
            // Skry všetky vetvy krokov
            document.querySelectorAll('.step-item.branched').forEach(s => s.classList.remove('visible'));
            
            // Zobraz kroky patriace k vybranej vetve
            document.querySelectorAll('.step-item.branched[data-branch-id="' + branchId + '"]').forEach(s => {
                s.classList.add('visible');
            });
            
            // Zvýrazni komplikácie patriace k vybranej vetve
            document.querySelectorAll('.branched-comp').forEach(c => c.classList.remove('highlight'));
            document.querySelectorAll('.branched-comp[data-branch-id="' + branchId + '"]').forEach(c => {
                c.classList.add('highlight');
            });
            
            selectedBranchId = branchId;
        }
        
        // Editácia kroku
        function openEditStepModal(stepId, title, description, isDecision) {
            document.getElementById('editStepId').value = stepId;
            document.getElementById('editStepTitle').value = title;
            document.getElementById('editStepDesc').value = description;
            document.getElementById('editStepForm').action = '/service/{{ case.id }}/edit-step/' + stepId;
            document.querySelector('#editStepModal .modal-title').textContent = isDecision ? '✏️ Upraviť rozhodnutie' : '✏️ Upraviť krok';
            document.getElementById('editStepModal').classList.add('active');
        }
        function closeEditStepModal() { document.getElementById('editStepModal').classList.remove('active'); }
        
        // Mazanie kroku
        function deleteStep(stepId) {
            if (confirm('Naozaj chcete zmazať tento krok? Táto akcia sa nedá vrátiť späť.')) {
                window.location.href = '/service/{{ case.id }}/delete-step/' + stepId;
            }
        }
        
        // Zatvor modály kliknutím mimo
        document.querySelectorAll('.modal').forEach(m => {
            m.onclick = function(e) { if (e.target === this) this.classList.remove('active'); }
        });
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    vysledok = None
    if request.method == 'POST':
        typ = request.form['typ']
        nazov = request.form['nazov']
        if typ == 'module':
            vysledok = ai.explain_module(nazov)
        else:
            vysledok = ai.explain_functionality(nazov)
    return render_template_string(HTML, vysledok=vysledok)


    # Nová route pre AI chat

@app.route('/ai-chat', methods=['GET', 'POST'])
def ai_chat():
    odpoved = None
    otazka = None
    debug_vypis = ""  # Debug vypnutý
    otazka = None
    odpoved = None
    kontext = ""
    if request.method == 'POST':
        otazka = request.form['otazka']
        import unicodedata
        def normalize(text):
            return ''.join(c for c in unicodedata.normalize('NFD', text.lower()) if unicodedata.category(c) != 'Mn')
        otazka_norm = normalize(otazka)
        import sqlite3, os
        db_path = os.path.abspath('database/is_data.db')
        # Vyhľadáme moduly podľa výskytu kľúčových slov v názve alebo popise
        klucove_slova = [slovo for slovo in otazka_norm.split() if len(slovo) > 2]
        query = "SELECT name, description FROM modules WHERE " + " OR ".join([
            f"LOWER(name) LIKE '%{slovo}%' OR LOWER(description) LIKE '%{slovo}%'" for slovo in klucove_slova
        ])
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            try:
                c.execute(query)
                rows = c.fetchall()
            except Exception as e:
                rows = []
        if rows:
            kontext += f"Relevantné moduly podľa vašej otázky:\n"
            for row in rows:
                kontext += f"Modul: {row[0]}\nPopis: {row[1]}\n\n"
        else:
            # Ak sa nič nenájde, pošleme AI všetky moduly
            with sqlite3.connect(db_path) as conn:
                c = conn.cursor()
                c.execute("SELECT name, description FROM modules")
                all_rows = c.fetchall()
                kontext += f"V databáze je {len(all_rows)} modulov.\n"
                for row in all_rows:
                    kontext += f"Modul: {row[0]}\nPopis: {row[1]}\n\n"

        # Ak otázka obsahuje kľúčové slová o funkcionalitách, spracuj ich samostatne
        if any(kluc in otazka_norm for kluc in ["ake funkcionality", "zoznam funkcionalit", "vsetky funkcionality", "funkcionality mame", "funkcionality su"]):
            with sqlite3.connect('database/is_data.db') as conn:
                c = conn.cursor()
                c.execute("SELECT name, description FROM functionalities")
                rows = c.fetchall()
                if rows:
                    for row in rows:
                        kontext += f"Funkcionalita: {row[0]}\nPopis: {row[1]}\n\n"
        else:
            # 1. Vyhľadáme všetky moduly a funkcionality, ktoré obsahujú kľúčové slová z otázky
            vysl_modul = ai.find_module(otazka)
            vysl_func = ai.find_functionality(otazka)
            if vysl_modul:
                kontext += f"Modul: {vysl_modul['name']}\nPopis: {vysl_modul['description']}\nVerzia: {vysl_modul['version']}\n"
            if vysl_func:
                kontext += f"Funkcionalita: {vysl_func['name']}\nPopis: {vysl_func['description']}\n"
        # Spracovanie odpovede
        if not kontext:
            odpoved = "Nenašlo sa v databáze. Skús zadať presný názov modulu alebo funkcionality."
        else:
            prompt = f"Na základe týchto údajov odpovedz na otázku používateľa. Odpovedaj len z týchto údajov, nevymýšľaj si nič navyše.\n\nÚdaje:\n{kontext}\n\nOtázka: {otazka}\nOdpoveď:"
            ai_odpoved = ai.ask(prompt)
            odpoved = ai_odpoved
    # Odpoveď bez debug výpisu
    if not odpoved:
        odpoved = ""
    return render_template_string(AI_CHAT_HTML, odpoved=odpoved, otazka=otazka)

@app.route('/wiki', methods=['GET', 'POST'])
def wiki():
    """Wiki stránka zobrazujúca hierarchiu modulov a funkcionalít."""
    import sqlite3
    import json
    db_path = 'database/is_data.db'
    success_message = None
    error_message = None

    if request.method == 'POST':
        action = request.form.get('action')
        try:
            with sqlite3.connect(db_path) as conn:
                c = conn.cursor()
                if action == 'add_module':
                    c.execute(
                        "INSERT INTO modules (name, description) VALUES (?, ?)",
                        (request.form.get('name'), request.form.get('description', ''))
                    )
                    success_message = "Modul bol pridaný."
                elif action == 'add_submodule':
                    c.execute(
                        """
                        INSERT INTO modules (name, description, parent_module_id)
                        VALUES (?, ?, ?)
                        """,
                        (
                            request.form.get('name'),
                            request.form.get('description', ''),
                            request.form.get('parent_module_id')
                        )
                    )
                    success_message = "Podmodul bol pridaný."
                elif action == 'update_module':
                    c.execute(
                        """
                        UPDATE modules
                        SET name = ?, description = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                        """,
                        (
                            request.form.get('name'),
                            request.form.get('description', ''),
                            request.form.get('module_id')
                        )
                    )
                    success_message = "Modul bol aktualizovaný."
                elif action == 'add_functionality':
                    c.execute(
                        """
                        INSERT INTO functionalities (module_id, name, description, code_example)
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            request.form.get('module_id'),
                            request.form.get('name'),
                            request.form.get('description', ''),
                            request.form.get('code_example', '')
                        )
                    )
                    success_message = "Funkcionalita bola pridaná."
                elif action == 'add_relationship':
                    c.execute(
                        """
                        INSERT INTO module_relationships (module_from_id, module_to_id, relationship_type, description)
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            request.form.get('module_from_id'),
                            request.form.get('module_to_id'),
                            request.form.get('relationship_type', ''),
                            request.form.get('description', '')
                        )
                    )
                    success_message = "Súvislosť bola pridaná."
                conn.commit()
        except Exception as exc:
            error_message = f"Chyba pri ukladaní: {exc}"

    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        # Načítaj všetky moduly
        c.execute("SELECT id, name, description, parent_module_id FROM modules ORDER BY name")
        modules_raw = c.fetchall()

        # Mapa modulov podľa ID
        modules_map = {}
        for module in modules_raw:
            modules_map[module['id']] = {
                'id': module['id'],
                'name': module['name'],
                'description': module['description'],
                'parent_module_id': module['parent_module_id'],
                'functionalities': [],
                'relationships': [],
                'submodules': []
            }

        # Funkcionality
        c.execute("SELECT module_id, name, description FROM functionalities ORDER BY name")
        funcs = c.fetchall()
        total_functionalities = 0
        for func in funcs:
            if func['module_id'] in modules_map:
                modules_map[func['module_id']]['functionalities'].append({
                    'name': func['name'],
                    'description': func['description']
                })
                total_functionalities += 1

        # Súvislosti
        c.execute("""
            SELECT mr.module_from_id, mr.module_to_id, mr.relationship_type, mr.description,
                   mto.name AS to_module_name
            FROM module_relationships mr
            LEFT JOIN modules mto ON mto.id = mr.module_to_id
        """)
        rels = c.fetchall()
        for rel in rels:
            if rel['module_from_id'] in modules_map:
                modules_map[rel['module_from_id']]['relationships'].append({
                    'relationship_type': rel['relationship_type'],
                    'description': rel['description'],
                    'to_module_name': rel['to_module_name'] or 'Neznámy modul'
                })

        # Hierarchia modulov/podmodulov
        modules = []
        for module in modules_map.values():
            parent_id = module['parent_module_id']
            if parent_id and parent_id in modules_map:
                modules_map[parent_id]['submodules'].append(module)
            else:
                modules.append(module)

        all_modules = list(modules_map.values())

    return render_template_string(
        WIKI_HTML,
        modules=modules,
        all_modules=all_modules,
        total_modules=len(all_modules),
        total_functionalities=total_functionalities,
        success_message=success_message,
        error_message=error_message
    )

@app.route('/wiki/admin', methods=['GET', 'POST'])
def wiki_admin():
    """Admin stránka pre správu modulov."""
    import sqlite3
    db_path = 'database/is_data.db'
    success_message = None
    error_message = None

    if request.method == 'POST':
        action = request.form.get('action')
        try:
            with sqlite3.connect(db_path) as conn:
                c = conn.cursor()
                if action == 'add_module':
                    c.execute(
                        "INSERT INTO modules (name, description) VALUES (?, ?)",
                        (request.form.get('name'), request.form.get('description', ''))
                    )
                    success_message = "Modul bol pridaný."
                elif action == 'add_submodule':
                    c.execute(
                        """
                        INSERT INTO modules (name, description, parent_module_id)
                        VALUES (?, ?, ?)
                        """,
                        (
                            request.form.get('name'),
                            request.form.get('description', ''),
                            request.form.get('parent_module_id')
                        )
                    )
                    success_message = "Podmodul bol pridaný."
                elif action == 'add_functionality':
                    c.execute(
                        """
                        INSERT INTO functionalities (module_id, name, description, code_example)
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            request.form.get('module_id'),
                            request.form.get('name'),
                            request.form.get('description', ''),
                            request.form.get('code_example', '')
                        )
                    )
                    success_message = "Funkcionalita bola pridaná."
                elif action == 'add_relationship':
                    c.execute(
                        """
                        INSERT INTO module_relationships (module_from_id, module_to_id, relationship_type, description)
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            request.form.get('module_from_id'),
                            request.form.get('module_to_id'),
                            request.form.get('relationship_type', ''),
                            request.form.get('description', '')
                        )
                    )
                    success_message = "Súvislosť bola pridaná."
                conn.commit()
        except Exception as exc:
            error_message = f"Chyba pri ukladaní: {exc}"

    # Načítaj moduly pre formuláre
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        c.execute("SELECT id, name, description, parent_module_id FROM modules ORDER BY name")
        modules_raw = c.fetchall()
        all_modules = [dict(m) for m in modules_raw]
        
        c.execute("SELECT COUNT(*) as cnt FROM functionalities")
        total_functionalities = c.fetchone()['cnt']

    return render_template_string(
        WIKI_ADMIN_HTML,
        all_modules=all_modules,
        total_modules=len(all_modules),
        total_functionalities=total_functionalities,
        success_message=success_message,
        error_message=error_message
    )

@app.route('/ai-parse-summary', methods=['POST'])
def ai_parse_summary():
    """AI parseuje počiatočný súhrn a extrahuje údaje."""
    import json
    
    data = request.get_json()
    summary = data.get('summary', '').strip()
    
    if not summary:
        return jsonify({'error': 'Žiadny súhrn nezadaný'}), 400
    
    # Prompt pre AI na parsovanie súhrnu
    prompt = """Si asistent, ktorý extrahuje údaje zo súhrnu stretnutia so zákazníkom.

Extrahuj z textu tieto údaje vo formáte JSON:

1. **contact_name** - meno kontaktnej osoby (ak je uvedené)
2. **contact_email** - email (ak je uvedený)
3. **contact_phone** - telefón (ak je uvedený)
4. **companies** - zoznam firiem:
   - name: názov firmy
   - ico: IČO (8-miestne číslo)
5. **branches** - zoznam pobočiek/prevádzok:
   - name: názov pobočky (napr. "Reštaurácia U Janka", "Predajňa Centrum")
   - address: ÚPLNÁ adresa (ulica + číslo, PSČ, mesto). Ak nie je úplná, nechaj prázdne.
   - type: pole typov podnikania. Môže obsahovať viacero hodnôt z: ["restauracia", "obchod", "eshop", "sklad", "kancelaria", "vyrobna", "servis", "ine"]
     - Ak sa spomína jedlo, gastronómia, reštaurácia, kaviareň, bar, pizzeria = "restauracia"
     - Ak sa spomína obchod, predajňa, kamenný obchod = "obchod"
     - Ak sa spomína e-shop, online predaj, internetový obchod = "eshop"
     - Ak sa spomína sklad, skladovanie = "sklad"
     - Ak sa spomína kancelária, administratíva, office = "kancelaria"
     - Ak sa spomína výroba, výrobňa = "vyrobna"
     - Ak sa spomína servis, opravy = "servis"
   - location_hint: ak chýba úplná adresa, uveď čo vieš (mesto, ulicu, mestskú časť)

DÔLEŽITÉ:
- Typ pobočky VŽDY vyplň ak vieš určiť z kontextu (reštaurácia = "restauracia", obchod = "obchod", atď.)
- Adresu vyplň len ak je kompletná (ulica + číslo + mesto)
- type musí byť POLE (array), nie string!

Súhrn na parsovanie:
---
{summary}
---

Vrať IBA platný JSON bez komentárov:
{{
    "contact_name": "",
    "contact_email": "",
    "contact_phone": "",
    "companies": [
        {{"name": "", "ico": ""}}
    ],
    "branches": [
        {{
            "name": "",
            "address": "",
            "type": ["restauracia"],
            "location_hint": ""
        }}
    ]
}}""".format(summary=summary)
    
    try:
        # Zavolaj AI
        response = ai.ask(prompt)
        
        # Parsuj JSON z odpovede
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        
        if json_start >= 0 and json_end > json_start:
            json_str = response[json_start:json_end]
            parsed_data = json.loads(json_str)
            
            # Ak pobočka nemá adresu, skúsime ju nájsť cez Nominatim
            from geopy.geocoders import Nominatim
            geolocator = Nominatim(user_agent="is_assistant_app")
            
            if 'branches' in parsed_data:
                for branch in parsed_data['branches']:
                    # Ak adresa chýba ale máme location_hint
                    if (not branch.get('address') or branch.get('address').strip() == '') and branch.get('location_hint'):
                        try:
                            # Vytvor vyhľadávací query
                            search_query = f"{branch.get('name', '')} {branch.get('location_hint', '')}"
                            location = geolocator.geocode(search_query, language='sk', timeout=5)
                            
                            if location:
                                branch['address'] = location.address
                                branch['address_suggested'] = True
                        except Exception as loc_err:
                            # Ticho ignorujeme chyby geolokácie
                            pass
            
            return jsonify(parsed_data)
        else:
            return jsonify({'error': 'AI nemohla parsovať súhrn'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/transcribe-audio', methods=['POST'])
def transcribe_audio():
    """Konvertuje audio súbor na text pomocou Whisper."""
    import os
    import time
    import io
    
    if 'audio' not in request.files:
        return jsonify({'error': 'Žiadny audio súbor'}), 400
    
    audio_file = request.files['audio']
    
    if audio_file.filename == '':
        return jsonify({'error': 'Žiadny súbor vybratý'}), 400
    
    temp_path = None
    try:
        # Uložíme dočasný súbor do project adresára
        temp_filename = f'temp_audio_{int(time.time() * 1000)}.wav'
        temp_path = os.path.abspath(temp_filename)
        
        # Ulož audio súbor
        audio_file.save(temp_path)
        
        # Skontroluj či súbor existuje
        if not os.path.exists(temp_path):
            return jsonify({'error': f'Súbor sa neuloži'}), 500
        
        file_size = os.path.getsize(temp_path)
        if file_size == 0:
            return jsonify({'error': 'Audio súbor je prazdny'}), 400
        
        # Čítaj WebM pomocou pydub a konvertuj na raw audio
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
            return jsonify({'error': f'Nemožno spracovať audio: {str(read_error)}'}), 400
        
        
        if not text:
            return jsonify({'error': 'Whisper nemohol extrahovať text. Skúste hovoriteľnejšie.'}), 400
        
        return jsonify({'text': text})
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return jsonify({
            'error': f'Chyba: {str(e) if str(e) else "Unknown error"}',
            'details': error_details
        }), 500
    finally:
        # Zmaž dočasný súbor
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass

@app.route('/new-customer', methods=['GET', 'POST'])
def new_customer():
    """Formulár pre vytvorenie nového zákazníka s dynamickými otázkami."""
    success = False
    
    if request.method == 'POST':
        import sqlite3
        import json
        from datetime import datetime
        
        # Získaj základné údaje
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone', '')
        
        # Spracuj firmy - zber všetkých firiem s príslušnými údajmi
        companies = []
        company_index = 0
        while f'company_name_{company_index}' in request.form:
            company_name = request.form.get(f'company_name_{company_index}', '').strip()
            company_ico = request.form.get(f'company_ico_{company_index}', '').strip()
            
            if company_name and company_ico:  # Ulož len ak má názov a IČO
                companies.append({
                    'name': company_name,
                    'ico': company_ico
                })
            company_index += 1
        
        # Spracuj pobočky - zber všetkých pobočiek
        branches = []
        branch_index = 0
        while f'branch_name_{branch_index}' in request.form:
            branch_name = request.form.get(f'branch_name_{branch_index}', '').strip()
            branch_address = request.form.get(f'branch_address_{branch_index}', '').strip()
            # Checkboxy - použijem getlist pre viacnásobný výber
            branch_types = request.form.getlist(f'branch_type_{branch_index}')
            branch_type = ','.join(branch_types) if branch_types else ''
            branch_info = request.form.get(f'branch_info_{branch_index}', '').strip()
            
            if branch_name:  # Ulož ak má aspoň názov
                branches.append({
                    'name': branch_name,
                    'address': branch_address,
                    'branch_type': branch_type,
                    'additional_info': branch_info
                })
            branch_index += 1
        
        # Vytvor kompletný dotazník ako JSON (všetky odpovede)
        questionnaire = {
            'companies': companies,
            'expectations': request.form.get('expectations', ''),
            'timeline': request.form.get('timeline', '')
        }
        
        # Ulož do databázy - prvú firmu daj ako company_name, ostatné v questionnaire
        first_company_name = companies[0]['name'] if companies else ''
        first_company_ico = companies[0]['ico'] if companies else ''
        business_types_first = ''  # Typ podnikania z firmy sme odstránili
        
        # Ulož zákazníka do databázy
        initial_summary = request.form.get('initial_summary', '').strip()
        
        with sqlite3.connect('database/is_data.db') as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO customers 
                (name, contact_email, contact_phone, company_name, business_type, questionnaire_data, initial_summary)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, email, phone, first_company_name, business_types_first, json.dumps(questionnaire, ensure_ascii=False), initial_summary))
            customer_id = c.lastrowid
            
            # Ulož pobočky do samostatnej tabuľky
            for branch in branches:
                c.execute('''
                    INSERT INTO branches (customer_id, name, address, branch_type, additional_info)
                    VALUES (?, ?, ?, ?, ?)
                ''', (customer_id, branch['name'], branch['address'], branch['branch_type'], branch.get('additional_info', '')))
            
            conn.commit()
        
        success = True
    
    return render_template_string(NEW_CUSTOMER_HTML, success=success)

@app.route('/customers')
def customers():
    """Zoznam existujúcich zákazníkov."""
    import sqlite3
    import json
    
    with sqlite3.connect('database/is_data.db') as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('''
            SELECT id, name, business_type, contact_email, contact_phone, 
                   company_name, questionnaire_data, initial_summary, created_at
            FROM customers
            ORDER BY created_at DESC
        ''')
        customers_raw = c.fetchall()
    
    # Sparsuj questionnaire_data a rozdeľ firmy + načítaj pobočky
    customers_list = []
    for cust in customers_raw:
        cust_dict = dict(cust)
        cust_dict['companies'] = []
        cust_dict['branches'] = []  # Pridaj zoznam pobočiek
        
        if cust['questionnaire_data']:
            try:
                questionnaire = json.loads(cust['questionnaire_data'])
                if 'companies' in questionnaire:
                    cust_dict['companies'] = questionnaire['companies']
            except:
                pass
        
        # Načítaj pobočky pre tohto zákazníka z databázy
        with sqlite3.connect('database/is_data.db') as conn:
            conn.row_factory = sqlite3.Row
            c2 = conn.cursor()
            c2.execute('''
                SELECT id, name, address, branch_type, additional_info, created_at
                FROM branches
                WHERE customer_id = ?
                ORDER BY created_at ASC
            ''', (cust['id'],))
            branches_raw = c2.fetchall()
            cust_dict['branches'] = [dict(b) for b in branches_raw]
        
        customers_list.append(cust_dict)
    
    return render_template_string(CUSTOMERS_HTML, customers=customers_list)

@app.route('/customer/<int:customer_id>/edit', methods=['GET', 'POST'])
def customer_edit(customer_id):
    """Editácia existujúceho zákazníka."""
    import sqlite3
    import json
    
    db_path = 'database/is_data.db'
    success_message = None
    error_message = None
    
    if request.method == 'POST':
        try:
            with sqlite3.connect(db_path) as conn:
                c = conn.cursor()
                
                # Spracuj firmy z formulára
                companies = []
                company_index = 0
                while f'company_name_{company_index}' in request.form:
                    company_name = request.form.get(f'company_name_{company_index}', '').strip()
                    company_ico = request.form.get(f'company_ico_{company_index}', '').strip()
                    
                    if company_name:  # Ulož ak má názov
                        companies.append({
                            'name': company_name,
                            'ico': company_ico
                        })
                    company_index += 1
                
                # Vytvor questionnaire JSON
                questionnaire = {
                    'companies': companies,
                    'expectations': request.form.get('expectations', ''),
                    'timeline': request.form.get('timeline', '')
                }
                
                # Prvá firma ako hlavný company_name
                first_company_name = companies[0]['name'] if companies else ''
                
                # Aktualizuj základné údaje zákazníka
                c.execute('''
                    UPDATE customers 
                    SET name = ?, contact_email = ?, contact_phone = ?, 
                        initial_summary = ?, company_name = ?, questionnaire_data = ?
                    WHERE id = ?
                ''', (
                    request.form.get('name'),
                    request.form.get('email'),
                    request.form.get('phone'),
                    request.form.get('initial_summary'),
                    first_company_name,
                    json.dumps(questionnaire, ensure_ascii=False),
                    customer_id
                ))
                
                # Aktualizuj pobočky
                branch_ids = request.form.getlist('branch_ids')
                for branch_id in branch_ids:
                    # Spracuj typ pobočky (môže byť viac checkboxov)
                    branch_types = request.form.getlist(f'branch_type_{branch_id}')
                    branch_type_str = ','.join(branch_types) if branch_types else ''
                    
                    c.execute('''
                        UPDATE branches
                        SET name = ?, address = ?, branch_type = ?, additional_info = ?
                        WHERE id = ?
                    ''', (
                        request.form.get(f'branch_name_{branch_id}'),
                        request.form.get(f'branch_address_{branch_id}'),
                        branch_type_str,
                        request.form.get(f'branch_info_{branch_id}'),
                        branch_id
                    ))
                
                # Pridaj nové pobočky
                new_branch_ids = request.form.getlist('new_branch_ids')
                for new_id in new_branch_ids:
                    new_name = request.form.get(f'new_branch_name_{new_id}', '').strip()
                    new_address = request.form.get(f'new_branch_address_{new_id}', '').strip()
                    new_types = request.form.getlist(f'new_branch_type_{new_id}')
                    new_type_str = ','.join(new_types) if new_types else ''
                    new_info = request.form.get(f'new_branch_info_{new_id}', '').strip()
                    
                    if new_name:  # Ulož len ak má názov
                        c.execute('''
                            INSERT INTO branches (customer_id, name, address, branch_type, additional_info)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (customer_id, new_name, new_address, new_type_str, new_info))
                
                conn.commit()
                success_message = "Zákazník bol úspešne aktualizovaný."
        except Exception as e:
            error_message = f"Chyba pri ukladaní: {e}"
    
    # Načítaj zákazníka
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        c.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
        customer = c.fetchone()
        
        if not customer:
            return "Zákazník nebol nájdený", 404
        
        customer = dict(customer)
        
        # Načítaj pobočky
        c.execute('SELECT * FROM branches WHERE customer_id = ? ORDER BY created_at', (customer_id,))
        branches = [dict(b) for b in c.fetchall()]
        
        # Parsuj questionnaire data
        companies = []
        expectations = ''
        timeline = ''
        
        if customer.get('questionnaire_data'):
            try:
                q_data = json.loads(customer['questionnaire_data'])
                companies = q_data.get('companies', [])
                expectations = q_data.get('expectations', '')
                timeline = q_data.get('timeline', '')
            except:
                pass
        
        # Ak nie sú firmy v questionnaire, použi company_name
        if not companies and customer.get('company_name'):
            companies = [{'name': customer['company_name'], 'ico': ''}]
    
    return render_template_string(
        CUSTOMER_EDIT_HTML,
        customer=customer,
        branches=branches,
        companies=companies,
        expectations=expectations,
        timeline=timeline,
        success_message=success_message,
        error_message=error_message
    )

@app.route('/customer/<int:customer_id>/delete', methods=['POST'])
def customer_delete(customer_id):
    """Zmazanie zákazníka a jeho pobočiek."""
    import sqlite3
    
    db_path = 'database/is_data.db'
    
    try:
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            
            # Najprv zmaž pobočky zákazníka
            c.execute('DELETE FROM branches WHERE customer_id = ?', (customer_id,))
            
            # Potom zmaž zákazníka
            c.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
            
            conn.commit()
    except Exception as e:
        # Log error but redirect anyway
        print(f"Chyba pri mazaní zákazníka: {e}")
    
    return redirect('/customers')

# ============ ŠKOLENIA HTML ŠABLÓNY ============

# HTML šablóna pre ŠKOLENIA - tréningové materiály (zelená/teal farba)
TRAINING_HTML = '''
<!doctype html>
<html lang="sk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IS-Assistant | Školenia</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #00897b 0%, #26a69a 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 { color: #00897b; margin-bottom: 10px; text-align: center; font-size: 2.5em; }
        .subtitle { text-align: center; color: #666; margin-bottom: 30px; }
        .nav-links {
            margin-bottom: 30px; text-align: center;
            display: flex; flex-wrap: wrap; justify-content: center; gap: 15px;
        }
        .nav-link { color: #00897b; text-decoration: none; font-weight: 600; transition: color 0.3s; }
        .nav-link:hover { color: #26a69a; }
        
        .case-list { margin-top: 20px; }
        .case-item {
            display: flex; align-items: center; gap: 15px;
            padding: 20px; margin-bottom: 10px;
            background: linear-gradient(135deg, #e0f2f1 0%, #b2dfdb 100%);
            border-radius: 12px; border-left: 5px solid #00897b;
            cursor: pointer; transition: all 0.3s;
        }
        .case-item:hover { transform: translateX(10px); box-shadow: 0 5px 20px rgba(0,0,0,0.1); }
        .case-icon { font-size: 2em; }
        .case-info { flex: 1; }
        .case-title { font-size: 1.2em; font-weight: 600; color: #333; }
        .case-desc { color: #666; font-size: 0.95em; margin-top: 5px; }
        .case-meta { display: flex; gap: 15px; margin-top: 8px; font-size: 0.85em; color: #888; }
        .case-arrow { color: #00897b; font-size: 1.5em; }
        .difficulty { padding: 3px 10px; border-radius: 12px; font-size: 0.8em; font-weight: 600; }
        .difficulty.beginner { background: #c8e6c9; color: #2e7d32; }
        .difficulty.intermediate { background: #fff9c4; color: #f57f17; }
        .difficulty.advanced { background: #ffcdd2; color: #c62828; }
        
        .add-btn {
            display: inline-flex; align-items: center; gap: 8px;
            padding: 12px 25px; background: linear-gradient(135deg, #00897b 0%, #26a69a 100%);
            color: white; border: none; border-radius: 25px;
            font-weight: 600; cursor: pointer; transition: all 0.3s;
            text-decoration: none; margin-bottom: 20px;
        }
        .add-btn:hover { transform: scale(1.05); box-shadow: 0 5px 20px rgba(0,137,123,0.4); }
        
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                 background: rgba(0,0,0,0.5); z-index: 1000; align-items: center; justify-content: center; }
        .modal.active { display: flex; }
        .modal-content {
            background: white; border-radius: 15px; padding: 30px;
            max-width: 600px; width: 90%; max-height: 80vh; overflow-y: auto;
        }
        .modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .modal-title { font-size: 1.4em; color: #00897b; }
        .close-btn { background: none; border: none; font-size: 1.5em; cursor: pointer; color: #999; }
        
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; font-weight: 600; margin-bottom: 5px; color: #333; }
        .form-group input, .form-group textarea, .form-group select {
            width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 1em;
        }
        .form-group input:focus, .form-group textarea:focus { border-color: #00897b; outline: none; }
        .submit-btn {
            width: 100%; padding: 15px; background: linear-gradient(135deg, #00897b 0%, #26a69a 100%);
            color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;
        }
        
        .no-cases { text-align: center; padding: 60px 20px; color: #999; }
        .no-cases-icon { font-size: 4em; margin-bottom: 20px; }
        
        .search-box {
            display: flex; gap: 10px; margin-bottom: 25px;
            background: linear-gradient(135deg, #e0f2f1 0%, #b2dfdb 100%);
            padding: 15px; border-radius: 15px;
        }
        .search-input {
            flex: 1; padding: 12px 20px; border: 2px solid #b2dfdb;
            border-radius: 25px; font-size: 1em; outline: none;
        }
        .search-input:focus { border-color: #00897b; }
        .search-btn {
            padding: 12px 25px; background: linear-gradient(135deg, #00897b 0%, #26a69a 100%);
            color: white; border: none; border-radius: 25px;
            font-weight: 600; cursor: pointer; transition: all 0.3s;
        }
        .search-btn:hover { transform: scale(1.05); }
        .clear-btn {
            padding: 12px 20px; background: #6c757d; color: white;
            border: none; border-radius: 25px; cursor: pointer;
            text-decoration: none; font-weight: 600;
        }
        .search-results {
            background: #e0f2f1; padding: 10px 20px; border-radius: 10px;
            margin-bottom: 20px; color: #00695c;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎓 Školenia</h1>
        <p class="subtitle">Tréningové materiály a vzdelávacie kurzy pre prácu s IS</p>
        
        <div class="nav-links">
            <a href="/" class="nav-link">🏠 Dashboard</a>
            <a href="/wiki" class="nav-link">📚 Wiki</a>
            <a href="/service" class="nav-link">🔧 Servis</a>
            <a href="/ai-chat" class="nav-link">💬 AI Asistent</a>
            <a href="/customers" class="nav-link">👥 Zákazníci</a>
        </div>
        
        <form class="search-box" method="GET" action="/training">
            <input type="text" name="q" class="search-input" 
                   placeholder="🔍 Hľadať v školeniach..."
                   value="{{ search_query or '' }}">
            <button type="submit" class="search-btn">Hľadať</button>
            {% if search_query %}
            <a href="/training" class="clear-btn">✕ Zrušiť</a>
            {% endif %}
        </form>
        
        {% if search_query %}
        <div class="search-results">
            🔍 Výsledky pre "<strong>{{ search_query }}</strong>": nájdených <strong>{{ cases|length }}</strong> školení
        </div>
        {% endif %}
        
        <button class="add-btn" onclick="openModal()">➕ Nové školenie</button>
        
        <div class="case-list">
            {% if cases %}
                {% for case in cases %}
                <a href="/training/{{ case.id }}" style="text-decoration: none;">
                    <div class="case-item">
                        <div class="case-icon">📖</div>
                        <div class="case-info">
                            <div class="case-title">{{ case.title }}</div>
                            <div class="case-desc">{{ case.description[:100] if case.description else '' }}{% if case.description and case.description|length > 100 %}...{% endif %}</div>
                            <div class="case-meta">
                                <span>📁 {{ case.category or 'Bez kategórie' }}</span>
                                <span>📅 {{ case.created_at[:10] if case.created_at else '' }}</span>
                                <span>📝 {{ case.steps_count or 0 }} krokov</span>
                                <span class="difficulty {{ case.difficulty or 'beginner' }}">
                                    {% if case.difficulty == 'advanced' %}Pokročilý
                                    {% elif case.difficulty == 'intermediate' %}Stredný
                                    {% else %}Začiatočník{% endif %}
                                </span>
                            </div>
                        </div>
                        <div class="case-arrow">→</div>
                    </div>
                </a>
                {% endfor %}
            {% else %}
                <div class="no-cases">
                    <div class="no-cases-icon">📖</div>
                    <h2>Zatiaľ žiadne školenia</h2>
                    <p>Začnite pridaním prvého školenia</p>
                </div>
            {% endif %}
        </div>
    </div>
    
    <div class="modal" id="addModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 class="modal-title">➕ Nové školenie</h2>
                <button class="close-btn" onclick="closeModal()">&times;</button>
            </div>
            <form method="POST" action="/training/add">
                <div class="form-group">
                    <label>Názov školenia</label>
                    <input type="text" name="title" required placeholder="Napr. Základy práce s IS">
                </div>
                <div class="form-group">
                    <label>Kategória</label>
                    <select name="category">
                        <option value="Základy IS">Základy IS</option>
                        <option value="Moduly">Moduly</option>
                        <option value="Reporty">Reporty</option>
                        <option value="Administrácia">Administrácia</option>
                        <option value="Integrácie">Integrácie</option>
                        <option value="Iné">Iné</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Úroveň obtiažnosti</label>
                    <select name="difficulty">
                        <option value="beginner">Začiatočník</option>
                        <option value="intermediate">Stredný</option>
                        <option value="advanced">Pokročilý</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Popis</label>
                    <textarea name="description" rows="4" placeholder="O čom je toto školenie..."></textarea>
                </div>
                <button type="submit" class="submit-btn">Vytvoriť</button>
            </form>
        </div>
    </div>
    
    <script>
        function openModal() { document.getElementById('addModal').classList.add('active'); }
        function closeModal() { document.getElementById('addModal').classList.remove('active'); }
        document.getElementById('addModal').onclick = function(e) { if (e.target === this) closeModal(); }
    </script>
</body>
</html>
'''

# HTML šablóna pre detail školenia
TRAINING_DETAIL_HTML = '''
<!doctype html>
<html lang="sk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IS-Assistant | {{ case.title }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #00897b 0%, #26a69a 100%);
            min-height: 100vh; padding: 20px;
        }
        .container {
            background: white; border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px; max-width: 1000px; margin: 0 auto;
        }
        .back-link { color: #00897b; text-decoration: none; font-weight: 600; display: inline-flex; align-items: center; gap: 5px; margin-bottom: 20px; }
        .back-link:hover { color: #26a69a; }
        h1 { color: #00897b; margin-bottom: 10px; font-size: 2em; }
        .case-meta { color: #666; margin-bottom: 30px; display: flex; gap: 20px; flex-wrap: wrap; }
        .case-desc { background: #e0f2f1; padding: 20px; border-radius: 10px; margin-bottom: 30px; line-height: 1.6; }
        .difficulty { padding: 3px 10px; border-radius: 12px; font-size: 0.85em; font-weight: 600; }
        .difficulty.beginner { background: #c8e6c9; color: #2e7d32; }
        .difficulty.intermediate { background: #fff9c4; color: #f57f17; }
        .difficulty.advanced { background: #ffcdd2; color: #c62828; }
        
        .section-title { color: #00897b; font-size: 1.4em; margin: 30px 0 20px; display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
        
        .steps-list { margin-bottom: 30px; }
        .step-item {
            background: linear-gradient(135deg, #e0f2f1 0%, #b2dfdb 100%);
            border-radius: 12px; padding: 20px; margin-bottom: 15px;
            border-left: 5px solid #00897b;
            transition: all 0.3s;
        }
        .step-item:hover { box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .step-item.decision { border-left-color: #ff9800; background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%); }
        .step-number {
            display: inline-flex; align-items: center; justify-content: center;
            width: 32px; height: 32px; background: #00897b;
            color: white; border-radius: 50%; font-weight: bold; margin-right: 15px;
        }
        .step-number.decision { background: #ff9800; }
        .step-title { font-weight: 600; color: #333; display: inline; }
        .step-desc { margin-top: 10px; color: #666; padding-left: 47px; }
        .step-actions { margin-top: 10px; padding-left: 47px; display: flex; gap: 10px; }
        .step-actions button, .step-actions a {
            padding: 5px 12px; border-radius: 5px; font-size: 0.85em;
            cursor: pointer; text-decoration: none; border: none;
        }
        .edit-btn { background: #2196F3; color: white; }
        .delete-btn { background: #f44336; color: white; }
        
        .branch-container {
            margin-left: 30px; margin-top: 15px; padding: 15px;
            border-left: 4px solid #26a69a; background: #f5f5f5; border-radius: 0 10px 10px 0;
        }
        .branch-header { font-weight: 600; color: #00897b; margin-bottom: 10px; display: flex; align-items: center; gap: 8px; }
        .branch-color { width: 12px; height: 12px; border-radius: 50%; }
        
        .add-step-form {
            background: #e0f2f1; padding: 20px; border-radius: 12px; margin-top: 20px;
        }
        .add-step-form h3 { color: #00897b; margin-bottom: 15px; }
        .form-row { display: flex; gap: 15px; margin-bottom: 15px; flex-wrap: wrap; }
        .form-group { flex: 1; min-width: 200px; }
        .form-group label { display: block; font-weight: 600; margin-bottom: 5px; }
        .form-group input, .form-group textarea, .form-group select {
            width: 100%; padding: 10px; border: 2px solid #b2dfdb; border-radius: 8px;
        }
        .form-group input:focus, .form-group textarea:focus { border-color: #00897b; outline: none; }
        .submit-btn {
            padding: 12px 30px; background: linear-gradient(135deg, #00897b 0%, #26a69a 100%);
            color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;
        }
        .submit-btn:hover { transform: scale(1.02); }
        
        .complications { margin-top: 30px; }
        .complication-item {
            background: #fff3e0; border-left: 4px solid #ff9800;
            padding: 15px; border-radius: 0 10px 10px 0; margin-bottom: 10px;
        }
        .complication-title { font-weight: 600; color: #e65100; }
        .complication-desc { margin-top: 8px; color: #666; }
        .complication-solution { margin-top: 8px; padding: 10px; background: #e8f5e9; border-radius: 8px; color: #2e7d32; }
        
        .no-steps { text-align: center; padding: 40px; color: #999; background: #f5f5f5; border-radius: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <a href="/training" class="back-link">← Späť na školenia</a>
        
        <h1>📖 {{ case.title }}</h1>
        <div class="case-meta">
            <span>📁 {{ case.category or 'Bez kategórie' }}</span>
            <span>📅 {{ case.created_at[:10] if case.created_at else '' }}</span>
            <span class="difficulty {{ case.difficulty or 'beginner' }}">
                {% if case.difficulty == 'advanced' %}Pokročilý
                {% elif case.difficulty == 'intermediate' %}Stredný
                {% else %}Začiatočník{% endif %}
            </span>
        </div>
        
        {% if case.description %}
        <div class="case-desc">{{ case.description }}</div>
        {% endif %}
        
        <h2 class="section-title">📋 Kroky školenia</h2>
        
        <div class="steps-list">
            {% if steps %}
                {% for step in steps %}
                <div class="step-item {% if step.step_type == 'decision' %}decision{% endif %}">
                    <span class="step-number {% if step.step_type == 'decision' %}decision{% endif %}">
                        {% if step.step_type == 'decision' %}?{% else %}{{ step.step_number }}{% endif %}
                    </span>
                    <span class="step-title">{{ step.title }}</span>
                    {% if step.description %}
                    <div class="step-desc">{{ step.description }}</div>
                    {% endif %}
                    <div class="step-actions">
                        <button class="edit-btn" onclick="editStep({{ step.id }}, '{{ step.title }}', '{{ step.description|default('', true)|replace("'", "\\'") }}')">✏️ Upraviť</button>
                        <a href="/training/{{ case.id }}/delete-step/{{ step.id }}" class="delete-btn" onclick="return confirm('Naozaj zmazať tento krok?')">🗑️ Zmazať</a>
                    </div>
                    
                    {% for branch in branches if branch.parent_step_id == step.id %}
                    <div class="branch-container" style="border-left-color: {{ branch.branch_color }};">
                        <div class="branch-header">
                            <span class="branch-color" style="background: {{ branch.branch_color }};"></span>
                            {{ branch.branch_name }}
                        </div>
                        {% for bstep in steps if bstep.branch_id == branch.id %}
                        <div class="step-item" style="margin-left: 0; border-left-color: {{ branch.branch_color }};">
                            <span class="step-number" style="background: {{ branch.branch_color }};">{{ bstep.step_number }}</span>
                            <span class="step-title">{{ bstep.title }}</span>
                            {% if bstep.description %}
                            <div class="step-desc">{{ bstep.description }}</div>
                            {% endif %}
                        </div>
                        {% endfor %}
                    </div>
                    {% endfor %}
                </div>
                {% endfor %}
            {% else %}
                <div class="no-steps">
                    <p>📝 Zatiaľ žiadne kroky. Pridajte prvý krok nižšie.</p>
                </div>
            {% endif %}
        </div>
        
        {% if complications %}
        <div class="complications">
            <h2 class="section-title">⚠️ Možné komplikácie</h2>
            {% for comp in complications %}
            <div class="complication-item">
                <div class="complication-title">{{ comp.title }}</div>
                {% if comp.description %}
                <div class="complication-desc">{{ comp.description }}</div>
                {% endif %}
                {% if comp.solution %}
                <div class="complication-solution"><strong>Riešenie:</strong> {{ comp.solution }}</div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        <div class="add-step-form">
            <h3>➕ Pridať nový krok</h3>
            <form method="POST" action="/training/{{ case.id }}/add-step">
                <div class="form-row">
                    <div class="form-group">
                        <label>Typ</label>
                        <select name="step_type">
                            <option value="step">Krok</option>
                            <option value="decision">Rozhodnutie</option>
                        </select>
                    </div>
                    <div class="form-group" style="flex: 2;">
                        <label>Názov kroku</label>
                        <input type="text" name="title" required placeholder="Čo sa má urobiť...">
                    </div>
                </div>
                <div class="form-group">
                    <label>Popis (voliteľné)</label>
                    <textarea name="description" rows="3" placeholder="Podrobnejší popis..."></textarea>
                </div>
                <button type="submit" class="submit-btn">Pridať krok</button>
            </form>
        </div>
        
        <div class="add-step-form" style="margin-top: 20px; background: #fff3e0;">
            <h3>⚠️ Pridať komplikáciu</h3>
            <form method="POST" action="/training/{{ case.id }}/add-complication">
                <div class="form-group">
                    <label>Názov problému</label>
                    <input type="text" name="title" required placeholder="Napr. Chyba pri pripojení...">
                </div>
                <div class="form-group">
                    <label>Popis problému</label>
                    <textarea name="description" rows="2" placeholder="Kedy nastáva..."></textarea>
                </div>
                <div class="form-group">
                    <label>Riešenie</label>
                    <textarea name="solution" rows="2" placeholder="Ako vyriešiť..."></textarea>
                </div>
                <button type="submit" class="submit-btn" style="background: linear-gradient(135deg, #ff9800 0%, #ffc107 100%);">Pridať komplikáciu</button>
            </form>
        </div>
    </div>
    
    <div class="modal" id="editModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:1000; align-items:center; justify-content:center;">
        <div style="background:white; border-radius:15px; padding:30px; max-width:500px; width:90%;">
            <h3 style="color:#00897b; margin-bottom:20px;">✏️ Upraviť krok</h3>
            <form method="POST" id="editForm">
                <div class="form-group">
                    <label>Názov</label>
                    <input type="text" name="title" id="editTitle" required>
                </div>
                <div class="form-group">
                    <label>Popis</label>
                    <textarea name="description" id="editDesc" rows="3"></textarea>
                </div>
                <div style="display:flex; gap:10px;">
                    <button type="submit" class="submit-btn">Uložiť</button>
                    <button type="button" onclick="closeEditModal()" style="padding:12px 30px; background:#6c757d; color:white; border:none; border-radius:8px; cursor:pointer;">Zrušiť</button>
                </div>
            </form>
        </div>
    </div>
    
    <script>
        function editStep(stepId, title, desc) {
            document.getElementById('editForm').action = '/training/{{ case.id }}/edit-step/' + stepId;
            document.getElementById('editTitle').value = title;
            document.getElementById('editDesc').value = desc;
            document.getElementById('editModal').style.display = 'flex';
        }
        function closeEditModal() {
            document.getElementById('editModal').style.display = 'none';
        }
    </script>
</body>
</html>
'''

# ============ SERVIS ROUTES ============

@app.route('/service')
def service():
    """Zoznam prípadových štúdií s vyhľadávaním."""
    import sqlite3
    
    search_query = request.args.get('q', '').strip()
    
    with sqlite3.connect('database/is_data.db') as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        if search_query:
            # Vyhľadávanie vo všetkých relevantných tabuľkách
            search_term = f'%{search_query}%'
            c.execute('''
                SELECT DISTINCT sc.*, 
                       (SELECT COUNT(*) FROM service_steps WHERE case_id = sc.id) as steps_count
                FROM service_cases sc
                LEFT JOIN service_steps ss ON ss.case_id = sc.id
                LEFT JOIN service_complications sco ON sco.case_id = sc.id
                LEFT JOIN service_branches sb ON sb.case_id = sc.id
                WHERE sc.title LIKE ? 
                   OR sc.description LIKE ? 
                   OR sc.category LIKE ?
                   OR ss.title LIKE ?
                   OR ss.description LIKE ?
                   OR sco.title LIKE ?
                   OR sco.description LIKE ?
                   OR sco.solution LIKE ?
                   OR sb.branch_name LIKE ?
                ORDER BY sc.created_at DESC
            ''', (search_term,) * 9)
        else:
            c.execute('''
                SELECT sc.*, 
                       (SELECT COUNT(*) FROM service_steps WHERE case_id = sc.id) as steps_count
                FROM service_cases sc
                ORDER BY sc.created_at DESC
            ''')
        
        cases = [dict(row) for row in c.fetchall()]
    
    return render_template_string(SERVICE_HTML, cases=cases, search_query=search_query)

@app.route('/service/add', methods=['POST'])
def service_add():
    """Pridanie novej prípadovej štúdie."""
    import sqlite3
    
    title = request.form.get('title', '').strip()
    category = request.form.get('category', '').strip()
    description = request.form.get('description', '').strip()
    
    if title:
        with sqlite3.connect('database/is_data.db') as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO service_cases (title, category, description)
                VALUES (?, ?, ?)
            ''', (title, category, description))
            case_id = c.lastrowid
        return redirect(f'/service/{case_id}')
    
    return redirect('/service')

@app.route('/service/<int:case_id>')
def service_detail(case_id):
    """Detail prípadovej štúdie."""
    import sqlite3
    
    with sqlite3.connect('database/is_data.db') as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        # Načítaj prípad
        c.execute('SELECT * FROM service_cases WHERE id = ?', (case_id,))
        case = c.fetchone()
        if not case:
            return redirect('/service')
        case = dict(case)
        
        # Načítaj kroky
        c.execute('SELECT * FROM service_steps WHERE case_id = ? ORDER BY step_number', (case_id,))
        steps = [dict(row) for row in c.fetchall()]
        
        # Načítaj komplikácie
        c.execute('SELECT * FROM service_complications WHERE case_id = ? ORDER BY id', (case_id,))
        complications = [dict(row) for row in c.fetchall()]
        
        # Načítaj vetvy (branches) pre vetvenie - s informáciou o rodičoch
        c.execute('''
            SELECT sb.*, 
                   ss.title as parent_step_title,
                   parent_branch.branch_name as parent_branch_name
            FROM service_branches sb
            LEFT JOIN service_steps ss ON ss.id = sb.parent_step_id
            LEFT JOIN service_branches parent_branch ON ss.branch_id = parent_branch.id
            WHERE sb.case_id = ? 
            ORDER BY sb.display_order
        ''', (case_id,))
        branches = [dict(row) for row in c.fetchall()]
    
    return render_template_string(SERVICE_DETAIL_HTML, case=case, steps=steps, complications=complications, branches=branches)

@app.route('/service/<int:case_id>/add-step', methods=['POST'])
def service_add_step(case_id):
    """Pridanie kroku do prípadovej štúdie."""
    import sqlite3
    import os
    from werkzeug.utils import secure_filename
    
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    branch_id = request.form.get('branch_id', '').strip()
    branch_id = int(branch_id) if branch_id else None
    
    image_path = None
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename:
            filename = secure_filename(f"case{case_id}_step_{file.filename}")
            upload_folder = os.path.join('static', 'uploads', 'service')
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, filename))
            image_path = filename
    
    if title:
        with sqlite3.connect('database/is_data.db') as conn:
            c = conn.cursor()
            # Automatické číslovanie podľa vetvy
            if branch_id:
                c.execute('SELECT COALESCE(MAX(step_number), 0) + 1 FROM service_steps WHERE case_id = ? AND branch_id = ?', (case_id, branch_id))
            else:
                c.execute('SELECT COALESCE(MAX(step_number), 0) + 1 FROM service_steps WHERE case_id = ? AND branch_id IS NULL', (case_id,))
            step_number = c.fetchone()[0]
            
            c.execute('''
                INSERT INTO service_steps (case_id, step_number, title, description, image_path, branch_id, is_decision)
                VALUES (?, ?, ?, ?, ?, ?, 0)
            ''', (case_id, step_number, title, description, image_path, branch_id))
    
    return redirect(f'/service/{case_id}')

@app.route('/service/<int:case_id>/add-decision', methods=['POST'])
def service_add_decision(case_id):
    """Pridanie rozhodovacieho bodu do prípadovej štúdie."""
    import sqlite3
    
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    branch_id = request.form.get('branch_id', '').strip()
    branch_id = int(branch_id) if branch_id else None
    
    if title:
        with sqlite3.connect('database/is_data.db') as conn:
            c = conn.cursor()
            # Automatické číslovanie podľa vetvy
            if branch_id:
                c.execute('SELECT COALESCE(MAX(step_number), 0) + 1 FROM service_steps WHERE case_id = ? AND branch_id = ?', (case_id, branch_id))
            else:
                c.execute('SELECT COALESCE(MAX(step_number), 0) + 1 FROM service_steps WHERE case_id = ? AND branch_id IS NULL', (case_id,))
            step_number = c.fetchone()[0]
            
            c.execute('''
                INSERT INTO service_steps (case_id, step_number, title, description, is_decision, branch_id)
                VALUES (?, ?, ?, ?, 1, ?)
            ''', (case_id, step_number, title, description, branch_id))
    
    return redirect(f'/service/{case_id}')

@app.route('/service/<int:case_id>/add-branch', methods=['POST'])
def service_add_branch(case_id):
    """Pridanie vetvy/možnosti k rozhodnutiu."""
    import sqlite3
    
    parent_step_id = request.form.get('parent_step_id', type=int)
    branch_name = request.form.get('branch_name', '').strip()
    branch_color = request.form.get('branch_color', '#28a745').strip()
    
    if branch_name and parent_step_id:
        with sqlite3.connect('database/is_data.db') as conn:
            c = conn.cursor()
            # Zisti poradie
            c.execute('SELECT COALESCE(MAX(display_order), 0) + 1 FROM service_branches WHERE case_id = ?', (case_id,))
            order = c.fetchone()[0]
            
            c.execute('''
                INSERT INTO service_branches (case_id, parent_step_id, branch_name, branch_color, display_order)
                VALUES (?, ?, ?, ?, ?)
            ''', (case_id, parent_step_id, branch_name, branch_color, order))
    
    return redirect(f'/service/{case_id}')

@app.route('/service/<int:case_id>/add-complication', methods=['POST'])
def service_add_complication(case_id):
    """Pridanie komplikácie do prípadovej štúdie."""
    import sqlite3
    
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    solution = request.form.get('solution', '').strip()
    branch_id = request.form.get('branch_id', '').strip()
    branch_id = int(branch_id) if branch_id else None
    
    if title:
        with sqlite3.connect('database/is_data.db') as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO service_complications (case_id, title, description, solution, branch_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (case_id, title, description, solution, branch_id))
    
    return redirect(f'/service/{case_id}')

@app.route('/service/<int:case_id>/edit-step/<int:step_id>', methods=['POST'])
def service_edit_step(case_id, step_id):
    """Editácia kroku v prípadovej štúdii."""
    import sqlite3
    
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    
    if title:
        with sqlite3.connect('database/is_data.db') as conn:
            c = conn.cursor()
            c.execute('''
                UPDATE service_steps 
                SET title = ?, description = ?
                WHERE id = ? AND case_id = ?
            ''', (title, description, step_id, case_id))
    
    return redirect(f'/service/{case_id}')

@app.route('/service/<int:case_id>/delete-step/<int:step_id>')
def service_delete_step(case_id, step_id):
    """Zmazanie kroku z prípadovej štúdie."""
    import sqlite3
    
    with sqlite3.connect('database/is_data.db') as conn:
        c = conn.cursor()
        # Najprv zmaž všetky vetvy ktoré majú tento krok ako rodiča
        c.execute('DELETE FROM service_branches WHERE parent_step_id = ?', (step_id,))
        # Potom zmaž samotný krok
        c.execute('DELETE FROM service_steps WHERE id = ? AND case_id = ?', (step_id, case_id))
    
    return redirect(f'/service/{case_id}')

# ============ ŠKOLENIA ROUTES ============

@app.route('/training')
def training():
    """Zobrazí zoznam školení."""
    import sqlite3
    
    search_query = request.args.get('q', '').strip()
    
    with sqlite3.connect('database/is_data.db') as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        if search_query:
            c.execute('''
                SELECT tc.*, COUNT(ts.id) as steps_count 
                FROM training_cases tc
                LEFT JOIN training_steps ts ON tc.id = ts.case_id
                WHERE tc.title LIKE ? OR tc.description LIKE ? OR tc.category LIKE ?
                GROUP BY tc.id
                ORDER BY tc.created_at DESC
            ''', (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%'))
        else:
            c.execute('''
                SELECT tc.*, COUNT(ts.id) as steps_count 
                FROM training_cases tc
                LEFT JOIN training_steps ts ON tc.id = ts.case_id
                GROUP BY tc.id
                ORDER BY tc.created_at DESC
            ''')
        
        cases = [dict(row) for row in c.fetchall()]
    
    return render_template_string(TRAINING_HTML, cases=cases, search_query=search_query)

@app.route('/training/add', methods=['POST'])
def training_add():
    """Pridá nové školenie."""
    import sqlite3
    
    title = request.form.get('title', '').strip()
    category = request.form.get('category', '').strip()
    difficulty = request.form.get('difficulty', 'beginner').strip()
    description = request.form.get('description', '').strip()
    
    if title:
        with sqlite3.connect('database/is_data.db') as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO training_cases (title, category, difficulty, description)
                VALUES (?, ?, ?, ?)
            ''', (title, category, difficulty, description))
    
    return redirect('/training')

@app.route('/training/<int:case_id>')
def training_detail(case_id):
    """Zobrazí detail školenia."""
    import sqlite3
    
    with sqlite3.connect('database/is_data.db') as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        c.execute('SELECT * FROM training_cases WHERE id = ?', (case_id,))
        case = c.fetchone()
        
        if not case:
            return redirect('/training')
        
        case = dict(case)
        
        c.execute('''
            SELECT * FROM training_steps WHERE case_id = ? ORDER BY display_order, id
        ''', (case_id,))
        steps = [dict(row) for row in c.fetchall()]
        
        c.execute('SELECT * FROM training_branches WHERE case_id = ?', (case_id,))
        branches = [dict(row) for row in c.fetchall()]
        
        c.execute('SELECT * FROM training_complications WHERE case_id = ?', (case_id,))
        complications = [dict(row) for row in c.fetchall()]
    
    return render_template_string(TRAINING_DETAIL_HTML, case=case, steps=steps, branches=branches, complications=complications)

@app.route('/training/<int:case_id>/add-step', methods=['POST'])
def training_add_step(case_id):
    """Pridá krok do školenia."""
    import sqlite3
    
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    step_type = request.form.get('step_type', 'step').strip()
    branch_id = request.form.get('branch_id')
    branch_id = int(branch_id) if branch_id else None
    
    if title:
        with sqlite3.connect('database/is_data.db') as conn:
            c = conn.cursor()
            
            # Zisti číslo kroku
            if branch_id:
                c.execute('SELECT COALESCE(MAX(step_number), 0) + 1 FROM training_steps WHERE case_id = ? AND branch_id = ?', (case_id, branch_id))
            else:
                c.execute('SELECT COALESCE(MAX(step_number), 0) + 1 FROM training_steps WHERE case_id = ? AND branch_id IS NULL', (case_id,))
            step_number = c.fetchone()[0]
            
            c.execute('SELECT COALESCE(MAX(display_order), 0) + 1 FROM training_steps WHERE case_id = ?', (case_id,))
            display_order = c.fetchone()[0]
            
            c.execute('''
                INSERT INTO training_steps (case_id, branch_id, step_number, title, description, step_type, display_order)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (case_id, branch_id, step_number, title, description, step_type, display_order))
    
    return redirect(f'/training/{case_id}')

@app.route('/training/<int:case_id>/add-complication', methods=['POST'])
def training_add_complication(case_id):
    """Pridá komplikáciu do školenia."""
    import sqlite3
    
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    solution = request.form.get('solution', '').strip()
    branch_id = request.form.get('branch_id', '').strip()
    branch_id = int(branch_id) if branch_id else None
    
    if title:
        with sqlite3.connect('database/is_data.db') as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO training_complications (case_id, title, description, solution, branch_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (case_id, title, description, solution, branch_id))
    
    return redirect(f'/training/{case_id}')

@app.route('/training/<int:case_id>/edit-step/<int:step_id>', methods=['POST'])
def training_edit_step(case_id, step_id):
    """Editácia kroku v školení."""
    import sqlite3
    
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    
    if title:
        with sqlite3.connect('database/is_data.db') as conn:
            c = conn.cursor()
            c.execute('''
                UPDATE training_steps 
                SET title = ?, description = ?
                WHERE id = ? AND case_id = ?
            ''', (title, description, step_id, case_id))
    
    return redirect(f'/training/{case_id}')

@app.route('/training/<int:case_id>/delete-step/<int:step_id>')
def training_delete_step(case_id, step_id):
    """Zmazanie kroku zo školenia."""
    import sqlite3
    
    with sqlite3.connect('database/is_data.db') as conn:
        c = conn.cursor()
        c.execute('DELETE FROM training_branches WHERE parent_step_id = ?', (step_id,))
        c.execute('DELETE FROM training_steps WHERE id = ? AND case_id = ?', (step_id, case_id))
    
    return redirect(f'/training/{case_id}')

@app.route('/favicon.ico')
def favicon():
    """Prázdny route pre favicon aby nebol 404 error."""
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
