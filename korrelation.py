"""
Korrelationskoeffizienten Berechnung

Berechnet verschiedene Korrelationskoeffizienten:
- Pearson-Korrelationskoeffizient (Bravais-Pearson) r
- Spearman-Rangkorrelationskoeffizient rho

Formeln:
- Pearson: r = Summe(xi - x_bar)(yi - y_bar) / sqrt[Summe(xi - x_bar)^2 * Summe(yi - y_bar)^2]
- Spearman: rho = 1 - (6 * Summe d^2) / (n * (n^2 - 1)) wobei d = Rang(xi) - Rang(yi)
"""

import sys
import math
from scipy.stats import pearsonr, spearmanr
from scipy.stats import chi2_contingency
import numpy as np


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
    
    # Ränge berechnen (bei Bindungen: Durchschnittsrang)
    def berechne_raenge(values):
        sorted_values = sorted(enumerate(values), key=lambda v: v[1])
        raenge = [0] * n
        i = 0
        while i < n:
            j = i
            # Finde alle Werte mit gleichem Wert
            while j < n and sorted_values[j][1] == sorted_values[i][1]:
                j += 1
            # Durchschnittsrang für Bindungen
            durchschnittsrang = (i + j + 1) / 2
            for k in range(i, j):
                raenge[sorted_values[k][0]] = durchschnittsrang
            i = j
        return raenge
    
    x_raenge = berechne_raenge(x)
    y_raenge = berechne_raenge(y)
    
    # Differenzen der Ränge
    d_quadrat_summe = sum((x_raenge[i] - y_raenge[i]) ** 2 for i in range(n))
    
    # Spearman-Formel: rho = 1 - (6 * Summe d^2) / (n * (n^2 - 1))
    if n == 1:
        rho = 1.0
    else:
        rho = 1 - (6 * d_quadrat_summe) / (n * (n * n - 1))
    
    return rho, x_raenge, y_raenge, d_quadrat_summe


def berechne_kontingenzkoeffizient(kontingenztabelle):
    """
    Berechnet Kontingenzkoeffizient C aus einer Kontingenztabelle
    
    Formel: C = sqrt(χ² / (χ² + n))
    wobei χ² der Chi-Quadrat-Wert ist
    """
    # Konvertiere zu numpy array
    tabelle = np.array(kontingenztabelle)
    
    # Chi-Quadrat-Test
    chi2_wert, p_wert, df, erwartete = chi2_contingency(tabelle)
    
    n = tabelle.sum()
    
    # Kontingenzkoeffizient
    if chi2_wert + n == 0:
        C = 0.0
    else:
        C = math.sqrt(chi2_wert / (chi2_wert + n))
    
    # Korrigierter Kontingenzkoeffizient C_korr
    # C_korr = C / sqrt((min(r,c) - 1) / min(r,c))
    r, c = tabelle.shape
    min_dim = min(r, c)
    if min_dim > 1:
        C_korr = C / math.sqrt((min_dim - 1) / min_dim)
    else:
        C_korr = C
    
    return C, C_korr, chi2_wert, p_wert, df, erwartete, n


if __name__ == "__main__":
    print("=" * 70)
    print("KORRELATIONSKOEFFIZIENTEN BERECHNUNG")
    print("=" * 70)
    print("\nBerechnet:")
    print("  - Pearson-Korrelationskoeffizient (Bravais-Pearson) r")
    print("  - Spearman-Rangkorrelationskoeffizient rho")
    print("  - Kontingenzkoeffizient C (aus Kontingenztabelle)")
    print("\nVerwendung:")
    print("  # Pearson und Spearman (mit Listen)")
    print("  python korrelation.py x=1,2,3,4,5 y=2,4,6,8,10")
    print("  # Kontingenzkoeffizient (Kontingenztabelle)")
    print("  python korrelation.py kontingenz=[[10,20],[15,25]]")
    
    if len(sys.argv) < 2:
        print("\n" + "=" * 70)
        print("Bitte geben Sie die erforderlichen Werte an")
        sys.exit(1)
    
    # Parse Argumente
    x = None
    y = None
    kontingenztabelle = None
    
    for arg in sys.argv[1:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            key = key.lower().strip()
            
            if key == 'x':
                x = parse_list(value)
            elif key == 'y':
                y = parse_list(value)
            elif key == 'kontingenz':
                # Parse Kontingenztabelle: [[a,b],[c,d]]
                try:
                    # Einfaches Parsing für 2D-Array
                    value = value.strip()
                    if value.startswith('[') and value.endswith(']'):
                        # Entferne äußere Klammern
                        value = value[1:-1]
                        rows = []
                        current_row = []
                        i = 0
                        while i < len(value):
                            if value[i] == '[':
                                current_row = []
                            elif value[i] == ']':
                                rows.append([parse_value(v.strip()) for v in ''.join(current_row).split(',')])
                                current_row = []
                            elif value[i] not in [' ', '\n']:
                                current_row.append(value[i])
                            i += 1
                        kontingenztabelle = rows
                    else:
                        raise ValueError("Ungueltiges Format fuer Kontingenztabelle")
                except Exception as e:
                    print(f"FEHLER beim Parsen der Kontingenztabelle: {e}")
                    print("Format: kontingenz=[[a,b],[c,d]]")
                    sys.exit(1)
            else:
                print(f"Unbekannter Parameter: {key}")
    
    print("\n" + "=" * 70)
    print("EINGEGEBENE WERTE")
    print("=" * 70)
    
    if kontingenztabelle is not None:
        # KONTINGENZKOEFFIZIENT
        print("  Kontingenztabelle:")
        for row in kontingenztabelle:
            print(f"    {row}")
        
        try:
            C, C_korr, chi2_wert, p_wert, df, erwartete, n = berechne_kontingenzkoeffizient(kontingenztabelle)
            
            print("\n" + "=" * 70)
            print("BERECHNUNGEN")
            print("=" * 70)
            print(f"  Chi-Quadrat-Wert = {chi2_wert:.6f}")
            print(f"  p-Wert = {p_wert:.6f}")
            print(f"  Freiheitsgrade (df) = {df}")
            print(f"  Gesamtanzahl n = {n}")
            print(f"  Kontingenzkoeffizient C = sqrt(chi2 / (chi2 + n))")
            print(f"                        = sqrt({chi2_wert:.6f} / ({chi2_wert:.6f} + {n}))")
            print(f"                        = {C:.6f}")
            print(f"  Korrigierter Kontingenzkoeffizient C_korr = {C_korr:.6f}")
            
            print("\n" + "=" * 70)
            print("ERGEBNIS")
            print("=" * 70)
            print(f"  Kontingenzkoeffizient C = {C:.6f}")
            print(f"  Korrigierter Kontingenzkoeffizient C_korr = {C_korr:.6f}")
            print(f"  Chi-Quadrat-Wert = {chi2_wert:.6f}")
            print(f"  p-Wert = {p_wert:.6f}")
            print(f"\nInterpretation:")
            if C < 0.3:
                print(f"  Schwache Kontingenz (C < 0.3)")
            elif C < 0.5:
                print(f"  Mittlere Kontingenz (0.3 <= C < 0.5)")
            else:
                print(f"  Starke Kontingenz (C >= 0.5)")
            
        except Exception as e:
            print(f"\nFEHLER: {e}")
            sys.exit(1)
    
    elif x is not None and y is not None:
        # PEARSON UND SPEARMAN
        print(f"  x = {x}")
        print(f"  y = {y}")
        
        if len(x) != len(y):
            print("\nFEHLER: x und y muessen die gleiche Laenge haben!")
            sys.exit(1)
        
        if len(x) < 2:
            print("\nFEHLER: Mindestens 2 Datenpaare erforderlich!")
            sys.exit(1)
        
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
            print(f"  Raenge von x: {[f'{r:.1f}' for r in x_raenge]}")
            print(f"  Raenge von y: {[f'{r:.1f}' for r in y_raenge]}")
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
        print(f"  Pearson-Korrelationskoeffizient r = {r_manuell:.6f}")
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
    
    else:
        print("\nFEHLER: Entweder x und y ODER kontingenz muss angegeben werden!")
        print("\nBeispiele:")
        print("  python korrelation.py x=1,2,3,4,5 y=2,4,6,8,10")
        print("  python korrelation.py kontingenz=[[10,20],[15,25]]")
        sys.exit(1)
