"""
Standardabweichung und deskriptive Statistik (CSV-Version)

Berechnet Standardabweichung, Varianz, Mittelwert und weitere deskriptive Statistiken
aus einer CSV-Datei.

Formeln:
- Stichprobenstandardabweichung: s = sqrt(Σ(xi - x_bar)² / (n-1))
- Populationsstandardabweichung: σ = sqrt(Σ(xi - μ)² / n)
- Varianz: s² bzw. σ²
"""

import sys
import math
import statistics
import csv
import os


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


def lade_csv_daten(dateipfad, spalte=None, spaltenname=None, spaltenindex=None):
    """
    Laedt Daten aus einer CSV-Datei
    
    Parameters:
    - dateipfad: Pfad zur CSV-Datei
    - spalte: Spaltenname oder Index (wird verwendet wenn angegeben)
    - spaltenname: Name der Spalte (Alternative zu spalte)
    - spaltenindex: Index der Spalte (0-basiert, Alternative zu spalte)
    
    Returns:
    - Liste von Zahlen
    """
    if not os.path.exists(dateipfad):
        raise FileNotFoundError(f"Datei nicht gefunden: {dateipfad}")
    
    daten = []
    spalten_index = None
    
    # Versuche verschiedene Encodings
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
    f = None
    for encoding in encodings:
        try:
            f = open(dateipfad, 'r', encoding=encoding)
            break
        except:
            continue
    
    if f is None:
        raise ValueError(f"Konnte Datei nicht oeffnen: {dateipfad}")
    
    with f:
        # Versuche verschiedene Trennzeichen
        try:
            reader = csv.reader(f, delimiter=',')
            erste_zeile = next(reader)
        except:
            f.seek(0)
            reader = csv.reader(f, delimiter=';')
            erste_zeile = next(reader)
        
        # Bestimme Spaltenindex
        if spalte is not None:
            # Versuche als Index
            try:
                spalten_index = int(spalte)
            except ValueError:
                # Versuche als Spaltenname
                spalten_index = erste_zeile.index(spalte) if spalte in erste_zeile else None
        elif spaltenname is not None:
            spalten_index = erste_zeile.index(spaltenname) if spaltenname in erste_zeile else None
        elif spaltenindex is not None:
            spalten_index = int(spaltenindex)
        else:
            # Verwende erste Spalte als Standard
            spalten_index = 0
        
        if spalten_index is None:
            raise ValueError(f"Spalte '{spalte or spaltenname}' nicht gefunden in CSV")
        
        if spalten_index >= len(erste_zeile):
            raise ValueError(f"Spaltenindex {spalten_index} ausserhalb des Bereichs")
        
        spalten_name = erste_zeile[spalten_index] if spalten_index < len(erste_zeile) else f"Spalte {spalten_index}"
        
        # Lese Daten
        for zeile in reader:
            if len(zeile) > spalten_index:
                wert = zeile[spalten_index].strip()
                # Entferne BOM und andere unsichtbare Zeichen
                wert = wert.replace('\ufeff', '').replace('\u200b', '')
                if wert:  # Ignoriere leere Werte
                    try:
                        daten.append(float(wert))
                    except ValueError:
                        # Ignoriere nicht-numerische Werte
                        continue
    
    return daten, spalten_name


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
    print("STANDARDABWEICHUNG UND DESKRIPTIVE STATISTIK (CSV-VERSION)")
    print("=" * 70)
    print("\nBerechnet Standardabweichung, Varianz, Mittelwert und weitere")
    print("deskriptive Statistiken aus einer CSV-Datei.")
    print("\nVerwendung:")
    print("  python standardabweichung_csv.py file=<datei.csv> [spalte=<name|index>] [population=true]")
    print("\nBeispiele:")
    print("  # Erste Spalte verwenden")
    print("  python standardabweichung_csv.py file=data.csv")
    print("  # Spalte nach Name")
    print("  python standardabweichung_csv.py file=data.csv spalte=zeit")
    print("  # Spalte nach Index (0-basiert)")
    print("  python standardabweichung_csv.py file=data.csv spalte=0")
    print("  # Populationsstandardabweichung")
    print("  python standardabweichung_csv.py file=data.csv spalte=zeit population=true")
    
    if len(sys.argv) < 2:
        print("\n" + "=" * 70)
        print("Bitte geben Sie die erforderlichen Werte an")
        sys.exit(1)
    
    # Parse Argumente
    dateipfad = None
    spalte = None
    population = False
    
    for arg in sys.argv[1:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            key = key.lower().strip()
            
            if key in ['file', 'datei', 'csv']:
                dateipfad = value
            elif key in ['spalte', 'column', 'col']:
                spalte = value
            elif key == 'population' or key == 'pop':
                population = value.lower() in ['true', '1', 'yes', 'ja']
            else:
                print(f"Unbekannter Parameter: {key}")
        else:
            print(f"Unbekannter Parameter: {arg}")
    
    if dateipfad is None:
        print("\nFEHLER: file muss angegeben werden!")
        print("\nBeispiel: python standardabweichung_csv.py file=data.csv")
        sys.exit(1)
    
    # Lade Daten aus CSV
    try:
        daten, spalten_name = lade_csv_daten(dateipfad, spalte=spalte)
    except Exception as e:
        print(f"\nFEHLER beim Laden der CSV-Datei: {e}")
        sys.exit(1)
    
    if len(daten) == 0:
        print("\nFEHLER: Keine Daten gefunden in CSV-Datei!")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("EINGEGEBENE WERTE")
    print("=" * 70)
    print(f"  CSV-Datei = {dateipfad}")
    print(f"  Spalte = {spalten_name}")
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
            print(f"  Mittelwert mu = Summe(xi) / n = {sum(daten):.6f} / {stats['n']} = {mittelwert:.6f}")
            print(f"  Summe(xi - mu)^2 = {summe_quadrat_abweichungen:.6f}")
            print(f"  Varianz sigma^2 = Summe(xi - mu)^2 / n = {summe_quadrat_abweichungen:.6f} / {stats['n']} = {stats['varianz']:.6f}")
            print(f"  Standardabweichung sigma = sqrt(sigma^2) = sqrt({stats['varianz']:.6f}) = {stats['standardabweichung']:.6f}")
        else:
            print(f"  Mittelwert x_bar = Summe(xi) / n = {sum(daten):.6f} / {stats['n']} = {mittelwert:.6f}")
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
        print(f"  CSV-Datei = {dateipfad}")
        print(f"  Spalte = {spalten_name}")
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
