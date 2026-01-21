"""
Standardabweichung und deskriptive Statistik

Berechnet Standardabweichung, Varianz, Mittelwert und weitere deskriptive Statistiken
aus einer Liste von Datenwerten.

Formeln:
- Stichprobenstandardabweichung: s = sqrt(Σ(xi - x̄)² / (n-1))
- Populationsstandardabweichung: σ = sqrt(Σ(xi - μ)² / n)
- Varianz: s² bzw. σ²
"""

import sys
import math
import statistics


def parse_value(value):
    """Parst einen Wert, der als Zahl oder Bruch (a/b) angegeben werden kann"""
    if value in ['-', 'None', '?', '']:
        return None
    value = value.strip()
    if '/' in value:
        parts = value.split('/')
        if len(parts) != 2:
            raise ValueError(f"Ungueltiger Bruch: {value}")
        numerator = float(parts[0])
        denominator = float(parts[1])
        if denominator == 0:
            raise ValueError("Division durch Null nicht erlaubt")
        return numerator / denominator
    else:
        return float(value)


def parse_list(value):
    """Parst eine kommagetrennte Liste von Werten"""
    if value in ['-', 'None', '?', '']:
        return None
    values = [parse_value(v.strip()) for v in value.split(',')]
    return values


def berechne_deskriptive_statistik(daten, population=False):
    """
    Berechnet deskriptive Statistiken aus einer Liste von Daten
    
    Parameters:
    - daten: Liste von Zahlen
    - population: Wenn True, verwendet Populationsformeln (n im Nenner), sonst Stichprobenformeln (n-1)
    
    Returns:
    - n, mittelwert, median, varianz, standardabweichung, min, max, spannweite, quartile
    """
    if len(daten) == 0:
        raise ValueError("Datenliste darf nicht leer sein")
    
    n = len(daten)
    mittelwert = statistics.mean(daten)
    median = statistics.median(daten)
    min_wert = min(daten)
    max_wert = max(daten)
    spannweite = max_wert - min_wert
    
    # Varianz und Standardabweichung
    if population:
        # Populationsvarianz: σ² = Σ(xi - μ)² / n
        varianz = statistics.pvariance(daten)
        standardabweichung = statistics.pstdev(daten)
        typ = "Population"
    else:
        # Stichprobenvarianz: s² = Σ(xi - x̄)² / (n-1)
        varianz = statistics.variance(daten)
        standardabweichung = statistics.stdev(daten)
        typ = "Stichprobe"
    
    # Quartile
    try:
        q1 = statistics.quantiles(daten, n=4)[0]  # 25. Perzentil
        q3 = statistics.quantiles(daten, n=4)[2]     # 75. Perzentil
        iqr = q3 - q1  # Interquartilsabstand
    except:
        q1 = None
        q3 = None
        iqr = None
    
    return {
        'n': n,
        'mittelwert': mittelwert,
        'median': median,
        'varianz': varianz,
        'standardabweichung': standardabweichung,
        'min': min_wert,
        'max': max_wert,
        'spannweite': spannweite,
        'q1': q1,
        'q3': q3,
        'iqr': iqr,
        'typ': typ
    }


if __name__ == "__main__":
    print("=" * 70)
    print("STANDARDABWEICHUNG UND DESKRIPTIVE STATISTIK")
    print("=" * 70)
    print("\nBerechnet Standardabweichung, Varianz, Mittelwert und weitere")
    print("deskriptive Statistiken aus einer Liste von Datenwerten.")
    print("\nVerwendung:")
    print("  python standardabweichung.py daten=<wert1>,<wert2>,... [population=true]")
    print("\nBeispiele:")
    print("  # Stichprobenstandardabweichung (Standard)")
    print("  python standardabweichung.py daten=1,2,3,4,5")
    print("  # Populationsstandardabweichung")
    print("  python standardabweichung.py daten=1,2,3,4,5 population=true")
    
    if len(sys.argv) < 2:
        print("\n" + "=" * 70)
        print("Bitte geben Sie die erforderlichen Werte an")
        sys.exit(1)
    
    # Parse Argumente
    daten = None
    population = False
    
    for arg in sys.argv[1:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            key = key.lower().strip()
            
            if key == 'daten' or key == 'data' or key == 'values':
                daten = parse_list(value)
            elif key == 'population' or key == 'pop':
                population = value.lower() in ['true', '1', 'yes', 'ja']
            else:
                print(f"Unbekannter Parameter: {key}")
        else:
            print(f"Unbekannter Parameter: {arg}")
    
    if daten is None:
        print("\nFEHLER: daten muss angegeben werden!")
        print("\nBeispiel: python standardabweichung.py daten=1,2,3,4,5")
        sys.exit(1)
    
    if len(daten) == 0:
        print("\nFEHLER: Datenliste darf nicht leer sein!")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("EINGEGEBENE WERTE")
    print("=" * 70)
    print(f"  Daten = {daten}")
    print(f"  Anzahl Werte (n) = {len(daten)}")
    print(f"  Typ = {'Population' if population else 'Stichprobe'}")
    
    # Berechne Statistiken
    print("\n" + "=" * 70)
    print("BERECHNUNGEN")
    print("=" * 70)
    
    try:
        stats = berechne_deskriptive_statistik(daten, population)
        
        # Berechne Summe der quadrierten Abweichungen für Ausgabe
        mittelwert = stats['mittelwert']
        summe_quadrat_abweichungen = sum((x - mittelwert) ** 2 for x in daten)
        
        if population:
            print(f"  Mittelwert mu = Summe(xi) / n = {sum(daten)} / {stats['n']} = {mittelwert:.6f}")
            print(f"  Summe(xi - mu)^2 = {summe_quadrat_abweichungen:.6f}")
            print(f"  Varianz sigma^2 = Summe(xi - mu)^2 / n = {summe_quadrat_abweichungen:.6f} / {stats['n']} = {stats['varianz']:.6f}")
            print(f"  Standardabweichung sigma = sqrt(sigma^2) = sqrt({stats['varianz']:.6f}) = {stats['standardabweichung']:.6f}")
        else:
            print(f"  Mittelwert x_bar = Summe(xi) / n = {sum(daten)} / {stats['n']} = {mittelwert:.6f}")
            print(f"  Summe(xi - x_bar)^2 = {summe_quadrat_abweichungen:.6f}")
            print(f"  Varianz s^2 = Summe(xi - x_bar)^2 / (n-1) = {summe_quadrat_abweichungen:.6f} / {stats['n']-1} = {stats['varianz']:.6f}")
            print(f"  Standardabweichung s = sqrt(s^2) = sqrt({stats['varianz']:.6f}) = {stats['standardabweichung']:.6f}")
        
        if stats['q1'] is not None:
            print(f"  Q1 (25. Perzentil) = {stats['q1']:.6f}")
            print(f"  Median (50. Perzentil) = {stats['median']:.6f}")
            print(f"  Q3 (75. Perzentil) = {stats['q3']:.6f}")
            print(f"  IQR (Interquartilsabstand) = Q3 - Q1 = {stats['q3']:.6f} - {stats['q1']:.6f} = {stats['iqr']:.6f}")
        
        print("\n" + "=" * 70)
        print("ERGEBNIS")
        print("=" * 70)
        print(f"  Anzahl Werte (n) = {stats['n']}")
        print(f"  Mittelwert = {stats['mittelwert']:.6f}")
        print(f"  Median = {stats['median']:.6f}")
        print(f"  Minimum = {stats['min']:.6f}")
        print(f"  Maximum = {stats['max']:.6f}")
        print(f"  Spannweite = {stats['spannweite']:.6f}")
        if stats['q1'] is not None:
            print(f"  Q1 = {stats['q1']:.6f}")
            print(f"  Q3 = {stats['q3']:.6f}")
            print(f"  IQR = {stats['iqr']:.6f}")
        print(f"\n  === VARIANZ UND STANDARDABWEICHUNG ===")
        if population:
            print(f"  Varianz sigma^2 ({stats['typ']}) = {stats['varianz']:.6f}")
            print(f"  Standardabweichung sigma ({stats['typ']}) = {stats['standardabweichung']:.6f}")
        else:
            print(f"  Varianz s^2 ({stats['typ']}) = {stats['varianz']:.6f}")
            print(f"  Standardabweichung s ({stats['typ']}) = {stats['standardabweichung']:.6f}")
        
        print(f"\nHinweis:")
        if population:
            print(f"  Populationsformeln verwendet (n im Nenner)")
            print(f"  sigma^2 = {stats['varianz']:.6f}, sigma = {stats['standardabweichung']:.6f}")
        else:
            print(f"  Stichprobenformeln verwendet (n-1 im Nenner)")
            print(f"  s^2 = {stats['varianz']:.6f}, s = {stats['standardabweichung']:.6f}")
            print(f"  Fuer Populationsstandardabweichung verwende: population=true")
        
    except Exception as e:
        print(f"\nFEHLER: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
