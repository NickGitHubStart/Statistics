"""
Konfidenzintervall Berechnung

Berechnet Konfidenzintervalle für den Mittelwert.
Unterscheidet zwischen Z-Test (sigma bekannt) und t-Test (nur s bekannt).

Formel 1 (Z-Test): x_bar +/- z_{1-alpha/2} * sigma/sqrt(n)
Formel 2 (t-Test): x_bar +/- t_{n-1; 1-alpha/2} * s/sqrt(n)
"""

import sys
import math
from scipy.stats import norm, t


def berechne_konfidenzintervall_z(x_bar, sigma, n, alpha, seite="zweiseitig"):
    """
    Berechnet Konfidenzintervall mit Z-Verteilung (sigma bekannt)
    
    Formel: x_bar +/- z_{1-alpha/2} * sigma/sqrt(n)
    """
    if n <= 0:
        raise ValueError("Stichprobenumfang n muss > 0 sein")
    if sigma <= 0:
        raise ValueError("Standardabweichung sigma muss > 0 sein")
    if not 0 < alpha < 1:
        raise ValueError("Irrtumswahrscheinlichkeit alpha muss zwischen 0 und 1 liegen")
    
    standardfehler = sigma / math.sqrt(n)
    
    if seite == "zweiseitig":
        z_wert = norm.ppf(1 - alpha/2)
        untere_grenze = x_bar - z_wert * standardfehler
        obere_grenze = x_bar + z_wert * standardfehler
    elif seite == "einseitig_links" or seite == "links":
        z_wert = norm.ppf(1 - alpha)
        untere_grenze = x_bar - z_wert * standardfehler
        obere_grenze = float('inf')
    elif seite == "einseitig_rechts" or seite == "rechts":
        z_wert = norm.ppf(1 - alpha)
        untere_grenze = float('-inf')
        obere_grenze = x_bar + z_wert * standardfehler  # Obere Grenze für rechtsseitiges Intervall
    else:
        raise ValueError(f"Unbekannte Seite: {seite}")
    
    return untere_grenze, obere_grenze, z_wert, standardfehler


def berechne_konfidenzintervall_t(x_bar, s, n, alpha, seite="zweiseitig"):
    """
    Berechnet Konfidenzintervall mit t-Verteilung (nur s bekannt)
    
    Formel: x_bar +/- t_{n-1; 1-alpha/2} * s/sqrt(n)
    """
    if n <= 1:
        raise ValueError("Stichprobenumfang n muss > 1 sein für t-Verteilung")
    if s <= 0:
        raise ValueError("Standardabweichung s muss > 0 sein")
    if not 0 < alpha < 1:
        raise ValueError("Irrtumswahrscheinlichkeit alpha muss zwischen 0 und 1 liegen")
    
    df = n - 1  # Freiheitsgrade
    standardfehler = s / math.sqrt(n)
    
    if seite == "zweiseitig":
        t_wert = t.ppf(1 - alpha/2, df)
        untere_grenze = x_bar - t_wert * standardfehler
        obere_grenze = x_bar + t_wert * standardfehler
    elif seite == "einseitig_links" or seite == "links":
        t_wert = t.ppf(1 - alpha, df)
        untere_grenze = x_bar - t_wert * standardfehler
        obere_grenze = float('inf')
    elif seite == "einseitig_rechts" or seite == "rechts":
        t_wert = t.ppf(1 - alpha, df)
        untere_grenze = float('-inf')
        obere_grenze = x_bar + t_wert * standardfehler  # Obere Grenze für rechtsseitiges Intervall
    else:
        raise ValueError(f"Unbekannte Seite: {seite}")
    
    return untere_grenze, obere_grenze, t_wert, standardfehler


def get_wahrscheinlichkeit_z(z, seite="zweiseitig"):
    """Berechnet Wahrscheinlichkeit für Z-Wert"""
    if seite == "zweiseitig":
        return 2 * (1 - norm.cdf(abs(z)))
    elif seite == "einseitig_links" or seite == "links":
        return norm.cdf(z)
    elif seite == "einseitig_rechts" or seite == "rechts":
        return 1 - norm.cdf(z)
    else:
        raise ValueError(f"Unbekannte Seite: {seite}")


def get_wahrscheinlichkeit_t(t_val, df, seite="zweiseitig"):
    """Berechnet Wahrscheinlichkeit für t-Wert"""
    if seite == "zweiseitig":
        return 2 * (1 - t.cdf(abs(t_val), df))
    elif seite == "einseitig_links" or seite == "links":
        return t.cdf(t_val, df)
    elif seite == "einseitig_rechts" or seite == "rechts":
        return 1 - t.cdf(t_val, df)
    else:
        raise ValueError(f"Unbekannte Seite: {seite}")


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
    print("KONFIDENZINTERVALL BERECHNUNG")
    print("=" * 70)
    print("\nFormel 1 (Z-Test, sigma bekannt): x_bar ± z_{1-alpha/2} · sigma/sqrt(n)")
    print("Formel 2 (t-Test, nur s bekannt): x_bar ± t_{n-1; 1-alpha/2} · s/sqrt(n)")
    print("\nVerwendung:")
    print("  python konfidenzintervall.py x_bar=<wert> n=<wert> alpha=<wert> seite=<art> [sigma=<wert>] [s=<wert>] [shoch2=<wert>]")
    print("\nWenn ein Wert unbekannt ist, verwende '-' als Platzhalter")
    print("shoch2 = Varianz (wird automatisch in s umgerechnet: s = sqrt(shoch2))")
    print("\nSeiten: zweiseitig, einseitig_links, einseitig_rechts (oder: links, rechts)")
    print("\nBeispiele:")
    print("  python konfidenzintervall.py x_bar=9 n=31 alpha=0.05 seite=zweiseitig shoch2=31/4")
    print("  python konfidenzintervall.py x_bar=9 n=31 alpha=0.05 seite=zweiseitig s=2.78")
    print("  python konfidenzintervall.py x_bar=100 n=25 alpha=0.05 seite=zweiseitig sigma=15")
    
    if len(sys.argv) < 2:
        print("\n" + "=" * 70)
        print("Bitte geben Sie die erforderlichen Werte an")
        sys.exit(1)
    
    # Parse Argumente
    x_bar = None
    n = None
    alpha = None
    seite = None
    sigma = None  # Für Z-Test
    s = None      # Für t-Test
    shoch2 = None # Varianz (wird in s umgerechnet)
    
    for arg in sys.argv[1:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            key = key.lower().strip()
            
            # Seite wird nicht als Zahl geparst
            if key in ['seite', 'side', 'art', 'test']:
                seite = value.strip().lower()
                continue
            
            try:
                parsed_value = parse_value(value)
                if key in ['x_bar', 'xbar', 'x', 'stichprobenmittelwert']:
                    x_bar = parsed_value
                elif key == 'n':
                    n = int(parsed_value) if parsed_value is not None else None
                elif key in ['alpha', 'irrtumswahrscheinlichkeit', 'signifikanzniveau']:
                    alpha = parsed_value
                elif key in ['sigma', 'std_pop', 'standardabweichung_population']:
                    sigma = parsed_value
                elif key in ['s', 'std', 'standardabweichung_stichprobe']:
                    s = parsed_value
                elif key in ['shoch2', 's^2', 's2', 'var', 'varianz', 'variance']:
                    shoch2 = parsed_value
                else:
                    print(f"Unbekannter Parameter: {key}")
            except ValueError as e:
                print(f"FEHLER beim Parsen von {key}={value}: {e}")
                sys.exit(1)
    
    # Normalisiere Seite
    if seite:
        seite_mapping = {
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
        if seite in seite_mapping:
            seite = seite_mapping[seite]
    
    # Wenn shoch2 gegeben ist, in s umrechnen (falls s nicht bereits gegeben)
    s_verwendet = False
    if shoch2 is not None:
        if shoch2 < 0:
            raise ValueError("Varianz darf nicht negativ sein")
        if s is not None:
            print("Warnung: Sowohl s als auch shoch2 wurden angegeben. s wird verwendet.")
        else:
            s = math.sqrt(shoch2)
            s_verwendet = True
    
    # Bestimme Testtyp: Z-Test wenn sigma gegeben, sonst t-Test
    testtyp = None
    if sigma is not None:
        testtyp = "z"
    elif s is not None:
        testtyp = "t"
    else:
        print("\nFEHLER: Entweder sigma (für Z-Test) oder s/shoch2 (für t-Test) muss angegeben werden!")
        sys.exit(1)
    
    # Validierung
    if x_bar is None:
        print("\nFEHLER: x_bar muss angegeben werden!")
        sys.exit(1)
    if n is None:
        print("\nFEHLER: n muss angegeben werden!")
        sys.exit(1)
    if alpha is None:
        print("\nFEHLER: alpha muss angegeben werden!")
        sys.exit(1)
    if seite is None:
        seite = "zweiseitig"
        print("Hinweis: Seite nicht angegeben, verwende zweiseitig als Standard")
    
    print("\n" + "=" * 70)
    print("EINGEGEBENE WERTE")
    print("=" * 70)
    print(f"  x_bar (Stichprobenmittelwert) = {x_bar}")
    print(f"  n (Stichprobenumfang) = {n}")
    print(f"  alpha (Irrtumswahrscheinlichkeit) = {alpha}")
    print(f"  Seite = {seite}")
    if testtyp == "z":
        print(f"  sigma (Populationsstandardabweichung) = {sigma}")
        print(f"  Testtyp: Z-Test (sigma bekannt)")
    else:
        if s_verwendet:
            print(f"  shoch2 (Varianz) = {shoch2}")
            print(f"  s (Stichprobenstandardabweichung) = {s:.6f} (aus shoch2 berechnet: s = sqrt(shoch2))")
        else:
            print(f"  s (Stichprobenstandardabweichung) = {s}")
        print(f"  Testtyp: t-Test (nur s bekannt, df = {n-1})")
    
    # Berechne Konfidenzintervall
    print("\n" + "=" * 70)
    print("BERECHNUNGEN")
    print("=" * 70)
    
    berechnungen = []
    
    if s_verwendet:
        berechnungen.append(f"s = sqrt(shoch2) = sqrt({shoch2}) = {s:.6f}")
    
    if testtyp == "z":
        untere_grenze, obere_grenze, z_wert, standardfehler = berechne_konfidenzintervall_z(x_bar, sigma, n, alpha, seite)
        berechnungen.append(f"Standardfehler = sigma / sqrt(n) = {sigma} / sqrt({n}) = {standardfehler:.6f}")
        
        if seite == "zweiseitig":
            berechnungen.append(f"z_{{1-alpha/2}} = z_{{1-{alpha}/2}} = z_{{{1-alpha/2:.4f}}} = {z_wert:.6f}")
        elif seite == "einseitig_links":
            berechnungen.append(f"z_{{1-alpha}} = z_{{1-{alpha}}} = z_{{{1-alpha:.4f}}} = {z_wert:.6f}")
        else:
            berechnungen.append(f"z_{{1-alpha}} = z_{{1-{alpha}}} = z_{{{1-alpha:.4f}}} = {z_wert:.6f}")
        
        p_wert = get_wahrscheinlichkeit_z(z_wert, seite)
        berechnungen.append(f"Wahrscheinlichkeit für z = {z_wert:.6f}: {p_wert:.6f} ({p_wert*100:.2f}%)")
        
        if seite == "zweiseitig":
            berechnungen.append(f"Konfidenzintervall: [{untere_grenze:.6f}, {obere_grenze:.6f}]")
            berechnungen.append(f"  Untere Grenze = x_bar - z * SE = {x_bar} - {z_wert} * {standardfehler} = {untere_grenze:.6f}")
            berechnungen.append(f"  Obere Grenze = x_bar + z * SE = {x_bar} + {z_wert} * {standardfehler} = {obere_grenze:.6f}")
        elif seite == "einseitig_links":
            berechnungen.append(f"Konfidenzintervall: (-inf, {obere_grenze:.6f}]")
            berechnungen.append(f"  Obere Grenze = x_bar + z * SE = {x_bar} + {z_wert} * {standardfehler} = {obere_grenze:.6f}")
        else:
            berechnungen.append(f"Konfidenzintervall: [{untere_grenze:.6f}, +inf)")
            berechnungen.append(f"  Untere Grenze = x_bar - z * SE = {x_bar} - {z_wert} * {standardfehler} = {untere_grenze:.6f}")
    else:
        untere_grenze, obere_grenze, t_wert, standardfehler = berechne_konfidenzintervall_t(x_bar, s, n, alpha, seite)
        df = n - 1
        berechnungen.append(f"Freiheitsgrade (df) = n - 1 = {n} - 1 = {df}")
        berechnungen.append(f"Standardfehler = s / sqrt(n) = {s} / sqrt({n}) = {standardfehler:.6f}")
        
        if seite == "zweiseitig":
            berechnungen.append(f"t_{{df; 1-alpha/2}} = t_{{{df}; 1-{alpha}/2}} = t_{{{df}; {1-alpha/2:.4f}}} = {t_wert:.6f}")
        elif seite == "einseitig_links":
            berechnungen.append(f"t_{{df; 1-alpha}} = t_{{{df}; 1-{alpha}}} = t_{{{df}; {1-alpha:.4f}}} = {t_wert:.6f}")
        else:
            berechnungen.append(f"t_{{df; 1-alpha}} = t_{{{df}; 1-{alpha}}} = t_{{{df}; {1-alpha:.4f}}} = {t_wert:.6f}")
        
        p_wert = get_wahrscheinlichkeit_t(t_wert, df, seite)
        berechnungen.append(f"Wahrscheinlichkeit für t = {t_wert:.6f}: {p_wert:.6f} ({p_wert*100:.2f}%)")
        
        if seite == "zweiseitig":
            berechnungen.append(f"Konfidenzintervall: [{untere_grenze:.6f}, {obere_grenze:.6f}]")
            berechnungen.append(f"  Untere Grenze = x_bar - t * SE = {x_bar} - {t_wert} * {standardfehler} = {untere_grenze:.6f}")
            berechnungen.append(f"  Obere Grenze = x_bar + t * SE = {x_bar} + {t_wert} * {standardfehler} = {obere_grenze:.6f}")
        elif seite == "einseitig_links":
            berechnungen.append(f"Konfidenzintervall: (-inf, {obere_grenze:.6f}]")
            berechnungen.append(f"  Obere Grenze = x_bar + t * SE = {x_bar} + {t_wert} * {standardfehler} = {obere_grenze:.6f}")
        else:
            berechnungen.append(f"Konfidenzintervall: (-inf, {obere_grenze:.6f}]")
            berechnungen.append(f"  Obere Grenze = x_bar + t * SE = {x_bar} + {t_wert} * {standardfehler} = {obere_grenze:.6f}")
    
    for berechnung in berechnungen:
        print(f"  {berechnung}")
    
    # Zusammenfassung
    print("\n" + "=" * 70)
    print("ERGEBNIS")
    print("=" * 70)
    print(f"  x_bar (Stichprobenmittelwert) = {x_bar:.6f}")
    print(f"  n (Stichprobenumfang) = {n}")
    print(f"  alpha (Irrtumswahrscheinlichkeit) = {alpha}")
    print(f"  Konfidenzniveau = {(1-alpha)*100:.2f}%")
    print(f"  Seite = {seite}")
    
    if testtyp == "z":
        print(f"  sigma (Populationsstandardabweichung) = {sigma:.6f}")
        print(f"  z-Wert = {z_wert:.6f} ({p_wert*100:.2f}%)")
        print(f"  Standardfehler = {standardfehler:.6f}")
    else:
        print(f"  s (Stichprobenstandardabweichung) = {s:.6f}")
        print(f"  Freiheitsgrade (df) = {df}")
        print(f"  t-Wert = {t_wert:.6f} ({p_wert*100:.2f}%)")
        print(f"  Standardfehler = {standardfehler:.6f}")
    
    if seite == "zweiseitig":
        print(f"\n  Konfidenzintervall ({(1-alpha)*100:.2f}%): [{untere_grenze:.6f}, {obere_grenze:.6f}]")
        print(f"  Breite des Intervalls: {obere_grenze - untere_grenze:.6f}")
    elif seite == "einseitig_links":
        print(f"\n  Konfidenzintervall ({(1-alpha)*100:.2f}%): (-inf, {obere_grenze:.6f}]")
    else:  # einseitig_rechts
        print(f"\n  Konfidenzintervall ({(1-alpha)*100:.2f}%): (-inf, {obere_grenze:.6f}]")
