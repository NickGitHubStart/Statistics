"""
k-Sigma-Regel (Vorhersageintervall)

Berechnet das Intervall, in dem eine einzelne Beobachtung mit gegebener Wahrscheinlichkeit liegt.

Formel: [mu - k*sigma; mu + k*sigma]
wobei k der z-Wert für die gewünschte Wahrscheinlichkeit ist.

Unterschied zu Konfidenzintervall:
- k-Sigma-Regel: Intervall für eine einzelne Beobachtung
- Konfidenzintervall: Intervall für den Mittelwert (Parameter)
"""

import sys
import math
from scipy.stats import norm


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


def berechne_k_sigma_intervall(mu, sigma, z=None, conf=None):
    """
    Berechnet k-Sigma-Intervall: [mu - k*sigma; mu + k*sigma]
    
    Parameters:
    - mu: Mittelwert
    - sigma: Standardabweichung
    - z: z-Wert (z.B. 1.96 für 95%)
    - conf: Konfidenzniveau (z.B. 0.95 oder 95 für 95%)
    
    Returns:
    - untere_grenze, obere_grenze, z_wert, wahrscheinlichkeit
    """
    if sigma <= 0:
        raise ValueError("Standardabweichung sigma muss > 0 sein")
    
    # Bestimme z-Wert
    if z is not None:
        z_wert = z
        # Berechne Wahrscheinlichkeit aus z-Wert
        wahrscheinlichkeit = norm.cdf(z_wert) - norm.cdf(-z_wert)
    elif conf is not None:
        # Konfidenzniveau gegeben (z.B. 0.95 oder 95)
        if conf > 1:
            conf = conf / 100  # Wenn als Prozent angegeben (z.B. 95 statt 0.95)
        if not 0 < conf < 1:
            raise ValueError("Konfidenzniveau muss zwischen 0 und 1 liegen (oder 0-100%)")
        wahrscheinlichkeit = conf
        # z-Wert für zweiseitiges Intervall
        z_wert = norm.ppf(1 - (1 - conf) / 2)
    else:
        raise ValueError("Entweder z oder conf muss angegeben werden")
    
    # Berechne Intervall
    untere_grenze = mu - z_wert * sigma
    obere_grenze = mu + z_wert * sigma
    
    return untere_grenze, obere_grenze, z_wert, wahrscheinlichkeit


if __name__ == "__main__":
    print("=" * 70)
    print("K-SIGMA-REGEL (VORHERSAGEINTERVALL)")
    print("=" * 70)
    print("\nBerechnet das Intervall, in dem eine einzelne Beobachtung")
    print("mit gegebener Wahrscheinlichkeit liegt.")
    print("\nFormel: [mu - k*sigma; mu + k*sigma]")
    print("\nUnterschied zu Konfidenzintervall:")
    print("  - k-Sigma-Regel: Intervall fuer eine einzelne Beobachtung")
    print("  - Konfidenzintervall: Intervall fuer den Mittelwert (Parameter)")
    print("\nVerwendung:")
    print("  python k_sigma.py mu=<wert> sigma=<wert> [z=<wert>] [conf=<wert>]")
    print("\nBeispiele:")
    print("  # Mit z-Wert")
    print("  python k_sigma.py mu=10 sigma=0.0167 z=1.96")
    print("  # Mit Konfidenzniveau (95%)")
    print("  python k_sigma.py mu=10 sigma=0.0167 conf=0.95")
    print("  # Mit Konfidenzniveau als Prozent")
    print("  python k_sigma.py mu=10 sigma=0.0167 conf=95")
    
    if len(sys.argv) < 2:
        print("\n" + "=" * 70)
        print("Bitte geben Sie die erforderlichen Werte an")
        sys.exit(1)
    
    # Parse Argumente
    mu = None
    sigma = None
    z = None
    conf = None
    
    for arg in sys.argv[1:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            key = key.lower().strip()
            
            try:
                parsed_value = parse_value(value)
                if key in ['mu', 'mittelwert', 'mean']:
                    mu = parsed_value
                elif key in ['sigma', 'std', 'standardabweichung']:
                    sigma = parsed_value
                elif key == 'z':
                    z = parsed_value
                elif key in ['conf', 'konfidenzniveau', 'wahrscheinlichkeit', 'prob', 'p']:
                    conf = parsed_value
                else:
                    print(f"Unbekannter Parameter: {key}")
            except ValueError as e:
                print(f"FEHLER beim Parsen von {key}={value}: {e}")
                sys.exit(1)
    
    # Validierung
    if mu is None:
        print("\nFEHLER: mu muss angegeben werden!")
        sys.exit(1)
    if sigma is None:
        print("\nFEHLER: sigma muss angegeben werden!")
        sys.exit(1)
    if z is None and conf is None:
        print("\nFEHLER: Entweder z oder conf muss angegeben werden!")
        sys.exit(1)
    if z is not None and conf is not None:
        print("\nWarnung: Sowohl z als auch conf wurden angegeben. z wird verwendet.")
        conf = None
    
    print("\n" + "=" * 70)
    print("EINGEGEBENE WERTE")
    print("=" * 70)
    print(f"  mu (Mittelwert) = {mu}")
    print(f"  sigma (Standardabweichung) = {sigma}")
    if z is not None:
        print(f"  z (z-Wert) = {z}")
    else:
        if conf > 1:
            print(f"  conf (Konfidenzniveau) = {conf}%")
        else:
            print(f"  conf (Konfidenzniveau) = {conf} ({conf*100}%)")
    
    # Berechne Intervall
    print("\n" + "=" * 70)
    print("BERECHNUNGEN")
    print("=" * 70)
    
    try:
        untere_grenze, obere_grenze, z_wert, wahrscheinlichkeit = berechne_k_sigma_intervall(mu, sigma, z, conf)
        
        if z is None:
            print(f"  z-Wert fuer Konfidenzniveau {conf if conf <= 1 else conf/100:.4f} = {z_wert:.6f}")
        
        print(f"  Wahrscheinlichkeit = {wahrscheinlichkeit:.6f} ({wahrscheinlichkeit*100:.2f}%)")
        print(f"  Untere Grenze = mu - z*sigma = {mu} - {z_wert:.6f} * {sigma} = {untere_grenze:.6f}")
        print(f"  Obere Grenze = mu + z*sigma = {mu} + {z_wert:.6f} * {sigma} = {obere_grenze:.6f}")
        
        print("\n" + "=" * 70)
        print("ERGEBNIS")
        print("=" * 70)
        print(f"  mu (Mittelwert) = {mu:.6f}")
        print(f"  sigma (Standardabweichung) = {sigma:.6f}")
        print(f"  z-Wert = {z_wert:.6f}")
        print(f"  Wahrscheinlichkeit = {wahrscheinlichkeit:.6f} ({wahrscheinlichkeit*100:.2f}%)")
        print(f"\n  k-Sigma-Intervall:")
        print(f"    [{untere_grenze:.6f}; {obere_grenze:.6f}]")
        print(f"\nInterpretation:")
        print(f"  Mit einer Wahrscheinlichkeit von {wahrscheinlichkeit*100:.2f}% liegt")
        print(f"  eine einzelne Beobachtung im Intervall [{untere_grenze:.6f}; {obere_grenze:.6f}]")
        
    except ValueError as e:
        print(f"\nFEHLER: {e}")
        sys.exit(1)
