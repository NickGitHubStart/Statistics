"""
Hypothesentest (Z-Test)

Berechnet alle relevanten Werte für einen Hypothesentest.

Formel: z = (x̄ - μ₀) / (σ / √n)
"""

import sys
import math
from scipy.stats import norm


def berechne_z_test(x_bar, mu0, sigma, n):
    """Berechnet Teststatistik: z = (x_bar - mu0) / (sigma / sqrt(n))"""
    if n <= 0:
        raise ValueError("Stichprobenumfang n muss > 0 sein")
    if sigma <= 0:
        raise ValueError("Standardabweichung sigma muss > 0 sein")
    standardfehler = sigma / math.sqrt(n)
    return (x_bar - mu0) / standardfehler


def berechne_x_bar(z, mu0, sigma, n):
    """Berechnet Stichprobenmittelwert: x_bar = mu0 + z * (sigma / sqrt(n))"""
    standardfehler = sigma / math.sqrt(n)
    return mu0 + z * standardfehler


def berechne_mu0(x_bar, z, sigma, n):
    """Berechnet angenommenen Populationsmittelwert: mu0 = x_bar - z * (sigma / sqrt(n))"""
    standardfehler = sigma / math.sqrt(n)
    return x_bar - z * standardfehler


def berechne_sigma(x_bar, mu0, z, n):
    """Berechnet Standardabweichung: sigma = (x_bar - mu0) * sqrt(n) / z"""
    if z == 0:
        raise ValueError("Z-Wert darf nicht 0 sein")
    if n <= 0:
        raise ValueError("Stichprobenumfang n muss > 0 sein")
    return (x_bar - mu0) * math.sqrt(n) / z


def berechne_n(x_bar, mu0, sigma, z):
    """Berechnet Stichprobenumfang: n = (z * sigma / (x_bar - mu0))^2"""
    if z == 0:
        raise ValueError("Z-Wert darf nicht 0 sein")
    if sigma <= 0:
        raise ValueError("Standardabweichung sigma muss > 0 sein")
    if x_bar == mu0:
        raise ValueError("x_bar und mu0 duerfen nicht gleich sein (Division durch 0)")
    return (z * sigma / (x_bar - mu0)) ** 2


def get_kritischer_wert(alpha, test_art):
    """Berechnet kritischen Z-Wert basierend auf alpha und Testart"""
    if test_art == "zweiseitig":
        return norm.ppf(1 - alpha/2)
    elif test_art == "einseitig_links" or test_art == "links":
        return norm.ppf(alpha)
    elif test_art == "einseitig_rechts" or test_art == "rechts":
        return norm.ppf(1 - alpha)
    else:
        raise ValueError(f"Unbekannte Testart: {test_art}")


def get_p_wert(z, test_art):
    """Berechnet p-Wert basierend auf Z-Wert und Testart"""
    if test_art == "zweiseitig":
        return 2 * (1 - norm.cdf(abs(z)))
    elif test_art == "einseitig_links" or test_art == "links":
        return norm.cdf(z)
    elif test_art == "einseitig_rechts" or test_art == "rechts":
        return 1 - norm.cdf(z)
    else:
        raise ValueError(f"Unbekannte Testart: {test_art}")


def berechne_z_aus_p_wert(p_wert, test_art):
    """Berechnet Z-Wert aus p-Wert (inverse Funktion)"""
    if not 0 <= p_wert <= 1:
        raise ValueError("p-Wert muss zwischen 0 und 1 liegen")
    
    if test_art == "zweiseitig":
        # p = 2 * (1 - norm.cdf(|z|))
        # |z| = norm.ppf(1 - p/2)
        z_abs = norm.ppf(1 - p_wert/2)
        # Wir können das Vorzeichen nicht bestimmen, nehmen positiven Wert
        return z_abs
    elif test_art == "einseitig_links" or test_art == "links":
        # p = norm.cdf(z)
        # z = norm.ppf(p)
        return norm.ppf(p_wert)
    elif test_art == "einseitig_rechts" or test_art == "rechts":
        # p = 1 - norm.cdf(z)
        # z = norm.ppf(1 - p)
        return norm.ppf(1 - p_wert)
    else:
        raise ValueError(f"Unbekannte Testart: {test_art}")


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
    print("HYPOTHESENTEST (Z-TEST)")
    print("=" * 70)
    print("\nFormel: z = (x_bar - mu0) / (sigma / sqrt(n))")
    print("\nVerwendung:")
    print("  python hypothesentest.py x_bar=<wert> mu0=<wert> sigma=<wert> n=<wert> alpha=<wert> test=<art> [z=<wert>] [p=<wert>]")
    print("\nWenn ein Wert unbekannt ist, verwende '-' als Platzhalter")
    print("p = p-Wert (Wahrscheinlichkeit, kann als Dezimalzahl oder Prozent angegeben werden)")
    print("\nTestarten: zweiseitig, einseitig_links, einseitig_rechts (oder: links, rechts)")
    print("\nBeispiele:")
    print("  python hypothesentest.py x_bar=105 mu0=100 sigma=15 n=25 alpha=0.05 test=zweiseitig")
    print("  python hypothesentest.py z=1.67 mu0=100 sigma=15 n=25 alpha=0.05 test=zweiseitig")
    print("  python hypothesentest.py p=0.0956 mu0=100 sigma=15 n=25 alpha=0.05 test=zweiseitig")
    print("  python hypothesentest.py z=1.67 mu0=100 sigma=15 alpha=0.05 test=zweiseitig n=-")
    
    if len(sys.argv) < 2:
        print("\n" + "=" * 70)
        print("Bitte geben Sie die erforderlichen Werte an")
        sys.exit(1)
    
    # Parse Argumente
    x_bar = None
    mu0 = None
    sigma = None
    n = None
    alpha = None
    test_art = None
    z = None
    p_wert = None
    
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
                if key in ['x_bar', 'xbar', 'x', 'stichprobenmittelwert']:
                    x_bar = parsed_value
                elif key in ['mu0', 'μ0', 'mu_0', 'mu_null', 'populationsmittelwert']:
                    mu0 = parsed_value
                elif key in ['sigma', 'σ', 'std', 'standardabweichung']:
                    sigma = parsed_value
                elif key == 'n':
                    n = parsed_value
                elif key in ['alpha', 'α', 'signifikanzniveau', 'signifikanz']:
                    alpha = parsed_value
                elif key == 'z':
                    z = parsed_value
                elif key in ['p', 'p_wert', 'pwert', 'p-value', 'pvalue', 'wahrscheinlichkeit', 'prob']:
                    p_wert = parsed_value
                    # Wenn p als Prozent angegeben wurde (z.B. 9.56 für 9.56%), konvertiere zu Dezimal
                    if p_wert is not None and p_wert > 1:
                        p_wert = p_wert / 100
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
    
    print("\n" + "=" * 70)
    print("EINGEGEBENE WERTE")
    print("=" * 70)
    print(f"  x_bar (Stichprobenmittelwert) = {x_bar if x_bar is not None else '-'}")
    print(f"  mu0 (angenommener Populationsmittelwert) = {mu0 if mu0 is not None else '-'}")
    print(f"  sigma (Standardabweichung) = {sigma if sigma is not None else '-'}")
    print(f"  n (Stichprobenumfang) = {n if n is not None else '-'}")
    print(f"  alpha (Signifikanzniveau) = {alpha if alpha is not None else '-'}")
    print(f"  Testart = {test_art if test_art else '-'}")
    if z is not None:
        # Berechne p-Wert für Anzeige (falls noch nicht berechnet)
        if p_wert is None:
            test_art_fuer_p = test_art if test_art else 'zweiseitig'
            p_wert_temp = get_p_wert(z, test_art_fuer_p)
            print(f"  z (Teststatistik) = {z:.6f} ({p_wert_temp*100:.5f}%)")
        else:
            print(f"  z (Teststatistik) = {z:.6f} ({p_wert*100:.5f}%)")
    if p_wert is not None:
        print(f"  p (p-Wert) = {p_wert:.6f} ({p_wert*100:.4f}%)")
    
    # Berechne fehlende Werte
    print("\n" + "=" * 70)
    print("BERECHNUNGEN")
    print("=" * 70)
    
    berechnungen = []
    
    # Berechne z (Teststatistik) - Priorität: gegeben > aus p > aus x_bar/mu0/sigma/n
    if z is None:
        if p_wert is not None and test_art:
            # Berechne z aus p-Wert
            z = berechne_z_aus_p_wert(p_wert, test_art)
            berechnungen.append(f"z = Phi^(-1)(p) = Phi^(-1)({p_wert}) = {z:.6f} (aus p-Wert berechnet)")
        elif x_bar is not None and mu0 is not None and sigma is not None and n is not None:
            z = berechne_z_test(x_bar, mu0, sigma, n)
            standardfehler = sigma / math.sqrt(n)
            berechnungen.append(f"z = (x_bar - mu0) / (sigma / sqrt(n)) = ({x_bar} - {mu0}) / ({sigma} / sqrt({n})) = {z:.6f}")
            berechnungen.append(f"  Standardfehler = sigma / sqrt(n) = {sigma} / sqrt({n}) = {standardfehler:.6f}")
    else:
        berechnungen.append(f"z = {z:.6f} (gegeben)")
    
    # Berechne p-Wert aus z (falls nicht gegeben)
    # Wenn test_art nicht gegeben, verwende zweiseitig als Standard
    test_art_fuer_p = test_art if test_art else 'zweiseitig'
    
    if p_wert is None and z is not None:
        p_wert = get_p_wert(z, test_art_fuer_p)
        if test_art:
            berechnungen.append(f"p = {p_wert:.6f} ({p_wert*100:.4f}%) (aus z berechnet, {test_art})")
        else:
            berechnungen.append(f"p = {p_wert:.6f} ({p_wert*100:.4f}%) (aus z berechnet, zweiseitig als Standard)")
    elif p_wert is not None:
        berechnungen.append(f"p = {p_wert:.6f} ({p_wert*100:.4f}%) (gegeben)")
    
    # Berechne x_bar
    if x_bar is None:
        if z is not None and mu0 is not None and sigma is not None and n is not None:
            x_bar = berechne_x_bar(z, mu0, sigma, n)
            standardfehler = sigma / math.sqrt(n)
            berechnungen.append(f"x_bar = mu0 + z * (sigma / sqrt(n)) = {mu0} + {z} * ({sigma} / sqrt({n})) = {x_bar:.6f}")
    else:
        if sigma is not None and n is not None:
            standardfehler = sigma / math.sqrt(n)
            berechnungen.append(f"Standardfehler = sigma / sqrt(n) = {sigma} / sqrt({n}) = {standardfehler:.6f}")
    
    # Berechne mu0
    if mu0 is None:
        if x_bar is not None and z is not None and sigma is not None and n is not None:
            mu0 = berechne_mu0(x_bar, z, sigma, n)
            berechnungen.append(f"mu0 = x_bar - z * (sigma / sqrt(n)) = {x_bar} - {z} * ({sigma} / sqrt({n})) = {mu0:.6f}")
    
    # Berechne sigma
    if sigma is None:
        if x_bar is not None and mu0 is not None and z is not None and n is not None:
            sigma = berechne_sigma(x_bar, mu0, z, n)
            berechnungen.append(f"sigma = (x_bar - mu0) * sqrt(n) / z = ({x_bar} - {mu0}) * sqrt({n}) / {z} = {sigma:.6f}")
    
    # Berechne n
    if n is None:
        if x_bar is not None and mu0 is not None and sigma is not None and z is not None:
            n = berechne_n(x_bar, mu0, sigma, z)
            berechnungen.append(f"n = (z * sigma / (x_bar - mu0))^2 = ({z} * {sigma} / ({x_bar} - {mu0}))^2 = {n:.2f}")
            n = int(math.ceil(n))  # Aufrunden auf ganze Zahl (mindestens n)
            berechnungen.append(f"  (aufgerundet: n = {n})")
    
    for berechnung in berechnungen:
        print(f"  {berechnung}")
    
    # Berechne kritischen z-Wert wenn alpha gegeben ist
    if alpha is not None:
        print("\n" + "=" * 70)
        print("KRITISCHER Z-WERT")
        print("=" * 70)
        
        # Wenn test_art nicht gegeben, zeige beide Varianten oder verwende zweiseitig
        if test_art:
            z_kritisch = get_kritischer_wert(alpha, test_art)
            print(f"\nKritischer Z-Wert (alpha = {alpha}, {test_art}):")
            if test_art == "zweiseitig":
                print(f"  z_kritisch = ±{abs(z_kritisch):.6f}")
                print(f"  z_{1-alpha/2:.3f} = {abs(z_kritisch):.6f}")
            elif test_art == "einseitig_links":
                print(f"  z_kritisch = {z_kritisch:.6f}")
                print(f"  z_{alpha:.3f} = {z_kritisch:.6f}")
            else:  # einseitig_rechts
                print(f"  z_kritisch = {z_kritisch:.6f}")
                print(f"  z_{1-alpha:.3f} = {z_kritisch:.6f}")
        else:
            # Zeige beide Varianten wenn test_art nicht gegeben
            z_kritisch_zweiseitig = get_kritischer_wert(alpha, 'zweiseitig')
            z_kritisch_rechts = get_kritischer_wert(alpha, 'einseitig_rechts')
            z_kritisch_links = get_kritischer_wert(alpha, 'einseitig_links')
            
            print(f"\nKritischer Z-Wert (alpha = {alpha}):")
            print(f"  Zweiseitig: z_kritisch = ±{abs(z_kritisch_zweiseitig):.6f} (z_{1-alpha/2:.3f} = {abs(z_kritisch_zweiseitig):.6f})")
            print(f"  Einseitig rechts: z_kritisch = {z_kritisch_rechts:.6f} (z_{1-alpha:.3f} = {z_kritisch_rechts:.6f})")
            print(f"  Einseitig links: z_kritisch = {z_kritisch_links:.6f} (z_{alpha:.3f} = {z_kritisch_links:.6f})")
    
    # Hypothesentest durchführen wenn alle nötigen Werte vorhanden
    if z is not None and alpha is not None and test_art:
        print("\n" + "=" * 70)
        print("HYPOTHESENTEST")
        print("=" * 70)
        
        # Kritischer Wert (wurde bereits oben ausgegeben)
        z_kritisch = get_kritischer_wert(alpha, test_art)
        
        # p-Wert (falls noch nicht berechnet)
        if p_wert is None:
            p_wert = get_p_wert(z, test_art)
        print(f"\np-Wert: {p_wert:.6f} ({p_wert*100:.4f}%)")
        
        # Entscheidung
        print(f"\nEntscheidung:")
        print(f"  H0: mu = {mu0 if mu0 else '?'}")
        if test_art == "zweiseitig":
            ablehnen = abs(z) > abs(z_kritisch)
            print(f"  H1: mu != {mu0 if mu0 else '?'}")
            print(f"  |z| = {abs(z):.6f} {'>' if ablehnen else '<='} |z_kritisch| = {abs(z_kritisch):.6f}")
        elif test_art == "einseitig_links":
            ablehnen = z < z_kritisch
            print(f"  H1: mu < {mu0 if mu0 else '?'}")
            print(f"  z = {z:.6f} {'<' if ablehnen else '>='} z_kritisch = {z_kritisch:.6f}")
        else:  # einseitig_rechts
            ablehnen = z > z_kritisch
            print(f"  H1: mu > {mu0 if mu0 else '?'}")
            print(f"  z = {z:.6f} {'>' if ablehnen else '<='} z_kritisch = {z_kritisch:.6f}")
        
        print(f"  p = {p_wert:.6f} {'<' if p_wert < alpha else '>='} alpha = {alpha}")
        
        if ablehnen:
            print(f"\n  OK H0 wird ABGELEHNT (p < alpha)")
            print(f"  -> Es gibt signifikante Evidenz gegen H0")
        else:
            print(f"\n  OK H0 wird NICHT ABGELEHNT (p >= alpha)")
            print(f"  -> Keine signifikante Evidenz gegen H0")
    
    # Zusammenfassung
    print("\n" + "=" * 70)
    print("ERGEBNIS")
    print("=" * 70)
    if x_bar is not None:
        print(f"  x_bar (Stichprobenmittelwert) = {x_bar:.6f}")
    if mu0 is not None:
        print(f"  mu0 (angenommener Populationsmittelwert) = {mu0:.6f}")
    if sigma is not None:
        print(f"  sigma (Standardabweichung) = {sigma:.6f}")
    if n is not None:
        print(f"  n (Stichprobenumfang) = {n}")
    if z is not None:
        # Berechne p-Wert für Anzeige (falls noch nicht berechnet)
        if p_wert is None:
            test_art_fuer_p = test_art if test_art else 'zweiseitig'
            p_wert_temp = get_p_wert(z, test_art_fuer_p)
            print(f"  z (Teststatistik) = {z:.6f} ({p_wert_temp*100:.5f}%)")
        else:
            print(f"  z (Teststatistik) = {z:.6f} ({p_wert*100:.5f}%)")
    if p_wert is not None:
        print(f"  p (p-Wert) = {p_wert:.6f} ({p_wert*100:.4f}%)")
    if alpha is not None:
        print(f"  alpha (Signifikanzniveau) = {alpha}")
    if test_art:
        print(f"  Testart = {test_art}")
