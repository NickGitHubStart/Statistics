"""
Binomialverteilung - Wahrscheinlichkeitsberechnungen

Dieses Script berechnet verschiedene Wahrscheinlichkeiten für die Binomialverteilung
und löst die Aufgaben 33.
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import argparse
from scipy.stats import binom


def binomial_kumulativ(n, p_erfolg, k_max, art="höchstens"):
    """
    Berechnet kumulative Binomialwahrscheinlichkeit
    
    Parameter:
    n         : Anzahl der Versuche
    p_erfolg  : Erfolgswahrscheinlichkeit pro Versuch (0 bis 1)
    k_max     : Grenze (inklusive)
    art       : "höchstens", "mindestens", "genau", "mehr_als", "weniger_als"
    
    Rückgabe: Wahrscheinlichkeit
    """
    p = p_erfolg
    q = 1 - p
    
    if art == "höchstens":
        return binom.cdf(k_max, n, p)          # P(X <= k_max)
    
    elif art == "mindestens":
        return 1 - binom.cdf(k_max-1, n, p)    # P(X >= k_max) = 1 - P(X <= k_max-1)
    
    elif art == "genau":
        return binom.pmf(k_max, n, p)          # P(X = k_max)
    
    elif art == "mehr_als":
        return 1 - binom.cdf(k_max, n, p)      # P(X > k_max) = 1 - P(X <= k_max)
    
    elif art == "weniger_als":
        return binom.cdf(k_max-1, n, p)        # P(X < k_max) = P(X <= k_max-1)
    
    else:
        raise ValueError(f"Ungültige Art: {art}. Erlaubt: 'höchstens', 'mindestens', 'genau', 'mehr_als', 'weniger_als'")


def aufgabe_1():
    """
    Aufgabe 1: Jäger mit 40% Trefferwahrscheinlichkeit
    Wie hoch ist die Wahrscheinlichkeit, dass er bei 10 Schüssen mehr als sechs Treffer hat?
    """
    print("=" * 70)
    print("AUFGABE 1: Jäger mit Trefferwahrscheinlichkeit")
    print("=" * 70)
    
    n = 10              # Anzahl der Schüsse
    p = 0.4             # Trefferwahrscheinlichkeit
    k = 6               # Mehr als 6 Treffer = mindestens 7 Treffer
    
    print(f"\nParameter:")
    print(f"  n (Anzahl Versuche) = {n}")
    print(f"  p (Erfolgswahrscheinlichkeit) = {p}")
    print(f"  Gesucht: P(X > {k}) = P(X >= {k+1})")
    
    # Mehr als 6 Treffer = mindestens 7 Treffer
    wahrscheinlichkeit = binomial_kumulativ(n, p, k+1, art="mindestens")
    
    print(f"\nErgebnis:")
    print(f"  P(X > {k}) = P(X >= {k+1}) = {wahrscheinlichkeit:.6f}")
    print(f"  P(X > {k}) = {wahrscheinlichkeit*100:.2f}%")
    
    print(f"\nVerteilung: Binomialverteilung")
    print(f"  Grund: Jeder Schuss ist ein unabhängiger Versuch mit zwei möglichen")
    print(f"         Ergebnissen (Treffer/Miss) und konstanter Erfolgswahrscheinlichkeit.")
    print(f"  B({n}, {p})")
    
    # Zusätzliche Details
    print(f"\nDetaillierte Berechnung:")
    for i in range(k+1, n+1):
        p_exakt = binomial_kumulativ(n, p, i, art="genau")
        print(f"  P(X = {i}) = {p_exakt:.6f}")
    
    return wahrscheinlichkeit


def aufgabe_2():
    """
    Aufgabe 2: Drahtlose Datenübertragung
    Mit welcher Wahrscheinlichkeit werden höchstens zwei Zeichen falsch übertragen,
    wenn eine Nachricht aus acht Zeichen besteht (p = 0.9 für richtige Übertragung)?
    """
    print("\n" + "=" * 70)
    print("AUFGABE 2: Drahtlose Datenübertragung")
    print("=" * 70)
    
    n = 8               # Anzahl der Zeichen
    p_richtig = 0.9     # Wahrscheinlichkeit für richtige Übertragung
    p_falsch = 1 - p_richtig  # Wahrscheinlichkeit für falsche Übertragung
    k_max = 2           # Höchstens 2 Fehler
    
    print(f"\nParameter:")
    print(f"  n (Anzahl Zeichen) = {n}")
    print(f"  p (richtige Übertragung) = {p_richtig}")
    print(f"  p (falsche Übertragung) = {p_falsch}")
    print(f"  Gesucht: P(X <= {k_max}) für Fehler")
    
    # Berechnung mit Fehlerwahrscheinlichkeit
    wahrscheinlichkeit = binomial_kumulativ(n, p_falsch, k_max, art="höchstens")
    
    print(f"\nErgebnis:")
    print(f"  P(X <= {k_max} Fehler) = {wahrscheinlichkeit:.6f}")
    print(f"  P(X <= {k_max} Fehler) = {wahrscheinlichkeit*100:.2f}%")
    
    print(f"\nVerteilung: Binomialverteilung")
    print(f"  Grund: Jedes Zeichen wird unabhängig übertragen mit zwei möglichen")
    print(f"         Ergebnissen (richtig/falsch) und konstanter Fehlerwahrscheinlichkeit.")
    print(f"  B({n}, {p_falsch})")
    
    # Detaillierte Berechnung
    print(f"\nDetaillierte Berechnung:")
    for i in range(0, k_max+1):
        p_exakt = binomial_kumulativ(n, p_falsch, i, art="genau")
        print(f"  P(X = {i} Fehler) = {p_exakt:.6f}")
    
    return wahrscheinlichkeit


def plot_binomial_verteilung(n, p, k_max=None, art="genau", save_file=None):
    """
    Erstellt einen Graph für die Binomialverteilung
    
    Parameter:
    n         : Anzahl der Versuche
    p         : Erfolgswahrscheinlichkeit
    k_max     : Optional: spezifischer Wert für Berechnung
    art       : Art der Berechnung (wenn k_max angegeben)
    save_file : Optional: Dateiname zum Speichern
    """
    k_werte = np.arange(0, n + 1)
    wahrscheinlichkeiten = [binom.pmf(k, n, p) for k in k_werte]
    
    plt.figure(figsize=(12, 6))
    
    # Wahrscheinlichkeitsfunktion
    plt.subplot(1, 2, 1)
    plt.bar(k_werte, wahrscheinlichkeiten, alpha=0.7, color='steelblue', edgecolor='black')
    plt.xlabel('k (Anzahl Erfolge)', fontsize=12)
    plt.ylabel('P(X = k)', fontsize=12)
    plt.title(f'Binomialverteilung B({n}, {p:.2f})\nWahrscheinlichkeitsfunktion', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='y')
    plt.xticks(k_werte)
    
    # Markiere k_max falls angegeben
    if k_max is not None:
        p_wert = binomial_kumulativ(n, p, k_max, art=art)
        plt.bar(k_max, binom.pmf(k_max, n, p), alpha=1.0, color='red', edgecolor='black', linewidth=2)
        plt.axvline(k_max, color='red', linestyle='--', linewidth=1, alpha=0.7)
        plt.text(k_max, max(wahrscheinlichkeiten) * 0.9, f'k={k_max}\nP={p_wert:.4f}', 
                ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    # Kumulative Verteilungsfunktion
    plt.subplot(1, 2, 2)
    kumulative = [binom.cdf(k, n, p) for k in k_werte]
    plt.plot(k_werte, kumulative, 'o-', linewidth=2, markersize=6, color='darkgreen')
    plt.xlabel('k (Anzahl Erfolge)', fontsize=12)
    plt.ylabel('P(X <= k)', fontsize=12)
    plt.title(f'Binomialverteilung B({n}, {p:.2f})\nKumulative Verteilungsfunktion', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.xticks(k_werte)
    plt.ylim(-0.05, 1.05)
    
    # Markiere k_max falls angegeben
    if k_max is not None:
        p_wert = binomial_kumulativ(n, p, k_max, art=art)
        plt.axvline(k_max, color='red', linestyle='--', linewidth=2, alpha=0.7)
        plt.plot(k_max, binom.cdf(k_max, n, p), 'ro', markersize=10)
        plt.text(k_max, 0.1, f'k={k_max}\nP={p_wert:.4f}', 
                ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    
    if save_file:
        plt.savefig(save_file, dpi=300, bbox_inches='tight')
        print(f"\nGraph gespeichert als: '{save_file}'")
    else:
        filename = f'binomial_n{n}_p{p:.2f}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"\nGraph gespeichert als: '{filename}'")
    
    plt.show()


def aufgabe_2_visualisierung():
    """
    Visualisierung: Wahrscheinlichkeitsdichtefunktion für fehlerfreie Übertragung
    für p von 0.0 bis 1.0 in Schritten von 0.1
    """
    print("\n" + "=" * 70)
    print("AUFGABE 2: Visualisierung - Wahrscheinlichkeit für fehlerfreie Übertragung")
    print("=" * 70)
    
    n = 8               # Anzahl der Zeichen
    p_werte = np.arange(0.0, 1.1, 0.1)  # p von 0.0 bis 1.0 in Schritten von 0.1
    wahrscheinlichkeiten = []
    
    print(f"\nBerechnung für n = {n} Zeichen:")
    print(f"{'p (richtig)':<12} {'P(0 Fehler)':<15} {'P(0 Fehler) [%]':<15}")
    print("-" * 45)
    
    for p in p_werte:
        # Wahrscheinlichkeit für 0 Fehler = alle Zeichen richtig
        p_0_fehler = binomial_kumulativ(n, p, 0, art="genau")
        wahrscheinlichkeiten.append(p_0_fehler)
        print(f"{p:<12.1f} {p_0_fehler:<15.6f} {p_0_fehler*100:<15.2f}")
    
    # Visualisierung
    plt.figure(figsize=(10, 6))
    plt.plot(p_werte, wahrscheinlichkeiten, 'b-o', linewidth=2, markersize=8)
    plt.xlabel('Wahrscheinlichkeit p für richtige Übertragung eines Zeichens', fontsize=12)
    plt.ylabel('Wahrscheinlichkeit P(0 Fehler)', fontsize=12)
    plt.title(f'Wahrscheinlichkeit für fehlerfreie Übertragung (n = {n} Zeichen)', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.xlim(-0.05, 1.05)
    plt.ylim(-0.05, 1.05)
    
    # Zusätzliche Markierung für p = 0.9
    p_spezial = 0.9
    p_0_fehler_spezial = binomial_kumulativ(n, p_spezial, 0, art="genau")
    plt.plot(p_spezial, p_0_fehler_spezial, 'ro', markersize=12, label=f'p = {p_spezial}')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('binomial_aufgabe2_visualisierung.png', dpi=300, bbox_inches='tight')
    print(f"\nVisualisierung gespeichert als: 'binomial_aufgabe2_visualisierung.png'")
    plt.show()
    
    return p_werte, wahrscheinlichkeiten


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
            n = None
            p = None
            art = 'genau'
            create_graph = False
            
            for arg in sys.argv[1:]:
                if arg == '--graph':
                    create_graph = True
                    continue
                if '=' in arg:
                    key, value = arg.split('=', 1)
                    key = key.lower().strip()
                    
                    # Test-Art wird nicht als Zahl geparst
                    if key in ['art', 'test', 'type']:
                        art = value.strip().lower()
                        continue
                    
                    try:
                        parsed_value = parse_value(value)
                        if key in ['k']:
                            k = int(parsed_value) if parsed_value is not None else None
                        elif key in ['n']:
                            n = int(parsed_value) if parsed_value is not None else None
                        elif key in ['p', 'p_erfolg', 'erfolgswahrscheinlichkeit']:
                            p = parsed_value
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
            
            # Validierung der erforderlichen Parameter
            if k is None or n is None or p is None:
                print("FEHLER: k, n und p müssen angegeben werden!")
                print("Verwendung: python binomial.py k=<wert> n=<wert> p=<wert> [art=<wert>] [--graph]")
                sys.exit(1)
            
            print("=" * 70)
            print("BINOMIALVERTEILUNG - Berechnung")
            print("=" * 70)
            print(f"\nParameter:")
            print(f"  k = {k}")
            print(f"  n (Anzahl Versuche) = {n}")
            print(f"  p (Erfolgswahrscheinlichkeit) = {p}")
            print(f"  Art = {art}")
            
            # Validierung
            if not 0 <= p <= 1:
                print(f"\nFEHLER: p muss zwischen 0 und 1 liegen!")
                sys.exit(1)
            if k < 0 or k > n:
                print(f"\nFEHLER: k muss zwischen 0 und {n} liegen!")
                sys.exit(1)
            
            # Berechnung
            wahrscheinlichkeit = binomial_kumulativ(n, p, k, art=art)
            
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
            
            print(f"\nVerteilung: Binomialverteilung B({n}, {p})")
            
            # Graph erstellen falls gewünscht
            if create_graph:
                plot_binomial_verteilung(n, p, k_max=k, art=art)
            else:
                print(f"\nTipp: Verwende --graph um einen Graph zu erstellen")
                print(f"Beispiel: python binomial.py {k} {n} {p} {art} --graph")
        
        except (ValueError, IndexError) as e:
            print("=" * 70)
            print("BINOMIALVERTEILUNG - Verwendung")
            print("=" * 70)
            print("\nVerwendung:")
            print("  python binomial.py k=<wert> n=<wert> p=<wert> [art=<wert>] [--graph]")
            print("\nParameter:")
            print("  k        : Anzahl Erfolge")
            print("  n        : Anzahl Versuche")
            print("  p        : Erfolgswahrscheinlichkeit (0-1)")
            print("  art      : höchstens, mindestens, genau, mehr_als, weniger_als (Standard: genau)")
            print("  --graph  : Erstellt einen Graph")
            print("\nBeispiele:")
            print("  python binomial.py k=2 n=8 p=0.1")
            print("  python binomial.py k=2 n=8 p=0.1 art=hoechstens")
            print("  python binomial.py n=8 p=0.1 k=2 art=genau --graph")
            sys.exit(1)
    
    else:
        # Standard-Aufgaben ausführen
        wahrscheinlichkeit_1 = aufgabe_1()
        wahrscheinlichkeit_2 = aufgabe_2()
        p_werte, wahrscheinlichkeiten = aufgabe_2_visualisierung()
        
        print("\n" + "=" * 70)
        print("ZUSAMMENFASSUNG")
        print("=" * 70)
        print(f"\nAufgabe 1: P(X > 6) = {wahrscheinlichkeit_1:.6f} ({wahrscheinlichkeit_1*100:.2f}%)")
        print(f"Aufgabe 2: P(X <= 2 Fehler) = {wahrscheinlichkeit_2:.6f} ({wahrscheinlichkeit_2*100:.2f}%)")
        print("\nBeide Aufgaben verwenden die Binomialverteilung, da es sich um")
        print("unabhängige Versuche mit zwei möglichen Ergebnissen handelt.")
