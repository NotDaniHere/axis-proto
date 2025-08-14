from flask import Flask, render_template, request, session, jsonify
import os
import json

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key_here'
app.config['LANGUAGES'] = ['ro', 'en', 'ru']

def load_translations():
    translations = {}
    base_path = os.path.dirname(os.path.abspath(__file__))
    translations_dir = os.path.join(base_path, 'translations')
    
    for lang in app.config['LANGUAGES']:
        file_path = os.path.join(translations_dir, f'{lang}.json')
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                translations[lang] = json.load(f)
        except FileNotFoundError:
            print(f"Warning: Translation file for '{lang}' not found")
            # Fallback to English
            try:
                with open(os.path.join(translations_dir, 'en.json'), 'r', encoding='utf-8') as f:
                    translations[lang] = json.load(f)
            except:
                translations[lang] = {}
    return translations

TRANSLATIONS = load_translations()

@app.route('/')
def index():
    lang = session.get('lang', 'ro')
    return render_template('index.html', 
                         lang=lang,
                         translations=TRANSLATIONS.get(lang, TRANSLATIONS['en']),
                         languages=app.config['LANGUAGES'])

@app.route('/set_language', methods=['POST'])
def set_language():
    lang = request.json.get('lang')
    if lang in app.config['LANGUAGES']:
        session['lang'] = lang
        return jsonify({'status': 'success', 'lang': lang})
    return jsonify({'status': 'error', 'message': 'Invalid language'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)