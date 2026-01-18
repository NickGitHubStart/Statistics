"""
Z-Score Berechnung

Berechnet Z-Score, Mittelwert, Standardabweichung oder x-Wert
je nachdem welche Werte gegeben sind.

Formel: z = (x - μ) / σ
"""

import sys
import math
from scipy.stats import norm


def berechne_z_score(x, mu, sigma):
    """Berechnet Z-Score: z = (x - mu) / sigma"""
    if sigma == 0:
        raise ValueError("Standardabweichung darf nicht 0 sein")
    return (x - mu) / sigma


def berechne_x(z, mu, sigma):
    """Berechnet x-Wert: x = mu + z * sigma"""
    return mu + z * sigma


def berechne_mu(x, z, sigma):
    """Berechnet Mittelwert: mu = x - z * sigma"""
    return x - z * sigma


def berechne_sigma(x, mu, z):
    """Berechnet Standardabweichung: sigma = (x - mu) / z"""
    if z == 0:
        raise ValueError("Z-Score darf nicht 0 sein (x waere gleich mu)")
    return (x - mu) / z


def berechne_wahrscheinlichkeit(z):
    """Berechnet Wahrscheinlichkeit (Flächeninhalt) für Z-Wert: P(Z <= z) = Φ(z)"""
    return norm.cdf(z)


def berechne_z_aus_wahrscheinlichkeit(p):
    """Berechnet Z-Wert aus Wahrscheinlichkeit: z = Φ^(-1)(p)"""
    if not 0 <= p <= 1:
        raise ValueError("Wahrscheinlichkeit muss zwischen 0 und 1 liegen")
    return norm.ppf(p)


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
    print("=" * 70)
    print("Z-SCORE BERECHNUNG")
    print("=" * 70)
    print("\nFormel: z = (x - mu) / sigma")
    print("Wahrscheinlichkeit: P(Z <= z) = Phi(z)")
    print("\nVerwendung:")
    print("  python z_score.py z=<wert> mu=<wert> sigma=<wert> x=<wert> p=<wert> [var=<wert>]")
    print("\nWenn ein Wert unbekannt ist, verwende '-' als Platzhalter")
    print("p = Wahrscheinlichkeit P(Z <= z) (Flächeninhalt)")
    print("var = Varianz (wird automatisch in sigma umgerechnet: sigma = sqrt(var))")
    print("\nBeispiele:")
    print("  python z_score.py z=1.5 mu=100 sigma=15 x=-")
    print("  python z_score.py z=1 mu=- sigma=- x=- p=-")
    print("  python z_score.py z=1 p=-")
    print("  python z_score.py z=- p=0.84134")
    
    if len(sys.argv) < 2:
        print("\n" + "=" * 70)
        print("Bitte geben Sie mindestens 3 Werte an (einer kann '-' sein)")
        sys.exit(1)
    
    # Parse Argumente
    z = None
    mu = None
    sigma = None
    x = None
    p = None
    var = None
    
    for arg in sys.argv[1:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            key = key.lower().strip()
            try:
                parsed_value = parse_value(value)
                if key in ['z', 'z-score', 'zscore']:
                    z = parsed_value
                elif key in ['mu', 'μ', 'mittelwert', 'mean', 'mu0']:
                    mu = parsed_value
                elif key in ['sigma', 'σ', 'std', 'standardabweichung']:
                    sigma = parsed_value
                elif key in ['var', 'varianz', 'variance']:
                    var = parsed_value
                elif key in ['x', 'x_bar', 'xbar']:
                    x = parsed_value
                elif key in ['p', 'prob', 'wahrscheinlichkeit', 'phi', 'probability']:
                    p = parsed_value
                else:
                    print(f"Unbekannter Parameter: {key}")
            except ValueError as e:
                print(f"FEHLER beim Parsen von {key}={value}: {e}")
                sys.exit(1)
    
    # Wenn var gegeben ist, in sigma umrechnen (falls sigma nicht bereits gegeben)
    var_verwendet = False
    if var is not None:
        if var < 0:
            raise ValueError("Varianz darf nicht negativ sein")
        if sigma is not None:
            print("Warnung: Sowohl sigma als auch var wurden angegeben. sigma wird verwendet.")
        else:
            sigma = math.sqrt(var)
            var_verwendet = True
    
    # Zähle gegebene Werte (p zählt nicht zu den 4 Grundwerten)
    gegebene_werte = sum([z is not None, mu is not None, sigma is not None, x is not None])
    
    # Spezialfälle: z allein, p allein, oder z und p zusammen sind OK
    z_allein_ok = (z is not None and gegebene_werte == 1)
    p_allein_ok = (p is not None and gegebene_werte == 0)
    z_und_p_ok = (z is not None and p is not None)
    
    # Wenn nur z oder nur p gegeben ist, ist das OK
    # Oder wenn mindestens 3 der 4 Grundwerte gegeben sind
    if gegebene_werte < 3 and not (z_allein_ok or p_allein_ok):
        print("\nFEHLER: Mindestens 3 Werte (z, mu, sigma, x) müssen angegeben werden!")
        print(f"Gegebene Werte: {gegebene_werte}")
        print("Oder: z allein, p allein, oder z und p zusammen")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("EINGEGEBENE WERTE")
    print("=" * 70)
    print(f"  z (Z-Score) = {z if z is not None else '-'}")
    print(f"  mu (Mittelwert) = {mu if mu is not None else '-'}")
    if var_verwendet:
        print(f"  var (Varianz) = {var}")
        print(f"  sigma (Standardabweichung) = {sigma:.6f} (aus var berechnet: sigma = sqrt(var))")
    else:
        print(f"  sigma (Standardabweichung) = {sigma if sigma is not None else '-'}")
        if var is not None and not var_verwendet:
            print(f"  var (Varianz) = {var} (ignoriert, sigma wurde verwendet)")
    print(f"  x (Wert) = {x if x is not None else '-'}")
    print(f"  p (Wahrscheinlichkeit P(Z <= z)) = {p if p is not None else '-'}")
    
    # Berechne fehlende Werte
    print("\n" + "=" * 70)
    print("BERECHNUNGEN")
    print("=" * 70)
    
    berechnungen = []
    
    # Zuerst: z und p berechnen (falls möglich)
    if z is None and p is not None:
        # Berechne z aus p
        z = berechne_z_aus_wahrscheinlichkeit(p)
        berechnungen.append(f"z = Phi^(-1)(p) = Phi^(-1)({p}) = {z:.6f}")
    elif z is not None and p is None:
        # Berechne p aus z
        p = berechne_wahrscheinlichkeit(z)
        berechnungen.append(f"p = Phi(z) = Phi({z}) = P(Z <= {z}) = {p:.6f}")
    elif z is not None and p is not None:
        # Beide gegeben, verifiziere
        p_berechnet = berechne_wahrscheinlichkeit(z)
        berechnungen.append(f"z = {z:.6f} (gegeben)")
        berechnungen.append(f"p = {p:.6f} (gegeben)")
        berechnungen.append(f"Verifikation: Phi({z}) = {p_berechnet:.6f}")
        if abs(p - p_berechnet) > 0.0001:
            berechnungen.append(f"  Warnung: Abweichung zwischen gegebenem und berechnetem p!")
    
    # Wenn var verwendet wurde, zeige Umrechnung
    if var_verwendet:
        berechnungen.append(f"sigma = sqrt(var) = sqrt({var}) = {sigma:.6f}")
    
    # Dann: z, mu, sigma, x berechnen
    if z is None:
        if x is not None and mu is not None and sigma is not None:
            z = berechne_z_score(x, mu, sigma)
            berechnungen.append(f"z = (x - mu) / sigma = ({x} - {mu}) / {sigma} = {z:.6f}")
    else:
        berechnungen.append(f"z = {z:.6f} (gegeben)")
    
    if x is None:
        if z is not None and mu is not None and sigma is not None:
            x = berechne_x(z, mu, sigma)
            berechnungen.append(f"x = mu + z * sigma = {mu} + {z} * {sigma} = {x:.6f}")
    else:
        berechnungen.append(f"x = {x:.6f} (gegeben)")
    
    if mu is None:
        if x is not None and z is not None and sigma is not None:
            mu = berechne_mu(x, z, sigma)
            berechnungen.append(f"mu = x - z * sigma = {x} - {z} * {sigma} = {mu:.6f}")
    else:
        berechnungen.append(f"mu = {mu:.6f} (gegeben)")
    
    if sigma is None:
        if x is not None and mu is not None and z is not None:
            sigma = berechne_sigma(x, mu, z)
            berechnungen.append(f"sigma = (x - mu) / z = ({x} - {mu}) / {z} = {sigma:.6f}")
    else:
        berechnungen.append(f"sigma = {sigma:.6f} (gegeben)")
    
    for berechnung in berechnungen:
        print(f"  {berechnung}")
    
    # Zusammenfassung
    print("\n" + "=" * 70)
    print("ERGEBNIS")
    print("=" * 70)
    # Berechne p falls z gegeben ist aber p noch nicht berechnet wurde
    if z is not None and p is None:
        p = berechne_wahrscheinlichkeit(z)
    
    # Zeige Z-Score mit Prozentwert in Klammern
    if z is not None:
        if p is not None:
            print(f"  z (Z-Score) = {z:.6f} ({p*100:.2f}%)")
        else:
            print(f"  z (Z-Score) = {z:.6f}")
    if mu is not None:
        print(f"  mu (Mittelwert) = {mu:.6f}")
    if sigma is not None:
        print(f"  sigma (Standardabweichung) = {sigma:.6f}")
    if x is not None:
        print(f"  x (Wert) = {x:.6f}")
    if p is not None:
        print(f"  p (Wahrscheinlichkeit P(Z <= z)) = {p:.6f}")
        print(f"  Phi(z) = Phi({z}) = {p:.6f}")
    
    # Verifikation (nur wenn alle Werte vorhanden)
    if z is not None and x is not None and mu is not None and sigma is not None:
        print("\n" + "=" * 70)
        print("VERIFIKATION")
        print("=" * 70)
        z_verifikation = berechne_z_score(x, mu, sigma)
        print(f"  z = (x - mu) / sigma = ({x} - {mu}) / {sigma} = {z_verifikation:.6f}")
        if abs(z - z_verifikation) < 0.0001:
            print("  OK Berechnung korrekt!")
        else:
            print("  Warnung: Abweichung festgestellt!")
