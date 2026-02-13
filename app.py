"""
Stated Preferences Survey Tool - Flask Application
Webbasiertes Tool für Future Mode Choice Experimente
"""

from flask import Flask, render_template, request, session, redirect, url_for, send_file
import json
import os
import csv
from datetime import datetime
import uuid

app = Flask(__name__)
# Verwende Umgebungsvariable oder generiere einen zufälligen Key für Lehrzwecke
app.secret_key = os.environ.get('FLASK_SECRET_KEY', os.urandom(24).hex())

# Lade Choice Sets beim Start
CHOICE_SETS_PATH = os.path.join(os.path.dirname(__file__), 'design', 'choice_sets.json')
with open(CHOICE_SETS_PATH, 'r', encoding='utf-8') as f:
    CHOICE_SETS = json.load(f)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
RESPONSES_FILE = os.path.join(DATA_DIR, 'responses.csv')

# CSV Header
CSV_HEADER = [
    'respondent_id', 'timestamp', 'age', 'gender', 'location', 'license', 'car_availability',
    'main_mode', 'commute_distance_km', 'pt_frequency', 'sharing_experience',
    'env_awareness', 'tech_affinity', 'autonomous_openness', 'price_sensitivity',
    'scenario_id', 
    'alt_a_mode', 'alt_a_time', 'alt_a_cost', 'alt_a_reliability', 'alt_a_co2',
    'alt_b_mode', 'alt_b_time', 'alt_b_cost', 'alt_b_reliability', 'alt_b_co2',
    'alt_c_mode', 'alt_c_time', 'alt_c_cost', 'alt_c_reliability', 'alt_c_co2',
    'choice'
]

def init_csv():
    """Initialisiert die CSV-Datei mit Header, falls sie nicht existiert."""
    if not os.path.exists(RESPONSES_FILE):
        with open(RESPONSES_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADER)

@app.route('/')
def index():
    """Startseite mit Einführung."""
    return render_template('index.html')

@app.route('/survey/demographics', methods=['GET', 'POST'])
def demographics():
    """Teil 1: Soziodemografie."""
    if request.method == 'POST':
        # Speichere Daten in Session
        session['demographics'] = {
            'age': request.form.get('age'),
            'gender': request.form.get('gender'),
            'location': request.form.get('location'),
            'license': request.form.get('license'),
            'car_availability': request.form.get('car_availability')
        }
        return redirect(url_for('mobility'))
    
    return render_template('demographics.html')

@app.route('/survey/mobility', methods=['GET', 'POST'])
def mobility():
    """Teil 2: Aktuelles Mobilitätsverhalten."""
    if 'demographics' not in session:
        return redirect(url_for('demographics'))
    
    if request.method == 'POST':
        session['mobility'] = {
            'main_mode': request.form.get('main_mode'),
            'commute_distance_km': request.form.get('commute_distance_km'),
            'pt_frequency': request.form.get('pt_frequency'),
            'sharing_experience': request.form.get('sharing_experience')
        }
        # Initialisiere Choice-Antworten
        session['choices'] = {}
        return redirect(url_for('choice', scenario_num=1))
    
    return render_template('mobility.html')

@app.route('/survey/choice/<int:scenario_num>', methods=['GET', 'POST'])
def choice(scenario_num):
    """Teil 3: Choice Experiment (Szenarien 1-12)."""
    if 'mobility' not in session:
        return redirect(url_for('mobility'))
    
    if scenario_num < 1 or scenario_num > 12:
        return redirect(url_for('attitudes'))
    
    if request.method == 'POST':
        # Speichere Choice
        choice_value = request.form.get('choice')
        if 'choices' not in session:
            session['choices'] = {}
        session['choices'][str(scenario_num)] = choice_value
        session.modified = True
        
        # Nächstes Szenario oder weiter zu Einstellungen
        if scenario_num < 12:
            return redirect(url_for('choice', scenario_num=scenario_num + 1))
        else:
            return redirect(url_for('attitudes'))
    
    # Hole das entsprechende Szenario
    scenario = CHOICE_SETS[scenario_num - 1]
    
    return render_template('choice.html', 
                          scenario=scenario, 
                          scenario_num=scenario_num,
                          total_scenarios=12)

@app.route('/survey/attitudes', methods=['GET', 'POST'])
def attitudes():
    """Teil 4: Einstellungsfragen."""
    if 'choices' not in session or len(session.get('choices', {})) != 12:
        return redirect(url_for('choice', scenario_num=1))
    
    if request.method == 'POST':
        session['attitudes'] = {
            'env_awareness': request.form.get('env_awareness'),
            'tech_affinity': request.form.get('tech_affinity'),
            'autonomous_openness': request.form.get('autonomous_openness'),
            'price_sensitivity': request.form.get('price_sensitivity')
        }
        
        # Speichere alle Daten in CSV
        save_responses()
        
        return redirect(url_for('thankyou'))
    
    return render_template('attitudes.html')

@app.route('/survey/thankyou')
def thankyou():
    """Danke-Seite nach Abschluss."""
    return render_template('thankyou.html')

def save_responses():
    """Speichert alle gesammelten Antworten in CSV (Long-Format)."""
    init_csv()
    
    # Generiere Respondent ID
    respondent_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    
    # Hole Daten aus Session
    demo = session.get('demographics', {})
    mob = session.get('mobility', {})
    att = session.get('attitudes', {})
    choices = session.get('choices', {})
    
    # Schreibe eine Zeile pro Szenario
    with open(RESPONSES_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        for scenario_num in range(1, 13):
            scenario = CHOICE_SETS[scenario_num - 1]
            choice_value = choices.get(str(scenario_num), '')
            
            # Extrahiere Alternative-Daten
            alt_a = scenario['alternatives']['A']
            alt_b = scenario['alternatives']['B']
            alt_c = scenario['alternatives']['C']
            
            row = [
                respondent_id,
                timestamp,
                demo.get('age', ''),
                demo.get('gender', ''),
                demo.get('location', ''),
                demo.get('license', ''),
                demo.get('car_availability', ''),
                mob.get('main_mode', ''),
                mob.get('commute_distance_km', ''),
                mob.get('pt_frequency', ''),
                mob.get('sharing_experience', ''),
                att.get('env_awareness', ''),
                att.get('tech_affinity', ''),
                att.get('autonomous_openness', ''),
                att.get('price_sensitivity', ''),
                scenario_num,
                alt_a['mode'], alt_a['time'], alt_a['cost'], alt_a['reliability'], alt_a['co2'],
                alt_b['mode'], alt_b['time'], alt_b['cost'], alt_b['reliability'], alt_b['co2'],
                alt_c['mode'], alt_c['time'], alt_c['cost'], alt_c['reliability'], alt_c['co2'],
                choice_value
            ]
            
            writer.writerow(row)
    
    # Lösche Session-Daten nach dem Speichern
    session.clear()

@app.route('/admin/data')
def admin_data():
    """Admin-Seite zum Herunterladen der CSV-Daten."""
    if os.path.exists(RESPONSES_FILE):
        return send_file(RESPONSES_FILE, 
                        as_attachment=True, 
                        download_name='survey_responses.csv',
                        mimetype='text/csv')
    else:
        return "Noch keine Daten vorhanden.", 404

if __name__ == '__main__':
    init_csv()
    print("=" * 60)
    print("Stated Preferences Survey Tool")
    print("=" * 60)
    print("Server läuft auf: http://127.0.0.1:5000")
    print("Admin-Daten: http://127.0.0.1:5000/admin/data")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
