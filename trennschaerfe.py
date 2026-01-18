"""
Trennschärfe (Power) Berechnung

Berechnet die Trennschärfe (Power) eines Hypothesentests.
Die Trennschärfe ist die Wahrscheinlichkeit, H0 abzulehnen, wenn H1 wahr ist.

Unterscheidet automatisch zwischen:
- Einstichproben-Z-Test (sigma bekannt)
- Einstichproben-t-Test (nur s bekannt)
- Zweistichproben-t-Test (zwei Gruppen, unverbundene Stichproben)

Formel 1 (Z-Test): Power = 1 - Beta
Formel 2 (t-Test): Power = 1 - Beta (mit t-Verteilung)
Formel 3 (Zweistichproben-t-Test): Power = 1 - Beta (mit gepoolter Varianz)
"""

import sys
import math
from scipy.stats import norm, t


def berechne_power_z(mu0, mu1, sigma, n, alpha, test_art="zweiseitig"):
    """
    Berechnet Trennschärfe für Z-Test (sigma bekannt)
    
    Power = P(H0 ablehnen | H1 ist wahr)
    """
    if n <= 0:
        raise ValueError("Stichprobenumfang n muss > 0 sein")
    if sigma <= 0:
        raise ValueError("Standardabweichung sigma muss > 0 sein")
    if not 0 < alpha < 1:
        raise ValueError("Signifikanzniveau alpha muss zwischen 0 und 1 liegen")
    
    standardfehler = sigma / math.sqrt(n)
    effekt = mu1 - mu0  # Effektgröße
    
    # Kritischer z-Wert
    if test_art == "zweiseitig":
        z_kritisch = norm.ppf(1 - alpha/2)
        # Power = 1 - P(-z_kritisch < Z < z_kritisch | H1)
        # Unter H1: Z ~ N((mu1-mu0)/(sigma/√n), 1) = N(effekt/SE, 1)
        z_standardisiert = effekt / standardfehler
        power = 1 - norm.cdf(z_kritisch - z_standardisiert) + norm.cdf(-z_kritisch - z_standardisiert)
    elif test_art == "einseitig_links" or test_art == "links":
        z_kritisch = norm.ppf(alpha)
        z_standardisiert = effekt / standardfehler
        power = norm.cdf(z_kritisch - z_standardisiert)
    elif test_art == "einseitig_rechts" or test_art == "rechts":
        z_kritisch = norm.ppf(1 - alpha)
        z_standardisiert = effekt / standardfehler
        power = 1 - norm.cdf(z_kritisch - z_standardisiert)
    else:
        raise ValueError(f"Unbekannte Testart: {test_art}")
    
    return power, z_kritisch, z_standardisiert, standardfehler


def berechne_power_t(mu0, mu1, s, n, alpha, test_art="zweiseitig"):
    """
    Berechnet Trennschärfe für t-Test (nur s bekannt)
    
    Power = P(H0 ablehnen | H1 ist wahr)
    """
    if n <= 1:
        raise ValueError("Stichprobenumfang n muss > 1 sein für t-Test")
    if s <= 0:
        raise ValueError("Standardabweichung s muss > 0 sein")
    if not 0 < alpha < 1:
        raise ValueError("Signifikanzniveau alpha muss zwischen 0 und 1 liegen")
    
    df = n - 1
    standardfehler = s / math.sqrt(n)
    effekt = mu1 - mu0
    
    # Kritischer t-Wert
    if test_art == "zweiseitig":
        t_kritisch = t.ppf(1 - alpha/2, df)
        # Power mit nicht-zentraler t-Verteilung approximiert
        # Für große n: ähnlich wie Z-Test
        t_standardisiert = effekt / standardfehler
        # Approximation: verwende Normalverteilung für große n, sonst nicht-zentrale t
        if n >= 30:
            power = 1 - norm.cdf(t_kritisch - t_standardisiert) + norm.cdf(-t_kritisch - t_standardisiert)
        else:
            # Für kleine n: verwende nicht-zentrale t-Verteilung (nct)
            from scipy.stats import nct
            ncp = t_standardisiert  # Non-centrality parameter
            power = 1 - nct.cdf(t_kritisch, df, ncp) + nct.cdf(-t_kritisch, df, ncp)
    elif test_art == "einseitig_links" or test_art == "links":
        t_kritisch = t.ppf(alpha, df)
        t_standardisiert = effekt / standardfehler
        if n >= 30:
            power = norm.cdf(t_kritisch - t_standardisiert)
        else:
            from scipy.stats import nct
            ncp = t_standardisiert
            power = nct.cdf(t_kritisch, df, ncp)
    elif test_art == "einseitig_rechts" or test_art == "rechts":
        t_kritisch = t.ppf(1 - alpha, df)
        t_standardisiert = effekt / standardfehler
        if n >= 30:
            power = 1 - norm.cdf(t_kritisch - t_standardisiert)
        else:
            from scipy.stats import nct
            ncp = t_standardisiert
            power = 1 - nct.cdf(t_kritisch, df, ncp)
    else:
        raise ValueError(f"Unbekannte Testart: {test_art}")
    
    return power, t_kritisch, t_standardisiert, standardfehler, df


def berechne_power_zweistichproben_t(mu1, mu2, s1, s2, n1, n2, alpha, test_art="zweiseitig"):
    """
    Berechnet Trennschärfe für Zweistichproben-t-Test (unverbundene Stichproben)
    
    Power = P(H0 ablehnen | H1 ist wahr)
    
    Verwendet gepoolte Varianz: s_pooled^2 = ((n1-1)*s1^2 + (n2-1)*s2^2) / (n1+n2-2)
    Standardfehler: SE = s_pooled * sqrt(1/n1 + 1/n2)
    """
    if n1 <= 1 or n2 <= 1:
        raise ValueError("Stichprobenumfang n1 und n2 müssen > 1 sein für t-Test")
    if s1 <= 0 or s2 <= 0:
        raise ValueError("Standardabweichungen s1 und s2 müssen > 0 sein")
    if not 0 < alpha < 1:
        raise ValueError("Signifikanzniveau alpha muss zwischen 0 und 1 liegen")
    
    df = n1 + n2 - 2
    
    # Gepoolte Varianz
    s_pooled_quadrat = ((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / df
    s_pooled = math.sqrt(s_pooled_quadrat)
    
    # Standardfehler
    standardfehler = s_pooled * math.sqrt(1/n1 + 1/n2)
    
    # Effekt (Differenz der Mittelwerte)
    effekt = mu1 - mu2
    
    # Kritischer t-Wert
    if test_art == "zweiseitig":
        t_kritisch = t.ppf(1 - alpha/2, df)
        # Power mit nicht-zentraler t-Verteilung
        t_standardisiert = effekt / standardfehler
        if n1 + n2 >= 60:  # Große Stichproben: Approximation mit Normalverteilung
            power = 1 - norm.cdf(t_kritisch - t_standardisiert) + norm.cdf(-t_kritisch - t_standardisiert)
        else:
            # Für kleine Stichproben: nicht-zentrale t-Verteilung
            from scipy.stats import nct
            ncp = t_standardisiert  # Non-centrality parameter
            power = 1 - nct.cdf(t_kritisch, df, ncp) + nct.cdf(-t_kritisch, df, ncp)
    elif test_art == "einseitig_links" or test_art == "links":
        t_kritisch = t.ppf(alpha, df)
        t_standardisiert = effekt / standardfehler
        if n1 + n2 >= 60:
            power = norm.cdf(t_kritisch - t_standardisiert)
        else:
            from scipy.stats import nct
            ncp = t_standardisiert
            power = nct.cdf(t_kritisch, df, ncp)
    elif test_art == "einseitig_rechts" or test_art == "rechts":
        t_kritisch = t.ppf(1 - alpha, df)
        t_standardisiert = effekt / standardfehler
        if n1 + n2 >= 60:
            power = 1 - norm.cdf(t_kritisch - t_standardisiert)
        else:
            from scipy.stats import nct
            ncp = t_standardisiert
            power = 1 - nct.cdf(t_kritisch, df, ncp)
    else:
        raise ValueError(f"Unbekannte Testart: {test_art}")
    
    return power, t_kritisch, t_standardisiert, standardfehler, df, s_pooled


def berechne_n_aus_power_z(mu0, mu1, sigma, alpha, power, test_art="zweiseitig"):
    """
    Berechnet benötigten Stichprobenumfang n für gewünschte Power (Z-Test)
    """
    if sigma <= 0:
        raise ValueError("Standardabweichung sigma muss > 0 sein")
    if not 0 < alpha < 1:
        raise ValueError("Signifikanzniveau alpha muss zwischen 0 und 1 liegen")
    if not 0 < power < 1:
        raise ValueError("Power muss zwischen 0 und 1 liegen")
    
    effekt = mu1 - mu0
    
    if test_art == "zweiseitig":
        z_kritisch = norm.ppf(1 - alpha/2)
        z_power = norm.ppf(power)
        # Approximation für zweiseitig
        n = ((z_kritisch + z_power) * sigma / effekt) ** 2
    elif test_art == "einseitig_links" or test_art == "links":
        z_kritisch = norm.ppf(alpha)
        z_power = norm.ppf(power)
        n = ((z_kritisch - z_power) * sigma / effekt) ** 2
    elif test_art == "einseitig_rechts" or test_art == "rechts":
        z_kritisch = norm.ppf(1 - alpha)
        z_power = norm.ppf(power)
        n = ((z_kritisch + z_power) * sigma / effekt) ** 2
    else:
        raise ValueError(f"Unbekannte Testart: {test_art}")
    
    return int(math.ceil(n))


def berechne_mu1_aus_power_z(mu0, sigma, n, alpha, power, test_art="zweiseitig"):
    """
    Berechnet mu1 für gewünschte Power (Z-Test)
    """
    if n <= 0:
        raise ValueError("Stichprobenumfang n muss > 0 sein")
    if sigma <= 0:
        raise ValueError("Standardabweichung sigma muss > 0 sein")
    if not 0 < alpha < 1:
        raise ValueError("Signifikanzniveau alpha muss zwischen 0 und 1 liegen")
    if not 0 < power < 1:
        raise ValueError("Power muss zwischen 0 und 1 liegen")
    
    standardfehler = sigma / math.sqrt(n)
    
    if test_art == "zweiseitig":
        z_kritisch = norm.ppf(1 - alpha/2)
        z_power = norm.ppf(power)
        effekt = (z_kritisch + z_power) * standardfehler
    elif test_art == "einseitig_links" or test_art == "links":
        z_kritisch = norm.ppf(alpha)
        z_power = norm.ppf(power)
        effekt = (z_kritisch - z_power) * standardfehler
    elif test_art == "einseitig_rechts" or test_art == "rechts":
        z_kritisch = norm.ppf(1 - alpha)
        z_power = norm.ppf(power)
        effekt = (z_kritisch + z_power) * standardfehler
    else:
        raise ValueError(f"Unbekannte Testart: {test_art}")
    
    return mu0 + effekt


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
    print("TRENNSCHÄRFE (POWER) BERECHNUNG")
    print("=" * 70)
    print("\nBerechnet die Trennschärfe (Power) eines Hypothesentests.")
    print("Power = Wahrscheinlichkeit, H0 abzulehnen, wenn H1 wahr ist")
    print("\nFormel 1 (Einstichproben-Z-Test, sigma bekannt): Power = 1 - Beta")
    print("Formel 2 (Einstichproben-t-Test, nur s bekannt): Power = 1 - Beta (mit t-Verteilung)")
    print("Formel 3 (Zweistichproben-t-Test): Power = 1 - Beta (mit gepoolter Varianz)")
    print("\nVerwendung:")
    print("  # Einstichproben-Test:")
    print("  python trennschaerfe.py mu0=<wert> mu1=<wert> n=<wert> alpha=<wert> test=<art> [sigma=<wert>] [s=<wert>] [shoch2=<wert>] [power=<wert>]")
    print("  # Zweistichproben-t-Test:")
    print("  python trennschaerfe.py mu1=<wert> mu2=<wert> n1=<wert> n2=<wert> s1=<wert> s2=<wert> alpha=<wert> test=<art>")
    print("\nWenn ein Wert unbekannt ist, verwende '-' als Platzhalter")
    print("shoch2 = Varianz (wird automatisch in s umgerechnet: s = sqrt(shoch2))")
    print("\nTestarten: zweiseitig, einseitig_links, einseitig_rechts (oder: links, rechts)")
    print("\nBeispiele:")
    print("  # Power berechnen (Einstichproben-Z-Test)")
    print("  python trennschaerfe.py mu0=100 mu1=105 sigma=15 n=25 alpha=0.05 test=zweiseitig")
    print("  # Power berechnen (Einstichproben-t-Test)")
    print("  python trennschaerfe.py mu0=100 mu1=105 s=15 n=25 alpha=0.05 test=zweiseitig")
    print("  # Power berechnen (Zweistichproben-t-Test)")
    print("  python trennschaerfe.py mu1=26 mu2=28 n1=10 n2=10 s1=4 s2=3 alpha=0.05 test=einseitig_links")
    print("  # Benötigtes n für gewünschte Power berechnen (Einstichproben)")
    print("  python trennschaerfe.py mu0=100 mu1=105 sigma=15 alpha=0.05 power=0.8 test=zweiseitig n=-")
    
    if len(sys.argv) < 2:
        print("\n" + "=" * 70)
        print("Bitte geben Sie die erforderlichen Werte an")
        sys.exit(1)
    
    # Parse Argumente
    mu0 = None
    mu1 = None
    mu2 = None  # Für Zweistichproben-Test
    n = None
    n1 = None   # Für Zweistichproben-Test
    n2 = None   # Für Zweistichproben-Test
    alpha = None
    test_art = None
    sigma = None  # Für Z-Test
    s = None      # Für t-Test
    s1 = None     # Für Zweistichproben-Test
    s2 = None     # Für Zweistichproben-Test
    shoch2 = None # Varianz (wird in s umgerechnet)
    power = None
    zweistichproben = False  # Flag für Zweistichproben-Test
    
    for arg in sys.argv[1:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            key = key.lower().strip()
            
            # Test-Art wird nicht als Zahl geparst
            if key in ['test', 'testart', 'art']:
                test_art = value.strip().lower()
                continue
            
            try:
                parsed_value = parse_value(value)
                if key in ['mu0', 'mu_0', 'mu_null', 'populationsmittelwert_h0']:
                    mu0 = parsed_value
                elif key in ['mu1', 'mu_1', 'mu_eins', 'populationsmittelwert_h1', 'x_bar1', 'xbar1']:
                    mu1 = parsed_value
                elif key in ['mu2', 'mu_2', 'mu_zwei', 'populationsmittelwert_h2', 'x_bar2', 'xbar2']:
                    mu2 = parsed_value
                elif key == 'n':
                    n = int(parsed_value) if parsed_value is not None else None
                elif key == 'n1':
                    n1 = int(parsed_value) if parsed_value is not None else None
                elif key == 'n2':
                    n2 = int(parsed_value) if parsed_value is not None else None
                elif key in ['alpha', 'irrtumswahrscheinlichkeit', 'signifikanzniveau']:
                    alpha = parsed_value
                elif key in ['sigma', 'std_pop', 'standardabweichung_population']:
                    sigma = parsed_value
                elif key in ['s', 'std', 'standardabweichung_stichprobe']:
                    s = parsed_value
                elif key == 's1':
                    s1 = parsed_value
                elif key == 's2':
                    s2 = parsed_value
                elif key in ['shoch2', 's^2', 's2', 'var', 'varianz', 'variance']:
                    shoch2 = parsed_value
                elif key in ['power', 'trennschaerfe', '1-beta']:
                    power = parsed_value
                else:
                    print(f"Unbekannter Parameter: {key}")
            except ValueError as e:
                print(f"FEHLER beim Parsen von {key}={value}: {e}")
                sys.exit(1)
    
    # Normalisiere Testart
    if test_art:
        test_mapping = {
            'zweiseitig': 'zweiseitig',
            'zwei-seitig': 'zweiseitig',
            'beidseitig': 'zweiseitig',
            'einseitig_links': 'einseitig_links',
            'einseitig links': 'einseitig_links',
            'links': 'einseitig_links',
            'einseitig_rechts': 'einseitig_rechts',
            'einseitig rechts': 'einseitig_rechts',
            'rechts': 'einseitig_rechts'
        }
        if test_art in test_mapping:
            test_art = test_mapping[test_art]
    
    # Prüfe ob Zweistichproben-Test (wenn n1, n2, s1, s2 gegeben sind)
    if n1 is not None and n2 is not None and s1 is not None and s2 is not None:
        zweistichproben = True
        if mu1 is None or mu2 is None:
            print("\nFEHLER: Für Zweistichproben-t-Test müssen mu1 und mu2 angegeben werden!")
            sys.exit(1)
    
    # Wenn shoch2 gegeben ist, in s umrechnen (nur für Einstichproben-Test)
    s_verwendet = False
    if not zweistichproben and shoch2 is not None:
        if shoch2 < 0:
            raise ValueError("Varianz darf nicht negativ sein")
        if s is not None:
            print("Warnung: Sowohl s als auch shoch2 wurden angegeben. s wird verwendet.")
        else:
            s = math.sqrt(shoch2)
            s_verwendet = True
    
    # Bestimme Testtyp
    testtyp = None
    if zweistichproben:
        testtyp = "zweistichproben_t"
    elif sigma is not None:
        testtyp = "z"
    elif s is not None:
        testtyp = "t"
    else:
        print("\nFEHLER: Entweder sigma (für Z-Test) oder s/shoch2 (für t-Test) muss angegeben werden!")
        print("Oder für Zweistichproben-t-Test: n1, n2, s1, s2, mu1, mu2")
        sys.exit(1)
    
    if test_art is None:
        test_art = "zweiseitig"
        print("Hinweis: Testart nicht angegeben, verwende zweiseitig als Standard")
    
    print("\n" + "=" * 70)
    print("EINGEGEBENE WERTE")
    print("=" * 70)
    if zweistichproben:
        print(f"  mu1 (Mittelwert Gruppe 1) = {mu1 if mu1 is not None else '-'}")
        print(f"  mu2 (Mittelwert Gruppe 2) = {mu2 if mu2 is not None else '-'}")
        print(f"  n1 (Stichprobenumfang Gruppe 1) = {n1 if n1 is not None else '-'}")
        print(f"  n2 (Stichprobenumfang Gruppe 2) = {n2 if n2 is not None else '-'}")
        print(f"  s1 (Standardabweichung Gruppe 1) = {s1 if s1 is not None else '-'}")
        print(f"  s2 (Standardabweichung Gruppe 2) = {s2 if s2 is not None else '-'}")
        print(f"  alpha (Signifikanzniveau) = {alpha if alpha is not None else '-'}")
        print(f"  Testart = {test_art}")
        print(f"  Testtyp: Zweistichproben-t-Test (unverbundene Stichproben)")
    else:
        print(f"  mu0 (Wert unter H0) = {mu0 if mu0 is not None else '-'}")
        print(f"  mu1 (Wert unter H1) = {mu1 if mu1 is not None else '-'}")
        print(f"  n (Stichprobenumfang) = {n if n is not None else '-'}")
        print(f"  alpha (Signifikanzniveau) = {alpha if alpha is not None else '-'}")
        print(f"  Testart = {test_art}")
        if testtyp == "z":
            print(f"  sigma (Populationsstandardabweichung) = {sigma}")
            print(f"  Testtyp: Einstichproben-Z-Test (sigma bekannt)")
        else:
            if s_verwendet:
                print(f"  shoch2 (Varianz) = {shoch2}")
                print(f"  s (Stichprobenstandardabweichung) = {s:.6f} (aus shoch2 berechnet: s = sqrt(shoch2))")
            else:
                print(f"  s (Stichprobenstandardabweichung) = {s}")
            print(f"  Testtyp: Einstichproben-t-Test (nur s bekannt, df = {n-1 if n else '?'})")
    if power is not None:
        print(f"  power (gewünschte Trennschärfe) = {power}")
    
    # Berechne fehlende Werte
    print("\n" + "=" * 70)
    print("BERECHNUNGEN")
    print("=" * 70)
    
    berechnungen = []
    
    if zweistichproben:
        # ZWEISTICHPROBEN-T-TEST
        if mu1 is None or mu2 is None or n1 is None or n2 is None or s1 is None or s2 is None or alpha is None:
            print("\nFEHLER: Für Zweistichproben-t-Test müssen mu1, mu2, n1, n2, s1, s2 und alpha angegeben werden!")
            sys.exit(1)
        
        power, t_kritisch, t_standardisiert, standardfehler, df, s_pooled = berechne_power_zweistichproben_t(
            mu1, mu2, s1, s2, n1, n2, alpha, test_art
        )
        effekt = mu1 - mu2
        
        berechnungen.append(f"Freiheitsgrade (df) = n1 + n2 - 2 = {n1} + {n2} - 2 = {df}")
        berechnungen.append(f"s_pooled^2 = ((n1-1)*s1^2 + (n2-1)*s2^2) / (n1+n2-2)")
        berechnungen.append(f"            = (({n1}-1)*{s1}^2 + ({n2}-1)*{s2}^2) / ({n1}+{n2}-2)")
        s_pooled_quadrat = ((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / df
        berechnungen.append(f"            = {s_pooled_quadrat:.6f}")
        berechnungen.append(f"s_pooled = sqrt({s_pooled_quadrat:.6f}) = {s_pooled:.6f}")
        berechnungen.append(f"Standardfehler = s_pooled * sqrt(1/n1 + 1/n2)")
        berechnungen.append(f"               = {s_pooled:.6f} * sqrt(1/{n1} + 1/{n2}) = {standardfehler:.6f}")
        berechnungen.append(f"Effekt = mu1 - mu2 = {mu1} - {mu2} = {effekt:.6f}")
        
        if test_art == "zweiseitig":
            berechnungen.append(f"t_kritisch = t_{{df; 1-alpha/2}} = t_{{{df}; 1-{alpha}/2}} = {t_kritisch:.6f}")
        else:
            berechnungen.append(f"t_kritisch = t_{{df; 1-alpha}} = t_{{{df}; 1-{alpha}}} = {t_kritisch:.6f}")
        
        berechnungen.append(f"t_standardisiert = Effekt / SE = {effekt} / {standardfehler} = {t_standardisiert:.6f}")
        berechnungen.append(f"Power = 1 - Beta = {power:.6f} ({power*100:.2f}%)")
        beta = 1 - power
        berechnungen.append(f"Beta (Fehler 2. Art) = 1 - Power = {beta:.6f} ({beta*100:.2f}%)")
        if n1 + n2 < 60:
            berechnungen.append(f"Hinweis: Für n1+n2 < 60 wird nicht-zentrale t-Verteilung verwendet")
    
    elif testtyp == "z":
        # Z-TEST
        if power is None:
            # Berechne Power
            if mu0 is None or mu1 is None or n is None or alpha is None:
                print("\nFEHLER: Für Power-Berechnung müssen mu0, mu1, n und alpha angegeben werden!")
                sys.exit(1)
            
            power, z_kritisch, z_standardisiert, standardfehler = berechne_power_z(mu0, mu1, sigma, n, alpha, test_art)
            effekt = mu1 - mu0
            
            berechnungen.append(f"Effekt = mu1 - mu0 = {mu1} - {mu0} = {effekt:.6f}")
            berechnungen.append(f"Standardfehler = sigma / sqrt(n) = {sigma} / sqrt({n}) = {standardfehler:.6f}")
            
            if test_art == "zweiseitig":
                berechnungen.append(f"z_kritisch = z_{{1-alpha/2}} = z_{{1-{alpha}/2}} = {z_kritisch:.6f}")
            else:
                berechnungen.append(f"z_kritisch = z_{{1-alpha}} = z_{{1-{alpha}}} = {z_kritisch:.6f}")
            
            berechnungen.append(f"z_standardisiert = Effekt / SE = {effekt} / {standardfehler} = {z_standardisiert:.6f}")
            berechnungen.append(f"Power = 1 - Beta = {power:.6f} ({power*100:.2f}%)")
            beta = 1 - power
            berechnungen.append(f"Beta (Fehler 2. Art) = 1 - Power = {beta:.6f} ({beta*100:.2f}%)")
        
        elif n is None:
            # Berechne n aus Power
            if mu0 is None or mu1 is None or alpha is None:
                print("\nFEHLER: Für n-Berechnung müssen mu0, mu1, alpha und power angegeben werden!")
                sys.exit(1)
            
            n = berechne_n_aus_power_z(mu0, mu1, sigma, alpha, power, test_art)
            effekt = mu1 - mu0
            berechnungen.append(f"Effekt = mu1 - mu0 = {mu1} - {mu0} = {effekt:.6f}")
            berechnungen.append(f"Benötigtes n für Power = {power}: n = {n}")
            # Verifiziere mit berechneter Power
            power_verifikation, z_kritisch, z_standardisiert, standardfehler = berechne_power_z(mu0, mu1, sigma, n, alpha, test_art)
            berechnungen.append(f"Verifikation: Power mit n={n} = {power_verifikation:.6f} ({power_verifikation*100:.2f}%)")
        
        elif mu1 is None:
            # Berechne mu1 aus Power
            if mu0 is None or n is None or alpha is None:
                print("\nFEHLER: Für mu1-Berechnung müssen mu0, n, alpha und power angegeben werden!")
                sys.exit(1)
            
            mu1 = berechne_mu1_aus_power_z(mu0, sigma, n, alpha, power, test_art)
            effekt = mu1 - mu0
            berechnungen.append(f"Benötigtes mu1 für Power = {power}: mu1 = {mu1:.6f}")
            berechnungen.append(f"Effekt = mu1 - mu0 = {mu1:.6f} - {mu0} = {effekt:.6f}")
            # Verifiziere
            power_verifikation, z_kritisch, z_standardisiert, standardfehler = berechne_power_z(mu0, mu1, sigma, n, alpha, test_art)
            berechnungen.append(f"Verifikation: Power mit mu1={mu1:.6f} = {power_verifikation:.6f} ({power_verifikation*100:.2f}%)")
    
    else:
        # T-TEST
        if power is None:
            # Berechne Power
            if mu0 is None or mu1 is None or n is None or alpha is None:
                print("\nFEHLER: Für Power-Berechnung müssen mu0, mu1, n und alpha angegeben werden!")
                sys.exit(1)
            
            power, t_kritisch, t_standardisiert, standardfehler, df = berechne_power_t(mu0, mu1, s, n, alpha, test_art)
            effekt = mu1 - mu0
            
            berechnungen.append(f"Freiheitsgrade (df) = n - 1 = {n} - 1 = {df}")
            berechnungen.append(f"Effekt = mu1 - mu0 = {mu1} - {mu0} = {effekt:.6f}")
            berechnungen.append(f"Standardfehler = s / sqrt(n) = {s} / sqrt({n}) = {standardfehler:.6f}")
            
            if test_art == "zweiseitig":
                berechnungen.append(f"t_kritisch = t_{{df; 1-alpha/2}} = t_{{{df}; 1-{alpha}/2}} = {t_kritisch:.6f}")
            else:
                berechnungen.append(f"t_kritisch = t_{{df; 1-alpha}} = t_{{{df}; 1-{alpha}}} = {t_kritisch:.6f}")
            
            berechnungen.append(f"t_standardisiert = Effekt / SE = {effekt} / {standardfehler} = {t_standardisiert:.6f}")
            berechnungen.append(f"Power = 1 - Beta = {power:.6f} ({power*100:.2f}%)")
            beta = 1 - power
            berechnungen.append(f"Beta (Fehler 2. Art) = 1 - Power = {beta:.6f} ({beta*100:.2f}%)")
            if n < 30:
                berechnungen.append(f"Hinweis: Für n < 30 wird nicht-zentrale t-Verteilung verwendet")
    
    for berechnung in berechnungen:
        print(f"  {berechnung}")
    
    # Zusammenfassung
    print("\n" + "=" * 70)
    print("ERGEBNIS")
    print("=" * 70)
    
    if zweistichproben:
        print(f"  mu1 (Mittelwert Gruppe 1) = {mu1:.6f}")
        print(f"  mu2 (Mittelwert Gruppe 2) = {mu2:.6f}")
        print(f"  Effekt = mu1 - mu2 = {mu1 - mu2:.6f}")
        print(f"  n1 (Stichprobenumfang Gruppe 1) = {n1}")
        print(f"  n2 (Stichprobenumfang Gruppe 2) = {n2}")
        print(f"  s1 (Standardabweichung Gruppe 1) = {s1:.6f}")
        print(f"  s2 (Standardabweichung Gruppe 2) = {s2:.6f}")
        print(f"  s_pooled (gepoolte Standardabweichung) = {s_pooled:.6f}")
        print(f"  Freiheitsgrade (df) = {df}")
        print(f"  alpha (Signifikanzniveau) = {alpha}")
        print(f"  Testart = {test_art}")
        print(f"\n  Power (Trennschärfe) = {power:.6f} ({power*100:.2f}%)")
        beta = 1 - power
        print(f"  Beta (Fehler 2. Art) = {beta:.6f} ({beta*100:.2f}%)")
        print(f"\nInterpretation:")
        print(f"  Mit einer Wahrscheinlichkeit von {power*100:.2f}% wird H0 abgelehnt,")
        print(f"  wenn H1 wahr ist (mu1 - mu2 = {mu1 - mu2:.6f}).")
    else:
        print(f"  mu0 (Wert unter H0) = {mu0:.6f}")
        if mu1 is not None:
            print(f"  mu1 (Wert unter H1) = {mu1:.6f}")
            print(f"  Effekt = mu1 - mu0 = {mu1 - mu0:.6f}")
        if n is not None:
            print(f"  n (Stichprobenumfang) = {n}")
        print(f"  alpha (Signifikanzniveau) = {alpha}")
        print(f"  Testart = {test_art}")
        
        if testtyp == "z":
            print(f"  sigma (Populationsstandardabweichung) = {sigma:.6f}")
        else:
            print(f"  s (Stichprobenstandardabweichung) = {s:.6f}")
            if n is not None:
                print(f"  Freiheitsgrade (df) = {n-1}")
        
        if power is not None:
            print(f"\n  Power (Trennschärfe) = {power:.6f} ({power*100:.2f}%)")
            beta = 1 - power
            print(f"  Beta (Fehler 2. Art) = {beta:.6f} ({beta*100:.2f}%)")
            print(f"\nInterpretation:")
            print(f"  Mit einer Wahrscheinlichkeit von {power*100:.2f}% wird H0 abgelehnt,")
            print(f"  wenn H1 wahr ist (mu = {mu1 if mu1 else '?'}).")
    
    if power is not None:
        if power < 0.5:
            print(f"  Warnung: Power ist niedrig (< 50%). Test hat geringe Trennschärfe.")
        elif power < 0.8:
            print(f"  Hinweis: Power ist moderat. Für gute Trennschärfe wird Power >= 0.8 empfohlen.")
        else:
            print(f"  OK: Power ist ausreichend (>= 80%).")
