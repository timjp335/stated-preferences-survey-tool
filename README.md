# Stated Preferences Survey Tool

Ein webbasiertes Tool zur Durchführung von **Stated Preferences (SP) Experimenten** für **Future Mode Choice** im Rahmen der Verkehrsplanung.

## 📋 Übersicht

Dieses Tool ermöglicht es Studierenden und Forschenden, eigene SP-Umfragen zu erstellen und durchzuführen. Befragte treffen in 12 Szenarien Entscheidungen zwischen verschiedenen Verkehrsmitteln (Auto, ÖPNV, Fahrrad/E-Bike, Autonomes Ridesharing) mit unterschiedlichen Attributen (Reisezeit, Kosten, Zuverlässigkeit, CO₂-Ausstoß).

## ✨ Features

- 🌐 **Webbasiert**: Flask-Anwendung, lokal oder auf einem Server
- 📊 **4-teilige Umfrage**: Soziodemografie, Mobilitätsverhalten, 12 Choice-Szenarien, Einstellungen
- 🎨 **Modernes Design**: Responsive, visuell ansprechend, intuitive Bedienung
- 📈 **D-optimales Design**: Wissenschaftlich fundiertes experimentelles Design
- 💾 **CSV-Export**: Alle Daten werden strukturiert als CSV gespeichert
- 📓 **Analyse-Notebook**: Jupyter Notebook mit Beispielanalysen und Logit-Modellen

## 🚀 Schnellstart

### Voraussetzungen

- Python 3.8 oder höher
- pip (Python Package Manager)

### Installation

1. Repository klonen oder herunterladen:
```bash
git clone https://github.com/timjp335/stated-preferences-survey-tool.git
cd stated-preferences-survey-tool
```

2. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

3. Experimentelles Design generieren:
```bash
python design/generate_design.py
```

4. Flask-Anwendung starten:
```bash
python app.py
```

5. Browser öffnen und zu folgender Adresse navigieren:
```
http://127.0.0.1:5000
```

Die Umfrage ist jetzt verfügbar! 🎉

### Optional: Flask Secret Key setzen

Für Produktivumgebungen sollte ein eigener Secret Key gesetzt werden:

```bash
export FLASK_SECRET_KEY="ihr-geheimer-schluessel-hier"
python app.py
```

Für Lehrzwecke generiert die Anwendung automatisch einen zufälligen Key.

### Optional: Debug-Modus aktivieren

Für Entwicklungszwecke kann der Debug-Modus aktiviert werden:

```bash
export FLASK_DEBUG=True
python app.py
```

**Wichtig:** Debug-Modus sollte in Produktion **nicht** aktiviert sein!

## 📁 Projektstruktur

```
stated-preferences-survey-tool/
├── app.py                          # Flask-Hauptanwendung
├── requirements.txt                # Python-Abhängigkeiten
├── README.md                       # Diese Datei
│
├── design/
│   ├── generate_design.py          # Script zur Design-Generierung
│   └── choice_sets.json            # Generierte Choice Sets (12 Szenarien)
│
├── templates/
│   ├── base.html                   # Basis-Template
│   ├── index.html                  # Startseite mit Einführung
│   ├── demographics.html           # Teil 1: Soziodemografie
│   ├── mobility.html               # Teil 2: Mobilitätsverhalten
│   ├── choice.html                 # Teil 3: Choice-Experiment
│   ├── attitudes.html              # Teil 4: Einstellungsfragen
│   └── thankyou.html               # Danke-Seite
│
├── static/
│   ├── css/
│   │   └── style.css               # Modernes Styling
│   └── js/
│       └── survey.js               # Frontend-Validierung
│
├── data/
│   ├── .gitkeep                    # Platzhalter
│   └── responses.csv               # Gesammelte Antworten (wird beim ersten Start erstellt)
│
└── analysis/
    └── analysis_starter.ipynb      # Jupyter Notebook für Datenanalyse
```

## 🎯 Umfrage-Struktur

### Teil 1: Soziodemografie (~2 Minuten)
- Alter
- Geschlecht
- Wohnort (städtisch/vorstädtisch/ländlich)
- Führerscheinbesitz
- Auto-Verfügbarkeit

### Teil 2: Mobilitätsverhalten (~2 Minuten)
- Hauptverkehrsmittel
- Pendelstrecke in km
- ÖPNV-Nutzungshäufigkeit
- Erfahrung mit Sharing-Diensten

### Teil 3: Choice-Experiment (~5 Minuten)
12 Szenarien mit je 3 Alternativen + "Keine davon"-Option

**Attribute und Levels:**

| Attribut | Level 1 | Level 2 | Level 3 | Level 4 |
|----------|---------|---------|---------|---------|
| Verkehrsmittel | Auto (privat) | ÖPNV | Fahrrad / E-Bike | Autonomes Ridesharing |
| Reisezeit | 10 min | 20 min | 35 min | 50 min |
| Kosten | 1 € | 3 € | 6 € | 10 € |
| Zuverlässigkeit | 70% | 85% | 95% | 99% |
| CO₂-Ausstoß | hoch | mittel | niedrig | keine Emissionen |

### Teil 4: Einstellungen (~1 Minute)
4 Fragen auf 5-Punkt-Likert-Skala:
- Umweltbewusstsein
- Technikaffinität
- Offenheit für autonomes Fahren
- Preissensibilität

**Gesamtdauer:** ca. 10 Minuten

## 💾 Datenformat

Die Daten werden im **Long-Format** gespeichert (eine Zeile pro Szenario pro Befragtem):

```csv
respondent_id,timestamp,age,gender,location,...,scenario_id,alt_a_mode,alt_a_time,...,choice
```

- `respondent_id`: Eindeutige UUID für jeden Befragten
- `choice`: Gewählte Alternative (A, B, C, oder none)
- Vollständige Attribute für alle drei Alternativen pro Szenario

### Daten herunterladen

Gesammelte Daten können über die Admin-Route abgerufen werden:
```
http://127.0.0.1:5000/admin/data
```

Dies lädt die `responses.csv` Datei herunter.

Zusätzlich gibt es einen gesammelten Export mit **einer Zeile pro Befragtem**:
```
http://127.0.0.1:5000/admin/data-aggregated
```

Dies lädt die `survey_responses_aggregated.csv` Datei herunter.

### Export zurücksetzen (clear)

Der Export wird durch Stoppen von localhost **nicht** automatisch geleert, da die Daten in `data/responses.csv` gespeichert bleiben.

Zum Zurücksetzen der gespeicherten Umfragedaten gibt es eine Admin-Route:
```
http://127.0.0.1:5000/admin/clear-data
```

Diese Route setzt die Datei auf den CSV-Header zurück (alle bisherigen Antworten werden gelöscht).

## 📊 Datenanalyse

### Jupyter Notebook starten

```bash
cd analysis
jupyter notebook analysis_starter.ipynb
```

Das Notebook enthält:
- Daten laden und vorbereiten
- Deskriptive Statistik
- Visualisierungen
- Vorbereitung für Discrete Choice Modelle
- Beispiel eines Multinomial Logit (MNL) Modells

### Empfohlene Bibliotheken für Discrete Choice Modelle

Für professionelle Analysen empfehlen wir:
- **pylogit**: Python-Bibliothek für Discrete Choice Modelle
- **biogeme**: Umfassende Software für Discrete Choice Modellierung
- **xlogit**: Mixed Logit Modelle mit GPU-Beschleunigung

Installation:
```bash
pip install pylogit
# oder
pip install biogeme
```

## 🔧 Anpassungen

### Experimentelles Design ändern

Das Design kann in `design/generate_design.py` angepasst werden:
- Anzahl der Szenarien ändern
- Andere Attribute/Levels definieren
- D-Optimierung anpassen

Nach Änderungen erneut ausführen:
```bash
python design/generate_design.py
```

### Design anpassen

CSS in `static/css/style.css` anpassen für:
- Farben ändern (CSS-Variablen am Anfang der Datei)
- Layout-Anpassungen
- Responsive Design für mobile Geräte

## 🎓 Für die Lehre

Dieses Tool eignet sich hervorragend für:
- Vorlesungen zur Verkehrsplanung
- Seminare zu Discrete Choice Modellen
- Praktische Übungen zur Umfragegestaltung
- Studentische Forschungsprojekte

### Didaktische Elemente
- Praxisnahe Anwendung von SP-Methoden
- Verständnis für experimentelles Design
- Datensammlung und -analyse
- Interpretation von Logit-Modellen

## 🔐 Datenschutz

- Alle Antworten sind anonym (UUID-basiert)
- Keine personenbezogenen Daten werden erfasst
- Daten werden lokal gespeichert
- Für Lehrzwecke optimiert (keine komplexe Authentifizierung)

**Wichtig:** Bei Verwendung mit echten Probanden bitte lokale Datenschutzrichtlinien beachten!

## 🛠️ Technologie-Stack

- **Backend**: Python 3.8+, Flask 3.0+
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Design**: NumPy für experimentelles Design
- **Analyse**: Pandas, Matplotlib, Seaborn, Jupyter
- **Datenformat**: CSV

## 📝 Lizenz

MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 🤝 Beiträge

Verbesserungsvorschläge und Pull Requests sind willkommen!

## 📧 Kontakt

Bei Fragen oder Problemen bitte ein Issue auf GitHub erstellen.

## 🙏 Danksagungen

Dieses Tool wurde für Lehrzwecke im Bereich Verkehrsplanung entwickelt und basiert auf etablierten Methoden der Stated Preferences Forschung.

---

**Viel Erfolg bei Ihrer SP-Umfrage! 🚗🚌🚲🤖**
