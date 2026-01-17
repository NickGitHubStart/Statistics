"""
Poisson-Verteilung - Wahrscheinlichkeitsberechnungen

Dieses Script berechnet verschiedene Wahrscheinlichkeiten für die Poisson-Verteilung.

Formel: P(X = k) = (λ^k * e^(-λ)) / k!  für k = 0, 1, 2, ...
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy.stats import poisson


def poisson_kumulativ(lambda_rate, k_max, art="höchstens"):
    """
    Berechnet kumulative Poisson-Wahrscheinlichkeit
    
    Formel: P(X = k) = (λ^k * e^(-λ)) / k!
    
    Parameter:
    k_max       : Grenze (inklusive)
    lambda_rate : Mittlere Rate λ (Lambda)
    art         : "höchstens", "mindestens", "genau", "mehr_als", "weniger_als"
    
    Rückgabe: Wahrscheinlichkeit
    """
    # Validierung der Parameter
    if lambda_rate < 0:
        raise ValueError(f"lambda_rate ({lambda_rate}) darf nicht negativ sein")
    if k_max < 0:
        raise ValueError(f"k_max ({k_max}) darf nicht negativ sein")
    if k_max < 0:
        raise ValueError(f"k_max ({k_max}) darf nicht negativ sein")
    
    if art == "höchstens":
        return poisson.cdf(k_max, lambda_rate)          # P(X <= k_max)
    
    elif art == "mindestens":
        return 1 - poisson.cdf(k_max-1, lambda_rate)    # P(X >= k_max) = 1 - P(X <= k_max-1)
    
    elif art == "genau":
        return poisson.pmf(k_max, lambda_rate)          # P(X = k_max)
    
    elif art == "mehr_als":
        return 1 - poisson.cdf(k_max, lambda_rate)      # P(X > k_max) = 1 - P(X <= k_max)
    
    elif art == "weniger_als":
        return poisson.cdf(k_max-1, lambda_rate)        # P(X < k_max) = P(X <= k_max-1)
    
    else:
        raise ValueError(f"Ungültige Art: {art}. Erlaubt: 'höchstens', 'mindestens', 'genau', 'mehr_als', 'weniger_als'")


def plot_poisson_verteilung(lambda_rate, k_max=None, art="genau", save_file=None):
    """
    Erstellt einen Graph für die Poisson-Verteilung
    
    Parameter:
    lambda_rate : Mittlere Rate λ
    k_max       : Optional: spezifischer Wert für Berechnung
    art         : Art der Berechnung (wenn k_max angegeben)
    save_file   : Optional: Dateiname zum Speichern
    """
    # Bestimme sinnvollen Bereich für k (bis zu 99.9% der Wahrscheinlichkeit)
    # Für große Lambda-Werte brauchen wir mehr Werte
    max_k = max(int(lambda_rate * 3) + 10, 20) if lambda_rate > 0 else 20
    k_werte = np.arange(0, max_k + 1)
    wahrscheinlichkeiten = [poisson.pmf(k, lambda_rate) for k in k_werte]
    
    # Finde den Bereich, wo noch signifikante Wahrscheinlichkeit ist
    kumulative = np.cumsum(wahrscheinlichkeiten)
    # Schneide ab, wenn kumulative Wahrscheinlichkeit > 0.999
    cutoff = np.where(kumulative >= 0.999)[0]
    if len(cutoff) > 0:
        max_k = min(cutoff[0] + 2, max_k)
        k_werte = k_werte[:max_k+1]
        wahrscheinlichkeiten = wahrscheinlichkeiten[:max_k+1]
    
    plt.figure(figsize=(12, 6))
    
    # Wahrscheinlichkeitsfunktion
    plt.subplot(1, 2, 1)
    plt.bar(k_werte, wahrscheinlichkeiten, alpha=0.7, color='steelblue', edgecolor='black')
    plt.xlabel('k (Anzahl Ereignisse)', fontsize=12)
    plt.ylabel('P(X = k)', fontsize=12)
    plt.title(f'Poisson-Verteilung P(lambda={lambda_rate:.2f})\nWahrscheinlichkeitsfunktion', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='y')
    plt.xticks(k_werte[::max(1, len(k_werte)//10)])
    
    # Markiere k_max falls angegeben
    if k_max is not None and k_max <= max_k:
        p_wert = poisson_kumulativ(lambda_rate, k_max, art=art)
        plt.bar(k_max, poisson.pmf(k_max, lambda_rate), alpha=1.0, color='red', edgecolor='black', linewidth=2)
        plt.axvline(k_max, color='red', linestyle='--', linewidth=1, alpha=0.7)
        plt.text(k_max, max(wahrscheinlichkeiten) * 0.9, f'k={k_max}\nP={p_wert:.4f}', 
                ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    # Kumulative Verteilungsfunktion
    plt.subplot(1, 2, 2)
    kumulative = [poisson.cdf(k, lambda_rate) for k in k_werte]
    plt.plot(k_werte, kumulative, 'o-', linewidth=2, markersize=6, color='darkgreen')
    plt.xlabel('k (Anzahl Ereignisse)', fontsize=12)
    plt.ylabel('P(X <= k)', fontsize=12)
    plt.title(f'Poisson-Verteilung P(lambda={lambda_rate:.2f})\nKumulative Verteilungsfunktion', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.xticks(k_werte[::max(1, len(k_werte)//10)])
    plt.ylim(-0.05, 1.05)
    
    # Markiere k_max falls angegeben
    if k_max is not None and k_max <= max_k:
        p_wert = poisson_kumulativ(lambda_rate, k_max, art=art)
        plt.axvline(k_max, color='red', linestyle='--', linewidth=2, alpha=0.7)
        plt.plot(k_max, poisson.cdf(k_max, lambda_rate), 'ro', markersize=10)
        plt.text(k_max, 0.1, f'k={k_max}\nP={p_wert:.4f}', 
                ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    
    if save_file:
        plt.savefig(save_file, dpi=300, bbox_inches='tight')
        print(f"\nGraph gespeichert als: '{save_file}'")
    else:
        filename = f'poisson_lambda{lambda_rate:.2f}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"\nGraph gespeichert als: '{filename}'")
    
    plt.show()


def parse_number(value):
    """
    Parst eine Zahl, die als Dezimalzahl oder Bruch (a/b) angegeben werden kann
    """
    value = value.strip()
    if '/' in value:
        # Bruch: a/b
        parts = value.split('/')
        if len(parts) != 2:
            raise ValueError(f"Ungueltiger Bruch: {value}")
        numerator = float(parts[0])
        denominator = float(parts[1])
        if denominator == 0:
            raise ValueError("Division durch Null nicht erlaubt")
        return numerator / denominator
    else:
        # Normale Dezimalzahl
        return float(value)


if __name__ == "__main__":
    # Kommandozeilenargumente parsen
    if len(sys.argv) > 1:
        try:
            # Parse Argumente im key=value Format
            k = None
            lambda_rate = None
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
                        parsed_value = parse_number(value)
                        if key in ['k']:
                            k = int(parsed_value) if parsed_value is not None else None
                        elif key in ['lambda', 'lambda_rate', 'rate', 'l']:
                            lambda_rate = parsed_value
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
            if k is None or lambda_rate is None:
                print("FEHLER: k und lambda müssen angegeben werden!")
                print("Verwendung: python poisson.py k=<wert> lambda=<wert> [art=<wert>] [--graph]")
                sys.exit(1)
            
            print("=" * 70)
            print("POISSON-VERTEILUNG - Berechnung")
            print("=" * 70)
            print(f"\nParameter:")
            print(f"  k = {k}")
            print(f"  lambda (mittlere Rate) = {lambda_rate}")
            print(f"  Art = {art}")
            
            # Validierung
            if lambda_rate < 0:
                print(f"\nFEHLER: lambda muss >= 0 sein!")
                sys.exit(1)
            if k < 0:
                print(f"\nFEHLER: k muss >= 0 sein!")
                sys.exit(1)
            
            # Berechnung
            wahrscheinlichkeit = poisson_kumulativ(lambda_rate, k, art=art)
            
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
            
            print(f"\nVerteilung: Poisson-Verteilung P(lambda={lambda_rate})")
            print(f"  Formel: P(X = k) = (lambda^k * e^(-lambda)) / k!")
            
            # Graph erstellen falls gewünscht
            if create_graph:
                plot_poisson_verteilung(lambda_rate, k_max=k, art=art)
            else:
                print(f"\nTipp: Verwende --graph um einen Graph zu erstellen")
                print(f"Beispiel: python poisson.py {k} {lambda_rate} {art} --graph")
        
        except (ValueError, IndexError) as e:
            print("=" * 70)
            print("POISSON-VERTEILUNG - Verwendung")
            print("=" * 70)
            print("\nVerwendung:")
            print("  python poisson.py k lambda [art] [--graph]")
            print("\nParameter:")
            print("  k        : Anzahl Ereignisse")
            print("  lambda   : Mittlere Rate (Lambda)")
            print("  art      : höchstens, mindestens, genau, mehr_als, weniger_als (Standard: genau)")
            print("  --graph  : Erstellt einen Graph")
            print("\nBeispiele:")
            print("  python poisson.py k=3 lambda=2.5")
            print("  python poisson.py k=3 lambda=2.5 art=hoechstens")
            print("  python poisson.py lambda=2.5 k=3 art=genau --graph")
            print("\nFormel: P(X = k) = (lambda^k * e^(-lambda)) / k!")
            sys.exit(1)
    
    else:
        # Standard-Beispiel ausführen
        print("=" * 70)
        print("BEISPIEL: Poisson-Verteilung")
        print("=" * 70)
        print("\nBeispiel: In einem Call-Center kommen durchschnittlich 3 Anrufe pro Stunde.")
        print("Wie hoch ist die Wahrscheinlichkeit, dass genau 5 Anrufe in einer Stunde kommen?")
        
        lambda_rate = 3.0  # Mittlere Rate
        k = 5               # Anzahl Ereignisse
        
        print(f"\nParameter:")
        print(f"  lambda (mittlere Rate) = {lambda_rate}")
        print(f"  k (Anzahl Ereignisse) = {k}")
        
        p_genau = poisson_kumulativ(lambda_rate, k, art="genau")
        p_hoechstens = poisson_kumulativ(lambda_rate, k, art="höchstens")
        p_mindestens = poisson_kumulativ(lambda_rate, k, art="mindestens")
        p_mehr_als = poisson_kumulativ(lambda_rate, k, art="mehr_als")
        p_weniger_als = poisson_kumulativ(lambda_rate, k, art="weniger_als")
        
        print(f"\nErgebnisse:")
        print(f"  P(X = {k}) = {p_genau:.6f} ({p_genau*100:.2f}%)")
        print(f"  P(X <= {k}) = {p_hoechstens:.6f} ({p_hoechstens*100:.2f}%)")
        print(f"  P(X >= {k}) = {p_mindestens:.6f} ({p_mindestens*100:.2f}%)")
        print(f"  P(X > {k}) = {p_mehr_als:.6f} ({p_mehr_als*100:.2f}%)")
        print(f"  P(X < {k}) = {p_weniger_als:.6f} ({p_weniger_als*100:.2f}%)")
        
        print(f"\nVerwendung:")
        print(f"  poisson_kumulativ(lambda_rate={lambda_rate}, k_max={k}, art='genau')")
        
        print(f"\nVerteilung: Poisson-Verteilung")
        print(f"  Grund: Modelliert seltene Ereignisse mit bekannter mittlerer Rate.")
        print(f"         Geeignet für: Anrufe, Unfälle, Fehler, etc.")
        print(f"  P(lambda={lambda_rate})")
        print(f"\nFormel: P(X = k) = (lambda^k * e^(-lambda)) / k!")
