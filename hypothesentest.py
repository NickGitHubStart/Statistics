"""
Hypothesentest (Z-Test und t-Test)

Berechnet alle relevanten Werte für einen Hypothesentest.
Unterscheidet automatisch zwischen Z-Test (σ bekannt) und t-Test (nur s bekannt).

Formel 1 (Z-Test): z = (x_bar - mu0) / (sigma / sqrt(n))
Formel 2 (t-Test): t = (x_bar - mu0) / (s / sqrt(n))
"""

import sys
import math
from scipy.stats import norm, t


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


# t-Test Funktionen
def berechne_t_test(x_bar, mu0, s, n):
    """Berechnet Teststatistik: t = (x_bar - mu0) / (s / sqrt(n))"""
    if n <= 1:
        raise ValueError("Stichprobenumfang n muss > 1 sein für t-Test")
    if s <= 0:
        raise ValueError("Standardabweichung s muss > 0 sein")
    standardfehler = s / math.sqrt(n)
    return (x_bar - mu0) / standardfehler


def berechne_x_bar_t(t_val, mu0, s, n):
    """Berechnet Stichprobenmittelwert: x_bar = mu0 + t * (s / sqrt(n))"""
    standardfehler = s / math.sqrt(n)
    return mu0 + t_val * standardfehler


def berechne_mu0_t(x_bar, t_val, s, n):
    """Berechnet angenommenen Populationsmittelwert: mu0 = x_bar - t * (s / sqrt(n))"""
    standardfehler = s / math.sqrt(n)
    return x_bar - t_val * standardfehler


def berechne_s_t(x_bar, mu0, t_val, n):
    """Berechnet Standardabweichung: s = (x_bar - mu0) * sqrt(n) / t"""
    if t_val == 0:
        raise ValueError("t-Wert darf nicht 0 sein")
    if n <= 1:
        raise ValueError("Stichprobenumfang n muss > 1 sein")
    return (x_bar - mu0) * math.sqrt(n) / t_val


def berechne_n_t(x_bar, mu0, s, t_val):
    """Berechnet Stichprobenumfang: n = (t * s / (x_bar - mu0))^2"""
    if t_val == 0:
        raise ValueError("t-Wert darf nicht 0 sein")
    if s <= 0:
        raise ValueError("Standardabweichung s muss > 0 sein")
    if x_bar == mu0:
        raise ValueError("x_bar und mu0 duerfen nicht gleich sein (Division durch 0)")
    return (t_val * s / (x_bar - mu0)) ** 2


def get_kritischer_wert_t(alpha, test_art, df):
    """Berechnet kritischen t-Wert basierend auf alpha, Testart und Freiheitsgraden"""
    if test_art == "zweiseitig":
        return t.ppf(1 - alpha/2, df)
    elif test_art == "einseitig_links" or test_art == "links":
        return t.ppf(alpha, df)
    elif test_art == "einseitig_rechts" or test_art == "rechts":
        return t.ppf(1 - alpha, df)
    else:
        raise ValueError(f"Unbekannte Testart: {test_art}")


def get_p_wert_t(t_val, test_art, df):
    """Berechnet p-Wert basierend auf t-Wert, Testart und Freiheitsgraden"""
    if test_art == "zweiseitig":
        return 2 * (1 - t.cdf(abs(t_val), df))
    elif test_art == "einseitig_links" or test_art == "links":
        return t.cdf(t_val, df)
    elif test_art == "einseitig_rechts" or test_art == "rechts":
        return 1 - t.cdf(t_val, df)
    else:
        raise ValueError(f"Unbekannte Testart: {test_art}")


def berechne_t_aus_p_wert(p_wert, test_art, df):
    """Berechnet t-Wert aus p-Wert (inverse Funktion)"""
    if not 0 <= p_wert <= 1:
        raise ValueError("p-Wert muss zwischen 0 und 1 liegen")
    
    if test_art == "zweiseitig":
        t_abs = t.ppf(1 - p_wert/2, df)
        return t_abs
    elif test_art == "einseitig_links" or test_art == "links":
        return t.ppf(p_wert, df)
    elif test_art == "einseitig_rechts" or test_art == "rechts":
        return t.ppf(1 - p_wert, df)
    else:
        raise ValueError(f"Unbekannte Testart: {test_art}")


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
    print("HYPOTHESENTEST (Z-TEST UND T-TEST)")
    print("=" * 70)
    print("\nFormel 1 (Z-Test, sigma bekannt): z = (x_bar - mu0) / (sigma / sqrt(n))")
    print("Formel 2 (t-Test, nur s bekannt): t = (x_bar - mu0) / (s / sqrt(n))")
    print("\nVerwendung:")
    print("  python hypothesentest.py x_bar=<wert> mu0=<wert> n=<wert> alpha=<wert> test=<art> [sigma=<wert>] [s=<wert>] [shoch2=<wert>] [z=<wert>] [t=<wert>] [p=<wert>]")
    print("\nWenn ein Wert unbekannt ist, verwende '-' als Platzhalter")
    print("p = p-Wert (Wahrscheinlichkeit, kann als Dezimalzahl oder Prozent angegeben werden)")
    print("shoch2 = Varianz (wird automatisch in s umgerechnet: s = sqrt(shoch2))")
    print("\nTestarten: zweiseitig, einseitig_links, einseitig_rechts (oder: links, rechts)")
    print("\nBeispiele:")
    print("  # Z-Test (sigma bekannt)")
    print("  python hypothesentest.py x_bar=105 mu0=100 sigma=15 n=25 alpha=0.05 test=zweiseitig")
    print("  # t-Test (nur s bekannt)")
    print("  python hypothesentest.py x_bar=105 mu0=100 s=15 n=25 alpha=0.05 test=zweiseitig")
    print("  # t-Test mit Varianz")
    print("  python hypothesentest.py x_bar=105 mu0=100 shoch2=225 n=25 alpha=0.05 test=zweiseitig")
    
    if len(sys.argv) < 2:
        print("\n" + "=" * 70)
        print("Bitte geben Sie die erforderlichen Werte an")
        sys.exit(1)
    
    # Parse Argumente
    x_bar = None
    mu0 = None
    sigma = None  # Für Z-Test
    s = None      # Für t-Test
    shoch2 = None # Varianz (wird in s umgerechnet)
    n = None
    alpha = None
    test_art = None
    z = None      # Für Z-Test
    t_val = None  # Für t-Test
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
                elif key in ['sigma', 'std_pop', 'standardabweichung_population']:
                    sigma = parsed_value
                elif key in ['s', 'std', 'standardabweichung_stichprobe']:
                    s = parsed_value
                elif key in ['shoch2', 's^2', 's2', 'var', 'varianz', 'variance']:
                    shoch2 = parsed_value
                elif key == 'n':
                    n = parsed_value
                elif key in ['alpha', 'α', 'signifikanzniveau', 'signifikanz']:
                    alpha = parsed_value
                elif key == 'z':
                    z = parsed_value
                elif key == 't':
                    t_val = parsed_value
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
    
    print("\n" + "=" * 70)
    print("EINGEGEBENE WERTE")
    print("=" * 70)
    print(f"  x_bar (Stichprobenmittelwert) = {x_bar if x_bar is not None else '-'}")
    print(f"  mu0 (angenommener Populationsmittelwert) = {mu0 if mu0 is not None else '-'}")
    if testtyp == "z":
        print(f"  sigma (Populationsstandardabweichung) = {sigma}")
        print(f"  Testtyp: Z-Test (sigma bekannt)")
    else:
        if s_verwendet:
            print(f"  shoch2 (Varianz) = {shoch2}")
            print(f"  s (Stichprobenstandardabweichung) = {s:.6f} (aus shoch2 berechnet: s = sqrt(shoch2))")
        else:
            print(f"  s (Stichprobenstandardabweichung) = {s}")
        print(f"  Testtyp: t-Test (nur s bekannt, df = {n-1 if n else '?'})")
    print(f"  n (Stichprobenumfang) = {n if n is not None else '-'}")
    print(f"  alpha (Signifikanzniveau) = {alpha if alpha is not None else '-'}")
    print(f"  Testart = {test_art if test_art else '-'}")
    if z is not None:
        if p_wert is None:
            test_art_fuer_p = test_art if test_art else 'zweiseitig'
            p_wert_temp = get_p_wert(z, test_art_fuer_p)
            print(f"  z (Teststatistik) = {z:.6f} ({p_wert_temp*100:.5f}%)")
        else:
            print(f"  z (Teststatistik) = {z:.6f} ({p_wert*100:.5f}%)")
    if t_val is not None:
        if p_wert is None and n is not None:
            test_art_fuer_p = test_art if test_art else 'zweiseitig'
            df = n - 1
            p_wert_temp = get_p_wert_t(t_val, test_art_fuer_p, df)
            print(f"  t (Teststatistik) = {t_val:.6f} ({p_wert_temp*100:.5f}%)")
        else:
            print(f"  t (Teststatistik) = {t_val:.6f}")
    if p_wert is not None:
        print(f"  p (p-Wert) = {p_wert:.6f} ({p_wert*100:.4f}%)")
    
    # Berechne fehlende Werte
    print("\n" + "=" * 70)
    print("BERECHNUNGEN")
    print("=" * 70)
    
    berechnungen = []
    
    if s_verwendet:
        berechnungen.append(f"s = sqrt(shoch2) = sqrt({shoch2}) = {s:.6f}")
    
    # Z-Test oder t-Test?
    if testtyp == "z":
        # Z-TEST
        # Berechne z (Teststatistik) - Priorität: gegeben > aus p > aus x_bar/mu0/sigma/n
        if z is None:
            if p_wert is not None and test_art:
                z = berechne_z_aus_p_wert(p_wert, test_art)
                berechnungen.append(f"z = Phi^(-1)(p) = Phi^(-1)({p_wert}) = {z:.6f} (aus p-Wert berechnet)")
            elif x_bar is not None and mu0 is not None and sigma is not None and n is not None:
                z = berechne_z_test(x_bar, mu0, sigma, n)
                standardfehler = sigma / math.sqrt(n)
                berechnungen.append(f"z = (x_bar - mu0) / (sigma / sqrt(n)) = ({x_bar} - {mu0}) / ({sigma} / sqrt({n})) = {z:.6f}")
                berechnungen.append(f"  Standardfehler = sigma / sqrt(n) = {sigma} / sqrt({n}) = {standardfehler:.6f}")
        else:
            berechnungen.append(f"z = {z:.6f} (gegeben)")
        
        # Berechne p-Wert aus z
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
                n = int(math.ceil(n))
                berechnungen.append(f"  (aufgerundet: n = {n})")
    
    else:
        # T-TEST
        df = n - 1 if n is not None else None
        
        # Berechne t (Teststatistik) - Priorität: gegeben > aus p > aus x_bar/mu0/s/n
        if t_val is None:
            if p_wert is not None and test_art and df is not None:
                t_val = berechne_t_aus_p_wert(p_wert, test_art, df)
                berechnungen.append(f"t = t^(-1)(p) = t^(-1)({p_wert}) = {t_val:.6f} (aus p-Wert berechnet)")
            elif x_bar is not None and mu0 is not None and s is not None and n is not None:
                t_val = berechne_t_test(x_bar, mu0, s, n)
                standardfehler = s / math.sqrt(n)
                berechnungen.append(f"t = (x_bar - mu0) / (s / sqrt(n)) = ({x_bar} - {mu0}) / ({s} / sqrt({n})) = {t_val:.6f}")
                berechnungen.append(f"  Standardfehler = s / sqrt(n) = {s} / sqrt({n}) = {standardfehler:.6f}")
                berechnungen.append(f"  Freiheitsgrade (df) = n - 1 = {n} - 1 = {df}")
        else:
            berechnungen.append(f"t = {t_val:.6f} (gegeben)")
            if df is not None:
                berechnungen.append(f"  Freiheitsgrade (df) = n - 1 = {n} - 1 = {df}")
        
        # Berechne p-Wert aus t
        test_art_fuer_p = test_art if test_art else 'zweiseitig'
        if p_wert is None and t_val is not None and df is not None:
            p_wert = get_p_wert_t(t_val, test_art_fuer_p, df)
            if test_art:
                berechnungen.append(f"p = {p_wert:.6f} ({p_wert*100:.4f}%) (aus t berechnet, {test_art})")
            else:
                berechnungen.append(f"p = {p_wert:.6f} ({p_wert*100:.4f}%) (aus t berechnet, zweiseitig als Standard)")
        elif p_wert is not None:
            berechnungen.append(f"p = {p_wert:.6f} ({p_wert*100:.4f}%) (gegeben)")
        
        # Berechne x_bar
        if x_bar is None:
            if t_val is not None and mu0 is not None and s is not None and n is not None:
                x_bar = berechne_x_bar_t(t_val, mu0, s, n)
                standardfehler = s / math.sqrt(n)
                berechnungen.append(f"x_bar = mu0 + t * (s / sqrt(n)) = {mu0} + {t_val} * ({s} / sqrt({n})) = {x_bar:.6f}")
        else:
            if s is not None and n is not None:
                standardfehler = s / math.sqrt(n)
                berechnungen.append(f"Standardfehler = s / sqrt(n) = {s} / sqrt({n}) = {standardfehler:.6f}")
                if df is not None:
                    berechnungen.append(f"Freiheitsgrade (df) = n - 1 = {n} - 1 = {df}")
        
        # Berechne mu0
        if mu0 is None:
            if x_bar is not None and t_val is not None and s is not None and n is not None:
                mu0 = berechne_mu0_t(x_bar, t_val, s, n)
                berechnungen.append(f"mu0 = x_bar - t * (s / sqrt(n)) = {x_bar} - {t_val} * ({s} / sqrt({n})) = {mu0:.6f}")
        
        # Berechne s
        if s is None:
            if x_bar is not None and mu0 is not None and t_val is not None and n is not None:
                s = berechne_s_t(x_bar, mu0, t_val, n)
                berechnungen.append(f"s = (x_bar - mu0) * sqrt(n) / t = ({x_bar} - {mu0}) * sqrt({n}) / {t_val} = {s:.6f}")
        
        # Berechne n
        if n is None:
            if x_bar is not None and mu0 is not None and s is not None and t_val is not None:
                n = berechne_n_t(x_bar, mu0, s, t_val)
                berechnungen.append(f"n = (t * s / (x_bar - mu0))^2 = ({t_val} * {s} / ({x_bar} - {mu0}))^2 = {n:.2f}")
                n = int(math.ceil(n))
                berechnungen.append(f"  (aufgerundet: n = {n})")
                df = n - 1
    
    for berechnung in berechnungen:
        print(f"  {berechnung}")
    
    # Berechne kritischen Wert wenn alpha gegeben ist
    if alpha is not None:
        print("\n" + "=" * 70)
        if testtyp == "z":
            print("KRITISCHER Z-WERT")
        else:
            print("KRITISCHER T-WERT")
        print("=" * 70)
        
        if testtyp == "z":
            # Z-TEST
            if test_art:
                kritisch = get_kritischer_wert(alpha, test_art)
                print(f"\nKritischer Z-Wert (alpha = {alpha}, {test_art}):")
                if test_art == "zweiseitig":
                    print(f"  z_kritisch = ±{abs(kritisch):.6f}")
                    print(f"  z_{1-alpha/2:.3f} = {abs(kritisch):.6f}")
                elif test_art == "einseitig_links":
                    print(f"  z_kritisch = {kritisch:.6f}")
                    print(f"  z_{alpha:.3f} = {kritisch:.6f}")
                else:
                    print(f"  z_kritisch = {kritisch:.6f}")
                    print(f"  z_{1-alpha:.3f} = {kritisch:.6f}")
            else:
                kritisch_zweiseitig = get_kritischer_wert(alpha, 'zweiseitig')
                kritisch_rechts = get_kritischer_wert(alpha, 'einseitig_rechts')
                kritisch_links = get_kritischer_wert(alpha, 'einseitig_links')
                print(f"\nKritischer Z-Wert (alpha = {alpha}):")
                print(f"  Zweiseitig: z_kritisch = ±{abs(kritisch_zweiseitig):.6f} (z_{1-alpha/2:.3f} = {abs(kritisch_zweiseitig):.6f})")
                print(f"  Einseitig rechts: z_kritisch = {kritisch_rechts:.6f} (z_{1-alpha:.3f} = {kritisch_rechts:.6f})")
                print(f"  Einseitig links: z_kritisch = {kritisch_links:.6f} (z_{alpha:.3f} = {kritisch_links:.6f})")
        else:
            # T-TEST
            if n is not None:
                df = n - 1
                if test_art:
                    kritisch = get_kritischer_wert_t(alpha, test_art, df)
                    print(f"\nKritischer t-Wert (alpha = {alpha}, {test_art}, df = {df}):")
                    if test_art == "zweiseitig":
                        print(f"  t_kritisch = ±{abs(kritisch):.6f}")
                        print(f"  t_{{{df}; {1-alpha/2:.3f}}} = {abs(kritisch):.6f}")
                    elif test_art == "einseitig_links":
                        print(f"  t_kritisch = {kritisch:.6f}")
                        print(f"  t_{{{df}; {alpha:.3f}}} = {kritisch:.6f}")
                    else:
                        print(f"  t_kritisch = {kritisch:.6f}")
                        print(f"  t_{{{df}; {1-alpha:.3f}}} = {kritisch:.6f}")
                else:
                    kritisch_zweiseitig = get_kritischer_wert_t(alpha, 'zweiseitig', df)
                    kritisch_rechts = get_kritischer_wert_t(alpha, 'einseitig_rechts', df)
                    kritisch_links = get_kritischer_wert_t(alpha, 'einseitig_links', df)
                    print(f"\nKritischer t-Wert (alpha = {alpha}, df = {df}):")
                    print(f"  Zweiseitig: t_kritisch = ±{abs(kritisch_zweiseitig):.6f} (t_{{{df}; {1-alpha/2:.3f}}} = {abs(kritisch_zweiseitig):.6f})")
                    print(f"  Einseitig rechts: t_kritisch = {kritisch_rechts:.6f} (t_{{{df}; {1-alpha:.3f}}} = {kritisch_rechts:.6f})")
                    print(f"  Einseitig links: t_kritisch = {kritisch_links:.6f} (t_{{{df}; {alpha:.3f}}} = {kritisch_links:.6f})")
    
    # Hypothesentest durchführen wenn alle nötigen Werte vorhanden
    if alpha is not None and test_art:
        if testtyp == "z" and z is not None:
            print("\n" + "=" * 70)
            print("HYPOTHESENTEST (Z-TEST)")
            print("=" * 70)
            
            kritisch = get_kritischer_wert(alpha, test_art)
            if p_wert is None:
                p_wert = get_p_wert(z, test_art)
            print(f"\np-Wert: {p_wert:.6f} ({p_wert*100:.4f}%)")
            
            print(f"\nEntscheidung:")
            print(f"  H0: mu = {mu0 if mu0 else '?'}")
            if test_art == "zweiseitig":
                ablehnen = abs(z) > abs(kritisch)
                print(f"  H1: mu != {mu0 if mu0 else '?'}")
                print(f"  |z| = {abs(z):.6f} {'>' if ablehnen else '<='} |z_kritisch| = {abs(kritisch):.6f}")
            elif test_art == "einseitig_links":
                ablehnen = z < kritisch
                print(f"  H1: mu < {mu0 if mu0 else '?'}")
                print(f"  z = {z:.6f} {'<' if ablehnen else '>='} z_kritisch = {kritisch:.6f}")
            else:
                ablehnen = z > kritisch
                print(f"  H1: mu > {mu0 if mu0 else '?'}")
                print(f"  z = {z:.6f} {'>' if ablehnen else '<='} z_kritisch = {kritisch:.6f}")
            
            print(f"  p = {p_wert:.6f} {'<' if p_wert < alpha else '>='} alpha = {alpha}")
            
            if ablehnen:
                print(f"\n  OK H0 wird ABGELEHNT (p < alpha)")
                print(f"  -> Es gibt signifikante Evidenz gegen H0")
            else:
                print(f"\n  OK H0 wird NICHT ABGELEHNT (p >= alpha)")
                print(f"  -> Keine signifikante Evidenz gegen H0")
        
        elif testtyp == "t" and t_val is not None and n is not None:
            print("\n" + "=" * 70)
            print("HYPOTHESENTEST (T-TEST)")
            print("=" * 70)
            
            df = n - 1
            kritisch = get_kritischer_wert_t(alpha, test_art, df)
            if p_wert is None:
                p_wert = get_p_wert_t(t_val, test_art, df)
            print(f"\np-Wert: {p_wert:.6f} ({p_wert*100:.4f}%)")
            
            print(f"\nEntscheidung:")
            print(f"  H0: mu = {mu0 if mu0 else '?'}")
            if test_art == "zweiseitig":
                ablehnen = abs(t_val) > abs(kritisch)
                print(f"  H1: mu != {mu0 if mu0 else '?'}")
                print(f"  |t| = {abs(t_val):.6f} {'>' if ablehnen else '<='} |t_kritisch| = {abs(kritisch):.6f}")
            elif test_art == "einseitig_links":
                ablehnen = t_val < kritisch
                print(f"  H1: mu < {mu0 if mu0 else '?'}")
                print(f"  t = {t_val:.6f} {'<' if ablehnen else '>='} t_kritisch = {kritisch:.6f}")
            else:
                ablehnen = t_val > kritisch
                print(f"  H1: mu > {mu0 if mu0 else '?'}")
                print(f"  t = {t_val:.6f} {'>' if ablehnen else '<='} t_kritisch = {kritisch:.6f}")
            
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
    if testtyp == "z":
        if sigma is not None:
            print(f"  sigma (Populationsstandardabweichung) = {sigma:.6f}")
        if z is not None:
            if p_wert is None:
                test_art_fuer_p = test_art if test_art else 'zweiseitig'
                p_wert_temp = get_p_wert(z, test_art_fuer_p)
                print(f"  z (Teststatistik) = {z:.6f} ({p_wert_temp*100:.5f}%)")
            else:
                print(f"  z (Teststatistik) = {z:.6f} ({p_wert*100:.5f}%)")
    else:
        if s is not None:
            print(f"  s (Stichprobenstandardabweichung) = {s:.6f}")
        if n is not None:
            df = n - 1
            print(f"  Freiheitsgrade (df) = {df}")
        if t_val is not None:
            if p_wert is None and n is not None:
                test_art_fuer_p = test_art if test_art else 'zweiseitig'
                df = n - 1
                p_wert_temp = get_p_wert_t(t_val, test_art_fuer_p, df)
                print(f"  t (Teststatistik) = {t_val:.6f} ({p_wert_temp*100:.5f}%)")
            else:
                print(f"  t (Teststatistik) = {t_val:.6f}")
    if n is not None:
        print(f"  n (Stichprobenumfang) = {n}")
    if p_wert is not None:
        print(f"  p (p-Wert) = {p_wert:.6f} ({p_wert*100:.4f}%)")
    if alpha is not None:
        print(f"  alpha (Signifikanzniveau) = {alpha}")
    if test_art:
        print(f"  Testart = {test_art}")
    print(f"  Testtyp = {testtyp.upper()}-Test")
