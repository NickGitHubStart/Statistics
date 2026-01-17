"""
Hypergeometrische Verteilung - Wahrscheinlichkeitsberechnungen

Dieses Script berechnet verschiedene Wahrscheinlichkeiten für die hypergeometrische Verteilung.

Formel: P(X = k) = h(k | N, M, n) = (M über k) * (N-M über n-k) / (N über n)
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import argparse
from scipy.stats import hypergeom


def hypergeometrisch_kumulativ(N, M, n, k_max, art="höchstens"):
    """
    Berechnet kumulative hypergeometrische Wahrscheinlichkeit
    
    Formel: P(X = k) = h(k | N, M, n) = (M über k) * (N-M über n-k) / (N über n)
    
    Parameter:
    N         : Grundgesamtheit (Gesamtanzahl der Objekte)
    M         : Anzahl der "Erfolge" in der Grundgesamtheit
    n         : Stichprobengröße (Anzahl der gezogenen Objekte)
    k_max     : Grenze (inklusive)
    art       : "höchstens", "mindestens", "genau", "mehr_als", "weniger_als"
    
    Rückgabe: Wahrscheinlichkeit
    """
    # Validierung der Parameter
    if M > N:
        raise ValueError(f"M ({M}) darf nicht größer als N ({N}) sein")
    if n > N:
        raise ValueError(f"n ({n}) darf nicht größer als N ({N}) sein")
    if k_max < 0:
        raise ValueError(f"k_max ({k_max}) darf nicht negativ sein")
    if k_max > min(n, M):
        raise ValueError(f"k_max ({k_max}) darf nicht größer als min(n={n}, M={M})={min(n, M)} sein")
    
    if art == "höchstens":
        return hypergeom.cdf(k_max, N, M, n)          # P(X <= k_max)
    
    elif art == "mindestens":
        return 1 - hypergeom.cdf(k_max-1, N, M, n)    # P(X >= k_max) = 1 - P(X <= k_max-1)
    
    elif art == "genau":
        return hypergeom.pmf(k_max, N, M, n)          # P(X = k_max)
    
    elif art == "mehr_als":
        return 1 - hypergeom.cdf(k_max, N, M, n)      # P(X > k_max) = 1 - P(X <= k_max)
    
    elif art == "weniger_als":
        return hypergeom.cdf(k_max-1, N, M, n)        # P(X < k_max) = P(X <= k_max-1)
    
    else:
        raise ValueError(f"Ungültige Art: {art}. Erlaubt: 'höchstens', 'mindestens', 'genau', 'mehr_als', 'weniger_als'")


def plot_hypergeometrisch_verteilung(N, M, n, k_max=None, art="genau", save_file=None):
    """
    Erstellt einen Graph für die hypergeometrische Verteilung
    
    Parameter:
    N         : Grundgesamtheit
    M         : Anzahl Erfolge in Grundgesamtheit
    n         : Stichprobengröße
    k_max     : Optional: spezifischer Wert für Berechnung
    art       : Art der Berechnung (wenn k_max angegeben)
    save_file : Optional: Dateiname zum Speichern
    """
    k_werte = np.arange(0, min(n, M) + 1)
    wahrscheinlichkeiten = [hypergeom.pmf(k, N, M, n) for k in k_werte]
    
    plt.figure(figsize=(12, 6))
    
    # Wahrscheinlichkeitsfunktion
    plt.subplot(1, 2, 1)
    plt.bar(k_werte, wahrscheinlichkeiten, alpha=0.7, color='steelblue', edgecolor='black')
    plt.xlabel('k (Anzahl Erfolge)', fontsize=12)
    plt.ylabel('P(X = k)', fontsize=12)
    plt.title(f'Hypergeometrische Verteilung H({N}, {M}, {n})\nWahrscheinlichkeitsfunktion', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='y')
    plt.xticks(k_werte)
    
    # Markiere k_max falls angegeben
    if k_max is not None:
        p_wert = hypergeometrisch_kumulativ(N, M, n, k_max, art=art)
        if k_max in k_werte:
            plt.bar(k_max, hypergeom.pmf(k_max, N, M, n), alpha=1.0, color='red', edgecolor='black', linewidth=2)
            plt.axvline(k_max, color='red', linestyle='--', linewidth=1, alpha=0.7)
            plt.text(k_max, max(wahrscheinlichkeiten) * 0.9, f'k={k_max}\nP={p_wert:.4f}', 
                    ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    # Kumulative Verteilungsfunktion
    plt.subplot(1, 2, 2)
    kumulative = [hypergeom.cdf(k, N, M, n) for k in k_werte]
    plt.plot(k_werte, kumulative, 'o-', linewidth=2, markersize=6, color='darkgreen')
    plt.xlabel('k (Anzahl Erfolge)', fontsize=12)
    plt.ylabel('P(X <= k)', fontsize=12)
    plt.title(f'Hypergeometrische Verteilung H({N}, {M}, {n})\nKumulative Verteilungsfunktion', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.xticks(k_werte)
    plt.ylim(-0.05, 1.05)
    
    # Markiere k_max falls angegeben
    if k_max is not None and k_max in k_werte:
        p_wert = hypergeometrisch_kumulativ(N, M, n, k_max, art=art)
        plt.axvline(k_max, color='red', linestyle='--', linewidth=2, alpha=0.7)
        plt.plot(k_max, hypergeom.cdf(k_max, N, M, n), 'ro', markersize=10)
        plt.text(k_max, 0.1, f'k={k_max}\nP={p_wert:.4f}', 
                ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    
    if save_file:
        plt.savefig(save_file, dpi=300, bbox_inches='tight')
        print(f"\nGraph gespeichert als: '{save_file}'")
    else:
        filename = f'hypergeometrisch_N{N}_M{M}_n{n}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"\nGraph gespeichert als: '{filename}'")
    
    plt.show()


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


if __name__ == "__main__":
    # Kommandozeilenargumente parsen
    if len(sys.argv) > 1:
        try:
            # Parse Argumente im key=value Format
            k = None
            N = None
            M = None
            n = None
            art = 'genau'
            create_graph = False
            
            for arg in sys.argv[1:]:
                if arg == '--graph':
                    create_graph = True
                    continue
                if '=' in arg:
                    key, value = arg.split('=', 1)
                    key_original = key.strip()
                    key = key.lower().strip()
                    
                    # Test-Art wird nicht als Zahl geparst
                    if key in ['art', 'test', 'type']:
                        art = value.strip().lower()
                        continue
                    
                    try:
                        parsed_value = parse_value(value)
                        # Prüfe zuerst spezifische Keys
                        if key in ['k']:
                            k = int(parsed_value) if parsed_value is not None else None
                        elif key == 'n' and key_original == 'n':  # Nur kleines 'n' für Stichprobengröße
                            n = int(parsed_value) if parsed_value is not None else None
                        elif key_original.upper() == 'N' and key_original != 'n':  # Großes 'N' für Grundgesamtheit
                            N = int(parsed_value) if parsed_value is not None else None
                        elif key_original.upper() == 'M' and key_original != 'm':  # Großes 'M'
                            M = int(parsed_value) if parsed_value is not None else None
                        elif key in ['n_pop', 'n_total', 'grundgesamtheit']:
                            N = int(parsed_value) if parsed_value is not None else None
                        elif key in ['m_erfolg', 'erfolge']:
                            M = int(parsed_value) if parsed_value is not None else None
                        else:
                            print(f"Unbekannter Parameter: {key}")
                    except ValueError as e:
                        print(f"FEHLER beim Parsen von {key}={value}: {e}")
                        sys.exit(1)
            
            # Validierung der Art
            art_mapping = {
                'hoechstens': 'höchstens',
                'mindestens': 'mindestens',
                'genau': 'genau',
                'mehr_als': 'mehr_als',
                'mehr als': 'mehr_als',
                'weniger_als': 'weniger_als',
                'weniger als': 'weniger_als'
            }
            if art in art_mapping:
                art = art_mapping[art]
            elif art not in ['höchstens', 'mindestens', 'genau', 'mehr_als', 'weniger_als']:
                print(f"FEHLER: Ungueltige Art '{art}'.")
                print(f"Erlaubt: hoechstens/höchstens, mindestens, genau, mehr_als, weniger_als")
                sys.exit(1)
            
            print("=" * 70)
            print("HYPERGEOMETRISCHE VERTEILUNG - Berechnung")
            print("=" * 70)
            print(f"\nParameter:")
            print(f"  N (Grundgesamtheit) = {N}")
            print(f"  M (Anzahl Erfolge in Grundgesamtheit) = {M}")
            print(f"  n (Stichprobengröße) = {n}")
            print(f"  k = {k}")
            print(f"  Art = {art}")
            
            # Validierung
            if M > N:
                print(f"\nFEHLER: M ({M}) darf nicht größer als N ({N}) sein!")
                sys.exit(1)
            if n > N:
                print(f"\nFEHLER: n ({n}) darf nicht größer als N ({N}) sein!")
                sys.exit(1)
            if k < 0 or k > min(n, M):
                print(f"\nFEHLER: k muss zwischen 0 und {min(n, M)} liegen!")
                sys.exit(1)
            
            # Berechnung
            wahrscheinlichkeit = hypergeometrisch_kumulativ(N, M, n, k, art=art)
            
            print(f"\nErgebnis:")
            if art == "genau":
                print(f"  P(X = {k}) = {wahrscheinlichkeit:.6f} ({wahrscheinlichkeit*100:.2f}%)")
            elif art == "höchstens":
                print(f"  P(X <= {k}) = {wahrscheinlichkeit:.6f} ({wahrscheinlichkeit*100:.2f}%)")
            elif art == "mindestens":
                print(f"  P(X >= {k}) = {wahrscheinlichkeit:.6f} ({wahrscheinlichkeit*100:.2f}%)")
            elif art == "mehr_als":
                print(f"  P(X > {k}) = {wahrscheinlichkeit:.6f} ({wahrscheinlichkeit*100:.2f}%)")
            elif art == "weniger_als":
                print(f"  P(X < {k}) = {wahrscheinlichkeit:.6f} ({wahrscheinlichkeit*100:.2f}%)")
            
            print(f"\nVerteilung: Hypergeometrische Verteilung H({N}, {M}, {n})")
            
            # Graph erstellen falls gewünscht
            if create_graph:
                plot_hypergeometrisch_verteilung(N, M, n, k_max=k, art=art)
            else:
                print(f"\nTipp: Verwende --graph um einen Graph zu erstellen")
                print(f"Beispiel: python hypergeometrisch.py {k} {N} {M} {n} {art} --graph")
        
        except (ValueError, IndexError) as e:
            print("=" * 70)
            print("HYPERGEOMETRISCHE VERTEILUNG - Verwendung")
            print("=" * 70)
            print("\nVerwendung:")
            print("  python hypergeometrisch.py k=<wert> N=<wert> M=<wert> n=<wert> [art=<wert>] [--graph]")
            print("\nParameter:")
            print("  k        : Anzahl Erfolge")
            print("  N        : Grundgesamtheit")
            print("  M        : Anzahl Erfolge in Grundgesamtheit")
            print("  n        : Stichprobengröße")
            print("  art      : höchstens, mindestens, genau, mehr_als, weniger_als (Standard: genau)")
            print("  --graph  : Erstellt einen Graph")
            print("\nBeispiele:")
            print("  python hypergeometrisch.py k=3 N=20 M=12 n=5")
            print("  python hypergeometrisch.py k=3 N=20 M=12 n=5 art=hoechstens")
            print("  python hypergeometrisch.py N=20 M=12 n=5 k=3 art=genau --graph")
            sys.exit(1)
    
    else:
        # Standard-Beispiel ausführen
        print("=" * 70)
        print("BEISPIEL: Hypergeometrische Verteilung")
        print("=" * 70)
        print("\nBeispiel: Aus einer Urne mit 20 Kugeln (12 rote, 8 blaue)")
        print("werden 5 Kugeln ohne Zurücklegen gezogen.")
        print("Wie hoch ist die Wahrscheinlichkeit, genau 3 rote Kugeln zu ziehen?")
        
        N = 20  # Grundgesamtheit
        M = 12  # Anzahl rote Kugeln (Erfolge)
        n = 5   # Stichprobengröße
        k = 3   # Anzahl rote Kugeln in Stichprobe
        
        print(f"\nParameter:")
        print(f"  N (Grundgesamtheit) = {N}")
        print(f"  M (Anzahl Erfolge in Grundgesamtheit) = {M}")
        print(f"  n (Stichprobengröße) = {n}")
        print(f"  k (Anzahl Erfolge in Stichprobe) = {k}")
        
        p_genau = hypergeometrisch_kumulativ(N, M, n, k, art="genau")
        p_hoechstens = hypergeometrisch_kumulativ(N, M, n, k, art="höchstens")
        p_mindestens = hypergeometrisch_kumulativ(N, M, n, k, art="mindestens")
        p_mehr_als = hypergeometrisch_kumulativ(N, M, n, k, art="mehr_als")
        p_weniger_als = hypergeometrisch_kumulativ(N, M, n, k, art="weniger_als")
        
        print(f"\nErgebnisse:")
        print(f"  P(X = {k}) = {p_genau:.6f} ({p_genau*100:.2f}%)")
        print(f"  P(X <= {k}) = {p_hoechstens:.6f} ({p_hoechstens*100:.2f}%)")
        print(f"  P(X >= {k}) = {p_mindestens:.6f} ({p_mindestens*100:.2f}%)")
        print(f"  P(X > {k}) = {p_mehr_als:.6f} ({p_mehr_als*100:.2f}%)")
        print(f"  P(X < {k}) = {p_weniger_als:.6f} ({p_weniger_als*100:.2f}%)")
        
        print(f"\nVerwendung:")
        print(f"  hypergeometrisch_kumulativ(N={N}, M={M}, n={n}, k_max={k}, art='genau')")
        
        print(f"\nVerteilung: Hypergeometrische Verteilung")
        print(f"  Grund: Ziehen ohne Zurücklegen aus einer endlichen Grundgesamtheit.")
        print(f"         Die Wahrscheinlichkeit ändert sich mit jedem Zug.")
        print(f"  H({N}, {M}, {n})")
