"""
Cohens d Berechnung

Berechnet Cohens d, Stichprobenmittelwert, Populationsmittelwert oder Standardabweichung
je nachdem welche Werte gegeben sind.

Formel: d = (x̄ - μ) / σ
"""

import sys
import math


def berechne_cohens_d(x_bar, mu0, sigma):
    """Berechnet Cohens d: d = (x_bar - mu0) / sigma"""
    if sigma == 0:
        raise ValueError("Standardabweichung darf nicht 0 sein")
    return (x_bar - mu0) / sigma


def berechne_x_bar(d, mu0, sigma):
    """Berechnet Stichprobenmittelwert: x_bar = mu0 + d * sigma"""
    return mu0 + d * sigma


def berechne_mu0(x_bar, d, sigma):
    """Berechnet Populationsmittelwert: mu0 = x_bar - d * sigma"""
    return x_bar - d * sigma


def berechne_sigma(x_bar, mu0, d):
    """Berechnet Standardabweichung: sigma = (x_bar - mu0) / d"""
    if d == 0:
        raise ValueError("Cohens d darf nicht 0 sein (x_bar waere gleich mu0)")
    return (x_bar - mu0) / d


def interpretiere_cohens_d(d):
    """Interpretiert Cohens d nach den Standard-Konventionen"""
    abs_d = abs(d)
    if abs_d < 0.2:
        return "sehr klein (vernachlässigbar)"
    elif abs_d < 0.5:
        return "klein"
    elif abs_d < 0.8:
        return "mittel"
    else:
        return "groß"


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
    print("COHENS D BERECHNUNG")
    print("=" * 70)
    print("\nFormel: d = (x_bar - mu0) / sigma")
    print("\nVerwendung:")
    print("  python cohens_d.py d=<wert> x_bar=<wert> mu0=<wert> sigma=<wert>")
    print("\nWenn ein Wert unbekannt ist, verwende '-' als Platzhalter")
    print("Mindestens 3 der 4 Werte müssen angegeben werden")
    print("\nBeispiele:")
    print("  python cohens_d.py x_bar=105 mu0=100 sigma=15 d=-")
    print("  python cohens_d.py d=0.33 x_bar=105 mu0=100 sigma=-")
    print("  python cohens_d.py d=0.33 x_bar=- mu0=100 sigma=15")
    print("  python cohens_d.py d=0.33 x_bar=105 mu0=- sigma=15")
    
    if len(sys.argv) < 2:
        print("\n" + "=" * 70)
        print("Bitte geben Sie mindestens 3 Werte an (einer kann '-' sein)")
        sys.exit(1)
    
    # Parse Argumente
    d = None
    x_bar = None
    mu0 = None
    sigma = None
    
    for arg in sys.argv[1:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            key = key.lower().strip()
            try:
                parsed_value = parse_value(value)
                if key in ['d', 'cohens_d', 'cohensd', 'cohen']:
                    d = parsed_value
                elif key in ['x_bar', 'xbar', 'x', 'stichprobenmittelwert', 'sample_mean']:
                    x_bar = parsed_value
                elif key in ['mu0', 'μ0', 'mu_0', 'mu_null', 'populationsmittelwert', 'population_mean', 'mu']:
                    mu0 = parsed_value
                elif key in ['sigma', 'σ', 'std', 'standardabweichung', 'standard_deviation']:
                    sigma = parsed_value
                else:
                    print(f"Unbekannter Parameter: {key}")
            except ValueError as e:
                print(f"FEHLER beim Parsen von {key}={value}: {e}")
                sys.exit(1)
    
    # Zähle gegebene Werte
    gegebene_werte = sum([d is not None, x_bar is not None, mu0 is not None, sigma is not None])
    
    if gegebene_werte < 3:
        print("\nFEHLER: Mindestens 3 Werte (d, x_bar, mu0, sigma) müssen angegeben werden!")
        print(f"Gegebene Werte: {gegebene_werte}")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("EINGEGEBENE WERTE")
    print("=" * 70)
    print(f"  d (Cohens d) = {d if d is not None else '-'}")
    print(f"  x_bar (Stichprobenmittelwert) = {x_bar if x_bar is not None else '-'}")
    print(f"  mu0 (Populationsmittelwert) = {mu0 if mu0 is not None else '-'}")
    print(f"  sigma (Standardabweichung) = {sigma if sigma is not None else '-'}")
    
    # Berechne fehlende Werte
    print("\n" + "=" * 70)
    print("BERECHNUNGEN")
    print("=" * 70)
    
    berechnungen = []
    
    # Berechne d
    if d is None:
        if x_bar is not None and mu0 is not None and sigma is not None:
            d = berechne_cohens_d(x_bar, mu0, sigma)
            berechnungen.append(f"d = (x_bar - mu0) / sigma = ({x_bar} - {mu0}) / {sigma} = {d:.6f}")
    else:
        berechnungen.append(f"d = {d:.6f} (gegeben)")
    
    # Berechne x_bar
    if x_bar is None:
        if d is not None and mu0 is not None and sigma is not None:
            x_bar = berechne_x_bar(d, mu0, sigma)
            berechnungen.append(f"x_bar = mu0 + d * sigma = {mu0} + {d} * {sigma} = {x_bar:.6f}")
    else:
        berechnungen.append(f"x_bar = {x_bar:.6f} (gegeben)")
    
    # Berechne mu0
    if mu0 is None:
        if x_bar is not None and d is not None and sigma is not None:
            mu0 = berechne_mu0(x_bar, d, sigma)
            berechnungen.append(f"mu0 = x_bar - d * sigma = {x_bar} - {d} * {sigma} = {mu0:.6f}")
    else:
        berechnungen.append(f"mu0 = {mu0:.6f} (gegeben)")
    
    # Berechne sigma
    if sigma is None:
        if x_bar is not None and mu0 is not None and d is not None:
            sigma = berechne_sigma(x_bar, mu0, d)
            berechnungen.append(f"sigma = (x_bar - mu0) / d = ({x_bar} - {mu0}) / {d} = {sigma:.6f}")
    else:
        berechnungen.append(f"sigma = {sigma:.6f} (gegeben)")
    
    for berechnung in berechnungen:
        print(f"  {berechnung}")
    
    # Zusammenfassung
    print("\n" + "=" * 70)
    print("ERGEBNIS")
    print("=" * 70)
    print(f"  d (Cohens d) = {d:.6f}")
    if x_bar is not None:
        print(f"  x_bar (Stichprobenmittelwert) = {x_bar:.6f}")
    if mu0 is not None:
        print(f"  mu0 (Populationsmittelwert) = {mu0:.6f}")
    if sigma is not None:
        print(f"  sigma (Standardabweichung) = {sigma:.6f}")
    
    # Interpretation von Cohens d
    if d is not None:
        print("\n" + "=" * 70)
        print("INTERPRETATION")
        print("=" * 70)
        interpretation = interpretiere_cohens_d(d)
        print(f"  Cohens d = {d:.6f} ist {interpretation}")
        print(f"  Effektgröße: |d| = {abs(d):.6f}")
        if d > 0:
            print(f"  Richtung: Stichprobenmittelwert liegt über Populationsmittelwert")
        elif d < 0:
            print(f"  Richtung: Stichprobenmittelwert liegt unter Populationsmittelwert")
        else:
            print(f"  Richtung: Stichprobenmittelwert entspricht Populationsmittelwert")
    
    # Verifikation (nur wenn alle Werte vorhanden)
    if d is not None and x_bar is not None and mu0 is not None and sigma is not None:
        print("\n" + "=" * 70)
        print("VERIFIKATION")
        print("=" * 70)
        d_verifikation = berechne_cohens_d(x_bar, mu0, sigma)
        print(f"  d = (x_bar - mu0) / sigma = ({x_bar} - {mu0}) / {sigma} = {d_verifikation:.6f}")
        if abs(d - d_verifikation) < 0.0001:
            print("  OK Berechnung korrekt!")
        else:
            print("  Warnung: Abweichung festgestellt!")
