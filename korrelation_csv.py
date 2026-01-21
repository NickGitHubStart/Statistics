"""
Korrelationskoeffizienten Berechnung (CSV-Version)

Berechnet verschiedene Korrelationskoeffizienten aus einer CSV-Datei:
- Pearson-Korrelationskoeffizient (Bravais-Pearson) r
- Spearman-Rangkorrelationskoeffizient rho

Formeln:
- Pearson: r = Summe(xi - x_bar)(yi - y_bar) / sqrt[Summe(xi - x_bar)^2 * Summe(yi - y_bar)^2]
- Spearman: rho = 1 - (6 * Summe d^2) / (n * (n^2 - 1)) wobei d = Rang(xi) - Rang(yi)
"""

import sys
import math
import csv
import os
from scipy.stats import pearsonr, spearmanr


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


def lade_csv_daten(dateipfad, x_spalte=None, y_spalte=None, x_index=None, y_index=None):
    """
    Laedt zwei Spalten aus einer CSV-Datei
    
    Parameters:
    - dateipfad: Pfad zur CSV-Datei
    - x_spalte: Name oder Index der x-Spalte
    - y_spalte: Name oder Index der y-Spalte
    - x_index: Index der x-Spalte (0-basiert)
    - y_index: Index der y-Spalte (0-basiert)
    
    Returns:
    - x_daten, y_daten, x_name, y_name
    """
    if not os.path.exists(dateipfad):
        raise FileNotFoundError(f"Datei nicht gefunden: {dateipfad}")
    
    x_daten = []
    y_daten = []
    x_index_final = None
    y_index_final = None
    
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
        
        # Bestimme x-Spaltenindex
        if x_spalte is not None:
            try:
                x_index_final = int(x_spalte)
            except ValueError:
                x_index_final = erste_zeile.index(x_spalte) if x_spalte in erste_zeile else None
        elif x_index is not None:
            x_index_final = int(x_index)
        else:
            # Verwende erste Spalte als Standard
            x_index_final = 0
        
        # Bestimme y-Spaltenindex
        if y_spalte is not None:
            try:
                y_index_final = int(y_spalte)
            except ValueError:
                y_index_final = erste_zeile.index(y_spalte) if y_spalte in erste_zeile else None
        elif y_index is not None:
            y_index_final = int(y_index)
        else:
            # Verwende zweite Spalte als Standard
            if len(erste_zeile) > 1:
                y_index_final = 1
            else:
                raise ValueError("Mindestens 2 Spalten erforderlich fuer Korrelation")
        
        if x_index_final is None:
            raise ValueError(f"x-Spalte '{x_spalte}' nicht gefunden in CSV")
        if y_index_final is None:
            raise ValueError(f"y-Spalte '{y_spalte}' nicht gefunden in CSV")
        
        if x_index_final >= len(erste_zeile) or y_index_final >= len(erste_zeile):
            raise ValueError(f"Spaltenindex ausserhalb des Bereichs")
        
        x_name = erste_zeile[x_index_final] if x_index_final < len(erste_zeile) else f"Spalte {x_index_final}"
        y_name = erste_zeile[y_index_final] if y_index_final < len(erste_zeile) else f"Spalte {y_index_final}"
        
        # Entferne BOM aus Spaltennamen
        x_name = x_name.replace('\ufeff', '').replace('\u200b', '')
        y_name = y_name.replace('\ufeff', '').replace('\u200b', '')
        
        # Lese Daten
        for zeile in reader:
            if len(zeile) > max(x_index_final, y_index_final):
                x_wert = zeile[x_index_final].strip() if x_index_final < len(zeile) else ""
                y_wert = zeile[y_index_final].strip() if y_index_final < len(zeile) else ""
                
                # Entferne BOM und andere unsichtbare Zeichen
                x_wert = x_wert.replace('\ufeff', '').replace('\u200b', '')
                y_wert = y_wert.replace('\ufeff', '').replace('\u200b', '')
                
                if x_wert and y_wert:  # Beide Werte muessen vorhanden sein
                    try:
                        x_daten.append(float(x_wert))
                        y_daten.append(float(y_wert))
                    except ValueError:
                        # Ignoriere nicht-numerische Werte
                        continue
    
    return x_daten, y_daten, x_name, y_name


def berechne_pearson_manuell(x, y):
    """Berechnet Pearson-Korrelationskoeffizient manuell"""
    n = len(x)
    if n != len(y):
        raise ValueError("x und y muessen die gleiche Laenge haben")
    if n < 2:
        raise ValueError("Mindestens 2 Datenpaare erforderlich")
    
    x_mean = sum(x) / n
    y_mean = sum(y) / n
    
    # Zaehler: Summe(xi - x_bar)(yi - y_bar)
    zaehler = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
    
    # Nenner: sqrt[Summe(xi - x_bar)^2 * Summe(yi - y_bar)^2]
    sum_x_quadrat = sum((x[i] - x_mean) ** 2 for i in range(n))
    sum_y_quadrat = sum((y[i] - y_mean) ** 2 for i in range(n))
    nenner = math.sqrt(sum_x_quadrat * sum_y_quadrat)
    
    if nenner == 0:
        return 0.0, zaehler, sum_x_quadrat, sum_y_quadrat, x_mean, y_mean
    
    r = zaehler / nenner
    return r, zaehler, sum_x_quadrat, sum_y_quadrat, x_mean, y_mean


def berechne_spearman_manuell(x, y):
    """Berechnet Spearman-Rangkorrelationskoeffizient manuell"""
    n = len(x)
    if n != len(y):
        raise ValueError("x und y muessen die gleiche Laenge haben")
    if n < 2:
        raise ValueError("Mindestens 2 Datenpaare erforderlich")
    
    # Raenge berechnen (bei Bindungen: Durchschnittsrang)
    def berechne_raenge(values):
        sorted_values = sorted(enumerate(values), key=lambda v: v[1])
        raenge = [0] * n
        i = 0
        while i < n:
            j = i
            # Finde alle Werte mit gleichem Wert
            while j < n and sorted_values[j][1] == sorted_values[i][1]:
                j += 1
            # Durchschnittsrang fuer Bindungen
            durchschnittsrang = (i + j + 1) / 2
            for k in range(i, j):
                raenge[sorted_values[k][0]] = durchschnittsrang
            i = j
        return raenge
    
    x_raenge = berechne_raenge(x)
    y_raenge = berechne_raenge(y)
    
    # Differenzen der Raenge
    d_quadrat_summe = sum((x_raenge[i] - y_raenge[i]) ** 2 for i in range(n))
    
    # Spearman-Formel: rho = 1 - (6 * Summe d^2) / (n * (n^2 - 1))
    if n == 1:
        rho = 1.0
    else:
        rho = 1 - (6 * d_quadrat_summe) / (n * (n * n - 1))
    
    return rho, x_raenge, y_raenge, d_quadrat_summe


if __name__ == "__main__":
    print("=" * 70)
    print("KORRELATIONSKOEFFIZIENTEN BERECHNUNG (CSV-VERSION)")
    print("=" * 70)
    print("\nBerechnet:")
    print("  - Pearson-Korrelationskoeffizient (Bravais-Pearson) r")
    print("  - Spearman-Rangkorrelationskoeffizient rho")
    print("\nVerwendung:")
    print("  python korrelation_csv.py file=<datei.csv> [x_spalte=<name|index>] [y_spalte=<name|index>]")
    print("\nBeispiele:")
    print("  # Erste und zweite Spalte verwenden")
    print("  python korrelation_csv.py file=data.csv")
    print("  # Spalten nach Namen")
    print("  python korrelation_csv.py file=data.csv x_spalte=groesse y_spalte=gewicht")
    print("  # Spalten nach Index (0-basiert)")
    print("  python korrelation_csv.py file=data.csv x_spalte=0 y_spalte=1")
    
    if len(sys.argv) < 2:
        print("\n" + "=" * 70)
        print("Bitte geben Sie die erforderlichen Werte an")
        sys.exit(1)
    
    # Parse Argumente
    dateipfad = None
    x_spalte = None
    y_spalte = None
    
    for arg in sys.argv[1:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            key = key.lower().strip()
            
            if key in ['file', 'datei', 'csv']:
                dateipfad = value
            elif key in ['x', 'x_spalte', 'x_column', 'x_col']:
                x_spalte = value
            elif key in ['y', 'y_spalte', 'y_column', 'y_col']:
                y_spalte = value
            else:
                print(f"Unbekannter Parameter: {key}")
        else:
            print(f"Unbekannter Parameter: {arg}")
    
    if dateipfad is None:
        print("\nFEHLER: file muss angegeben werden!")
        print("\nBeispiel: python korrelation_csv.py file=data.csv")
        sys.exit(1)
    
    # Lade Daten aus CSV
    try:
        x, y, x_name, y_name = lade_csv_daten(dateipfad, x_spalte=x_spalte, y_spalte=y_spalte)
    except Exception as e:
        print(f"\nFEHLER beim Laden der CSV-Datei: {e}")
        sys.exit(1)
    
    if len(x) == 0 or len(y) == 0:
        print("\nFEHLER: Keine Daten gefunden in CSV-Datei!")
        sys.exit(1)
    
    if len(x) != len(y):
        print("\nFEHLER: x und y muessen die gleiche Anzahl von Werten haben!")
        sys.exit(1)
    
    if len(x) < 2:
        print("\nFEHLER: Mindestens 2 Datenpaare erforderlich!")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("EINGEGEBENE WERTE")
    print("=" * 70)
    print(f"  CSV-Datei = {dateipfad}")
    print(f"  x-Spalte = {x_name} ({len(x)} Werte)")
    print(f"  y-Spalte = {y_name} ({len(y)} Werte)")
    
    print("\n" + "=" * 70)
    print("BERECHNUNGEN")
    print("=" * 70)
    
    # PEARSON
    try:
        r_manuell, zaehler, sum_x_quadrat, sum_y_quadrat, x_mean, y_mean = berechne_pearson_manuell(x, y)
        r_scipy, p_pearson = pearsonr(x, y)
        
        print("\n--- Pearson-Korrelationskoeffizient (Bravais-Pearson) ---")
        print(f"  x_bar (Mittelwert von x) = {x_mean:.6f}")
        print(f"  y_bar (Mittelwert von y) = {y_mean:.6f}")
        print(f"  Summe(xi - x_bar)^2 = {sum_x_quadrat:.6f}")
        print(f"  Summe(yi - y_bar)^2 = {sum_y_quadrat:.6f}")
        print(f"  Summe(xi - x_bar)(yi - y_bar) = {zaehler:.6f}")
        print(f"  r = Summe(xi - x_bar)(yi - y_bar) / sqrt[Summe(xi - x_bar)^2 * Summe(yi - y_bar)^2]")
        print(f"    = {zaehler:.6f} / sqrt({sum_x_quadrat:.6f} * {sum_y_quadrat:.6f})")
        print(f"    = {r_manuell:.6f}")
        print(f"  p-Wert = {p_pearson:.6f}")
        
    except Exception as e:
        print(f"\nFEHLER bei Pearson-Berechnung: {e}")
        sys.exit(1)
    
    # SPEARMAN
    try:
        rho_manuell, x_raenge, y_raenge, d_quadrat_summe = berechne_spearman_manuell(x, y)
        rho_scipy, p_spearman = spearmanr(x, y)
        
        print("\n--- Spearman-Rangkorrelationskoeffizient ---")
        print(f"  Raenge von x: {[f'{r:.1f}' for r in x_raenge[:10]]}{'...' if len(x_raenge) > 10 else ''}")
        print(f"  Raenge von y: {[f'{r:.1f}' for r in y_raenge[:10]]}{'...' if len(y_raenge) > 10 else ''}")
        print(f"  Summe d^2 (Summe der quadrierten Rangdifferenzen) = {d_quadrat_summe:.6f}")
        print(f"  n = {len(x)}")
        print(f"  rho = 1 - (6 * Summe d^2) / (n * (n^2 - 1))")
        print(f"      = 1 - (6 * {d_quadrat_summe:.6f}) / ({len(x)} * ({len(x)}^2 - 1))")
        print(f"      = {rho_manuell:.6f}")
        print(f"  p-Wert = {p_spearman:.6f}")
        
    except Exception as e:
        print(f"\nFEHLER bei Spearman-Berechnung: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("ERGEBNIS")
    print("=" * 70)
    print(f"  CSV-Datei = {dateipfad}")
    print(f"  x-Spalte = {x_name}")
    print(f"  y-Spalte = {y_name}")
    print(f"  Anzahl Datenpaare (n) = {len(x)}")
    print(f"\n  Pearson-Korrelationskoeffizient r = {r_manuell:.6f}")
    print(f"  p-Wert (Pearson) = {p_pearson:.6f}")
    print(f"  Spearman-Rangkorrelationskoeffizient rho = {rho_manuell:.6f}")
    print(f"  p-Wert (Spearman) = {p_spearman:.6f}")
    
    print(f"\nInterpretation:")
    print(f"  Pearson r = {r_manuell:.6f}:")
    if abs(r_manuell) < 0.1:
        print(f"    Praktisch keine Korrelation (|r| < 0.1)")
    elif abs(r_manuell) < 0.3:
        print(f"    Schwache Korrelation (0.1 <= |r| < 0.3)")
    elif abs(r_manuell) < 0.5:
        print(f"    Mittlere Korrelation (0.3 <= |r| < 0.5)")
    elif abs(r_manuell) < 0.7:
        print(f"    Starke Korrelation (0.5 <= |r| < 0.7)")
    else:
        print(f"    Sehr starke Korrelation (|r| >= 0.7)")
    
    if r_manuell > 0:
        print(f"    Positive Korrelation (r > 0)")
    elif r_manuell < 0:
        print(f"    Negative Korrelation (r < 0)")
    else:
        print(f"    Keine lineare Korrelation (r = 0)")
    
    if p_pearson < 0.05:
        print(f"  Signifikant (p < 0.05)")
    else:
        print(f"  Nicht signifikant (p >= 0.05)")
