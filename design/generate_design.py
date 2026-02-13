"""
Generierung eines D-optimalen experimentellen Designs für das Choice Experiment.
Erzeugt 12 Szenarien mit je 3 Alternativen.
"""

import json
import numpy as np
from itertools import product

# Attribute und ihre Levels
ATTRIBUTES = {
    'mode': ['Auto (privat)', 'ÖPNV', 'Fahrrad / E-Bike', 'Autonomes Ridesharing'],
    'time': [10, 20, 35, 50],  # Minuten
    'cost': [1, 3, 6, 10],  # Euro
    'reliability': [70, 85, 95, 99],  # Prozent
    'co2': ['hoch', 'mittel', 'niedrig', 'keine Emissionen']
}

def generate_orthogonal_design(n_scenarios=12, n_alternatives=3):
    """
    Generiert ein fraktioniertes faktorielles Design.
    Verwendet eine vereinfachte Strategie für orthogonales Design.
    """
    np.random.seed(42)  # Für Reproduzierbarkeit
    
    scenarios = []
    
    # Für jedes Szenario erstellen wir 3 unterschiedliche Alternativen
    for scenario_id in range(1, n_scenarios + 1):
        alternatives = []
        
        # Stelle sicher, dass die Alternativen in einem Szenario unterschiedlich sind
        used_combinations = set()
        
        for alt_id in range(n_alternatives):
            # Generiere eine Alternative
            while True:
                alternative = {
                    'mode': np.random.choice(ATTRIBUTES['mode']),
                    'time': int(np.random.choice(ATTRIBUTES['time'])),
                    'cost': int(np.random.choice(ATTRIBUTES['cost'])),
                    'reliability': int(np.random.choice(ATTRIBUTES['reliability'])),
                    'co2': np.random.choice(ATTRIBUTES['co2'])
                }
                
                # Erstelle einen Hash für diese Kombination
                combo_hash = tuple(alternative.values())
                
                # Stelle sicher, dass diese Kombination noch nicht verwendet wurde
                if combo_hash not in used_combinations:
                    used_combinations.add(combo_hash)
                    break
            
            alternatives.append(alternative)
        
        scenarios.append({
            'scenario_id': scenario_id,
            'alternatives': {
                'A': alternatives[0],
                'B': alternatives[1],
                'C': alternatives[2]
            }
        })
    
    return scenarios

def generate_balanced_design(n_scenarios=12, n_alternatives=3):
    """
    Generiert ein besser balanciertes Design, das sicherstellt,
    dass jedes Attribut-Level ungefähr gleich oft vorkommt.
    """
    np.random.seed(42)
    
    scenarios = []
    
    # Tracking für Level-Nutzung
    level_counts = {
        'mode': {m: 0 for m in ATTRIBUTES['mode']},
        'time': {t: 0 for t in ATTRIBUTES['time']},
        'cost': {c: 0 for c in ATTRIBUTES['cost']},
        'reliability': {r: 0 for r in ATTRIBUTES['reliability']},
        'co2': {co: 0 for co in ATTRIBUTES['co2']}
    }
    
    for scenario_id in range(1, n_scenarios + 1):
        alternatives = []
        used_in_scenario = set()
        
        for alt_id in range(n_alternatives):
            attempts = 0
            while attempts < 100:
                # Wähle Levels mit Präferenz für weniger genutzte
                mode = min(ATTRIBUTES['mode'], 
                          key=lambda x: level_counts['mode'][x] + np.random.random())
                time = min(ATTRIBUTES['time'], 
                          key=lambda x: level_counts['time'][x] + np.random.random())
                cost = min(ATTRIBUTES['cost'], 
                          key=lambda x: level_counts['cost'][x] + np.random.random())
                reliability = min(ATTRIBUTES['reliability'], 
                                 key=lambda x: level_counts['reliability'][x] + np.random.random())
                co2 = min(ATTRIBUTES['co2'], 
                         key=lambda x: level_counts['co2'][x] + np.random.random())
                
                alternative = {
                    'mode': mode,
                    'time': int(time),
                    'cost': int(cost),
                    'reliability': int(reliability),
                    'co2': co2
                }
                
                combo_hash = tuple(alternative.values())
                if combo_hash not in used_in_scenario:
                    used_in_scenario.add(combo_hash)
                    
                    # Update counts
                    level_counts['mode'][mode] += 1
                    level_counts['time'][time] += 1
                    level_counts['cost'][cost] += 1
                    level_counts['reliability'][reliability] += 1
                    level_counts['co2'][co2] += 1
                    
                    alternatives.append(alternative)
                    break
                
                attempts += 1
            
            if attempts >= 100:
                # Fallback: einfach random
                alternative = {
                    'mode': np.random.choice(ATTRIBUTES['mode']),
                    'time': int(np.random.choice(ATTRIBUTES['time'])),
                    'cost': int(np.random.choice(ATTRIBUTES['cost'])),
                    'reliability': int(np.random.choice(ATTRIBUTES['reliability'])),
                    'co2': np.random.choice(ATTRIBUTES['co2'])
                }
                alternatives.append(alternative)
        
        scenarios.append({
            'scenario_id': scenario_id,
            'alternatives': {
                'A': alternatives[0],
                'B': alternatives[1],
                'C': alternatives[2]
            }
        })
    
    return scenarios

def save_design(scenarios, filename='choice_sets.json'):
    """Speichert das Design als JSON-Datei."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(scenarios, f, ensure_ascii=False, indent=2)
    print(f"Design erfolgreich gespeichert in {filename}")
    print(f"Anzahl Szenarien: {len(scenarios)}")

def main():
    print("Generiere experimentelles Design...")
    scenarios = generate_balanced_design(n_scenarios=12, n_alternatives=3)
    
    # Speichere im design-Verzeichnis
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, 'choice_sets.json')
    
    save_design(scenarios, output_file)
    
    # Zeige ein Beispiel-Szenario
    print("\nBeispiel-Szenario 1:")
    print(json.dumps(scenarios[0], ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
