from flask import Flask, render_template_string, request, jsonify
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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            max-width: 600px;
            width: 100%;
        }
        h1 {
            color: #667eea;
            margin-bottom: 30px;
            text-align: center;
            font-size: 2em;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            color: #555;
            font-weight: 600;
            margin-bottom: 8px;
        }
        select, input {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s;
        }
        select:focus, input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
        }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
            box-shadow: 0 10px 20px rgba(102,126,234,0.4);
        }
        button:active {
            transform: translateY(0);
        }
        .nav-link {
            display: inline-block;
            margin-top: 20px;
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s;
        }
        .nav-link:hover {
            color: #764ba2;
        }
        .result {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        .result h2 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        .result pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            color: #333;
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
        <a href="/ai-chat" class="nav-link">💬 AI asistent →</a>
        <a href="/wiki" class="nav-link">📚 Wiki / Štruktúra →</a>
        <a href="/new-customer" class="nav-link">👤 Nový zákazník →</a>
        <a href="/customers" class="nav-link">👥 Existujúci zákazníci →</a>
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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            max-width: 800px;
            width: 100%;
        }
        h1 {
            color: #667eea;
            margin-bottom: 30px;
            text-align: center;
            font-size: 2em;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            color: #555;
            font-weight: 600;
            margin-bottom: 8px;
        }
        textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            resize: vertical;
            transition: all 0.3s;
        }
        textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
        }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
            box-shadow: 0 10px 20px rgba(102,126,234,0.4);
        }
        button:active {
            transform: translateY(0);
        }
        .nav-link {
            display: inline-block;
            margin-top: 20px;
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s;
        }
        .nav-link:hover {
            color: #764ba2;
        }
        .answer-box {
            margin-top: 30px;
            padding: 25px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 15px;
            border-left: 5px solid #667eea;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .answer-box h2 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .answer-box pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            color: #333;
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
        <a href="/" class="nav-link">← Späť na vyhľadávanie</a>
        <a href="/wiki" class="nav-link">📚 Wiki / Štruktúra →</a>
        <a href="/new-customer" class="nav-link">👤 Nový zákazník →</a>
        <a href="/customers" class="nav-link">👥 Existujúci zákazníci →</a>
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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .admin-panel {
            background: #ffffff;
            border: 2px dashed #667eea;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 30px;
        }
        .admin-panel h2 {
            color: #667eea;
            margin-bottom: 15px;
        }
        .admin-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }
        .admin-card {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 15px;
            border-left: 4px solid #667eea;
        }
        .admin-card h3 {
            color: #764ba2;
            margin-bottom: 10px;
        }
        .admin-card label {
            display: block;
            font-weight: 600;
            margin-top: 10px;
            margin-bottom: 6px;
        }
        .admin-card input, .admin-card select, .admin-card textarea {
            width: 100%;
            padding: 10px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
        }
        .admin-card button {
            margin-top: 12px;
            width: 100%;
            padding: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
        }
        .admin-note {
            margin-top: 10px;
            font-size: 0.9em;
            color: #666;
        }
        .message {
            padding: 12px 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .message.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .message.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .submodules {
            margin-top: 15px;
            padding-left: 20px;
            border-left: 2px dashed #c5c5c5;
        }
        .submodules-header {
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            padding: 10px;
            background: #f0f0f0;
            border-radius: 8px;
            margin-bottom: 10px;
            transition: background 0.3s;
        }
        .submodules-header:hover {
            background: #e0e0e0;
        }
        .toggle-btn {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            color: #764ba2;
            transition: all 0.3s;
            border-left: 3px solid #764ba2;
        }
        .submodule-name:hover {
            background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
            transform: translateX(5px);
        }
        .submodule-arrow {
            font-size: 0.8em;
            transition: transform 0.3s;
            color: #667eea;
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
            background: #ffffff;
            border-radius: 12px;
            padding: 15px;
            margin: 10px 0 12px 25px;
            border-left: 4px solid #764ba2;
        }
        .relationships {
            margin-top: 15px;
            padding-left: 50px;
        }
        .relationship-item {
            background: #ffffff;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 8px;
            border-left: 3px solid #667eea;
            font-size: 0.95em;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: #667eea;
            margin-bottom: 30px;

        {% if success_message %}
        <div class="message success">{{ success_message }}</div>
        {% endif %}
        {% if error_message %}
        <div class="message error">{{ error_message }}</div>
        {% endif %}

        <div class="admin-panel">
            <h2>🛠️ Správa modulov (admin)</h2>
            <div class="admin-note">Poznámka: Neskôr bude táto sekcia dostupná len pre administrátorov.</div>
            <div class="admin-grid">
                <div class="admin-card">
                    <h3>➕ Nový modul</h3>
                    <form method="post">
                        <input type="hidden" name="action" value="add_module">
                        <label>Názov modulu</label>
                        <input name="name" required>
                        <label>Popis</label>
                        <textarea name="description" rows="3"></textarea>
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
                        <textarea name="description" rows="3"></textarea>
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
                        <textarea name="description" rows="3"></textarea>
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
                        <textarea name="description" rows="3"></textarea>
                        <button type="submit">Pridať súvislosť</button>
                    </form>
                </div>
            </div>
        </div>
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
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s;
        }
        .nav-link:hover {
            color: #764ba2;
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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            cursor: pointer;
            color: white;
            font-weight: 600;
            font-size: 1.1em;
            transition: all 0.3s;
            box-shadow: 0 3px 10px rgba(102,126,234,0.3);
        }
        .module-name:hover {
            transform: translateX(5px);
            box-shadow: 0 5px 15px rgba(102,126,234,0.4);
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
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 15px;
            padding: 25px;
            margin: 10px 0 15px 20px;
            border-left: 5px solid #667eea;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
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
            color: #667eea;
            font-size: 1.5em;
            margin-bottom: 5px;
        }
        .module-version {
            background: #667eea;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }
        .module-description {
            color: #555;
            line-height: 1.6;
            margin-bottom: 20px;
            padding-left: 50px;
        }
        .functionalities {
            padding-left: 50px;
        }
        .functionalities h3 {
            color: #764ba2;
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        .functionality-item {
            background: white;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            border-left: 3px solid #764ba2;
            transition: all 0.3s;
        }
        .functionality-item:hover {
            box-shadow: 0 3px 10px rgba(118,75,162,0.2);
            transform: translateX(5px);
        }
        .functionality-name {
            color: #764ba2;
            font-weight: 600;
            margin-bottom: 5px;
        }
        .functionality-description {
            color: #666;
            font-size: 0.95em;
            line-height: 1.5;
        }
        .no-data {
            text-align: center;
            color: #999;
            padding: 40px;
            font-style: italic;
        }
        .stats {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
        <h1>📚 IS-Assistant Wiki</h1>
        <div class="nav-links">
            <a href="/" class="nav-link">🔍 Vyhľadávanie</a>
            <a href="/ai-chat" class="nav-link">💬 AI Asistent</a>
            <a href="/new-customer" class="nav-link">👤 Nový zákazník</a>
            <a href="/customers" class="nav-link">👥 Existujúci zákazníci</a>
        </div>
        
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
                                <textarea name="description" rows="3">{{ module.description }}</textarea>
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
                        <div style="color:#666;">{{ rel.description }}</div>
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
                                        <textarea name="description" rows="3">{{ sub.description }}</textarea>
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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            max-width: 800px;
            margin: 0 auto;
        }
        h1 {
            color: #667eea;
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
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s;
        }
        .nav-link:hover {
            color: #764ba2;
        }
        .form-step {
            margin-bottom: 25px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        .form-step.hidden {
            display: none;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            color: #555;
            font-weight: 600;
            margin-bottom: 8px;
            font-size: 1.1em;
        }
        input, select, textarea {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            transition: all 0.3s;
        }
        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
        }
        button {
            padding: 14px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
            box-shadow: 0 10px 20px rgba(102,126,234,0.4);
        }
        button.secondary {
            background: #6c757d;
        }
        .success-message {
            margin-top: 20px;
            padding: 20px;
            background: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 10px;
            color: #155724;
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
        }
        .company-box {
            background: white;
            border: 2px solid #667eea;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            position: relative;
        }
        .company-box h4 {
            color: #667eea;
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
            color: #667eea;
            font-weight: 600;
            margin-top: 30px;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
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
                <p style="color: #666; margin-bottom: 15px;">Zadajte textový súhrn z vášho stretnutia so zákazníkom. AI ho neskôr môže spracovať a doplniť jednotlivé údaje.</p>
                <div class="form-group">
                    <label>Súhrn stretnutia *</label>
                    <textarea id="summaryTextarea" name="initial_summary" required placeholder="Napr. Stretol som sa s Jánom Novákom z ABC s.r.o. so sídlom v Bratislave. Majú reštauráciu v centre s kapacitou 80 ľudí. Zákazník chce implementovať systém na rezervácie stolkov a správu inventára..." style="min-height: 120px; resize: vertical;"></textarea>
                </div>
                
                <!-- Audio nahrávanie -->
                <div style="margin-top: 15px; padding: 15px; background: #f0f0f0; border-radius: 8px;">
                    <h4 style="margin-top: 0; color: #333;">🎙️ Alebo nahrajte zvuk:</h4>
                    <div style="display: flex; gap: 10px; flex-wrap: wrap; align-items: center;">
                        <button type="button" id="recordBtn" style="background: #ef5350; color: white; border: none; padding: 10px 15px; border-radius: 6px; cursor: pointer; font-weight: 600;">● Začať nahrávanie</button>
                        <button type="button" id="stopBtn" style="background: #ff9800; color: white; border: none; padding: 10px 15px; border-radius: 6px; cursor: pointer; font-weight: 600; display: none;">⏹ Zastaviť</button>
                        <span id="recordingTime" style="color: #666; font-weight: 600;"></span>
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
                '<div class="checkbox-item"><input type="checkbox" name="branch_type_' + branchCount + '" value="ine"><label>Ine</label></div>' +
                '</div>' +
                '</div>' +
                '<div class="form-group">' +
                '<label>Poznamka (volitelne)</label>' +
                '<input type="text" name="branch_info_' + branchCount + '" placeholder="Doplnujuce informacie...">' +
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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
        h1 {
            color: #667eea;
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
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s;
        }
        .nav-link:hover {
            color: #764ba2;
        }
        .add-button {
            display: inline-block;
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 10px;
            font-weight: 600;
            transition: transform 0.2s, box-shadow 0.2s;
            margin-bottom: 30px;
        }
        .add-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102,126,234,0.4);
        }
        .customer-card {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            border-left: 5px solid #667eea;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .customer-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }
        .customer-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .customer-name {
            color: #667eea;
            font-size: 1.5em;
            font-weight: 600;
        }
        .customer-type {
            background: #764ba2;
            color: white;
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
            color: #555;
        }
        .info-label {
            font-weight: 600;
            color: #333;
            display: block;
            margin-bottom: 5px;
        }
        .customer-date {
            color: #999;
            font-size: 0.9em;
            margin-top: 10px;
        }
        .no-customers {
            text-align: center;
            padding: 60px 20px;
            color: #999;
        }
        .no-customers-icon {
            font-size: 4em;
            margin-bottom: 20px;
        }
        .company-items {
            background: white;
            border-radius: 10px;
            padding: 15px;
            margin-top: 10px;
        }
        .company-item {
            background: #f8f9fa;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 10px;
            border-left: 3px solid #667eea;
        }
        .company-item:last-child {
            margin-bottom: 0;
        }
        .company-name {
            font-weight: 600;
            color: #333;
            margin-bottom: 5px;
        }
        .company-ico {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 8px;
        }
        .business-types {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
        }
        .business-tag {
            background: #667eea;
            color: white;
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 0.8em;
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
                <div style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); padding: 12px; border-radius: 8px; margin-top: 12px; border-left: 4px solid #ff9800;">
                    <h4 style="color: #ff6f00; margin-top: 0; margin-bottom: 8px; font-size: 0.95em;">📝 Súhrn zo stretnutia:</h4>
                    <p style="margin: 0; color: #333; font-size: 0.9em; line-height: 1.4;">{{ customer.initial_summary }}</p>
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
                    <h3 style="color: #667eea; margin-bottom: 10px; font-size: 1em;">🏪 Pobočky:</h3>
                    {% for branch in customer.branches %}
                    <div class="company-item" style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-left: 4px solid #667eea;">
                        <div class="company-name" style="font-size: 1em; color: #333;">{{ branch.name }}</div>
                        <div class="company-ico" style="color: #666;">📍 {{ branch.address }}</div>
                        <div class="business-types" style="margin-top: 5px;">
                            <span class="business-tag" style="background: #667eea; color: white;">{{ branch.branch_type }}</span>
                        </div>
                        {% if branch.additional_info %}
                        <div style="margin-top: 8px; padding: 8px; background: rgba(255,255,255,0.7); border-radius: 4px; font-size: 0.85em; color: #555;">
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
            </div>
            {% endfor %}
        {% else %}
            <div class="no-customers">
                <div class="no-customers-icon">👤</div>
                <h2>Zatiaľ žiadni zákazníci</h2>
                <p style="margin-top: 10px;">Začnite pridaním prvého zákazníka</p>
            </div>
        {% endif %}
    </div>
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
            branch_type = request.form.get(f'branch_type_{branch_index}', '').strip()
            branch_info = request.form.get(f'branch_info_{branch_index}', '').strip()
            
            if branch_name and branch_address and branch_type:  # Ulož len ak má názov, adresu a typ
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

@app.route('/favicon.ico')
def favicon():
    """Prázdny route pre favicon aby nebol 404 error."""
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
