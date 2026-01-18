"""
Konfidenzintervall Berechnung

Berechnet Konfidenzintervalle fuer den Mittelwert mu und fuer die Varianz sigma².
Unterscheidet automatisch zwischen verschiedenen Formeln basierend auf den Eingaben.

Formel 1 (Z-Test, μ bei bekannter σ): x_bar +/- z_{1-alpha/2} * sigma/sqrt(n)
Formel 2 (t-Test, μ bei unbekannter σ): x_bar +/- t_{n-1; 1-alpha/2} * s/sqrt(n)
Formel 3 (Chi²-Test, σ²): [(n-1)*s²/χ²_{α/2}(n-1) ; (n-1)*s²/χ²_{1-α/2}(n-1)]
"""

import sys
import math
from scipy.stats import norm, t, chi2


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


def berechne_konfidenzintervall_varianz(s, n, alpha, seite="zweiseitig"):
    """
    Berechnet Konfidenzintervall fuer die Varianz sigma² (Chi-Quadrat-Verteilung)
    
    Formel: [(n-1)*s²/Chi²_{alpha/2}(n-1) ; (n-1)*s²/Chi²_{1-alpha/2}(n-1)]
    """
    if n <= 1:
        raise ValueError("Stichprobenumfang n muss > 1 sein für Varianz-Konfidenzintervall")
    if s <= 0:
        raise ValueError("Standardabweichung s muss > 0 sein")
    if not 0 < alpha < 1:
        raise ValueError("Irrtumswahrscheinlichkeit alpha muss zwischen 0 und 1 liegen")
    
    df = n - 1  # Freiheitsgrade
    s_quadrat = s * s  # Stichprobenvarianz s²
    
    if seite == "zweiseitig":
        chi2_links = chi2.ppf(alpha/2, df)      # Chi²_{alpha/2}(n-1)
        chi2_rechts = chi2.ppf(1 - alpha/2, df)  # Chi²_{1-alpha/2}(n-1)
        untere_grenze_var = (df * s_quadrat) / chi2_rechts
        obere_grenze_var = (df * s_quadrat) / chi2_links
    elif seite == "einseitig_links" or seite == "links":
        chi2_rechts = chi2.ppf(1 - alpha, df)
        untere_grenze_var = 0
        obere_grenze_var = (df * s_quadrat) / chi2_rechts
    elif seite == "einseitig_rechts" or seite == "rechts":
        chi2_links = chi2.ppf(alpha, df)
        untere_grenze_var = (df * s_quadrat) / chi2_links
        obere_grenze_var = float('inf')
    else:
        raise ValueError(f"Unbekannte Seite: {seite}")
    
    # Konfidenzintervall für Standardabweichung (Wurzel aus Varianz)
    untere_grenze_sigma = math.sqrt(untere_grenze_var) if untere_grenze_var >= 0 else 0
    obere_grenze_sigma = math.sqrt(obere_grenze_var) if obere_grenze_var != float('inf') else float('inf')
    
    return untere_grenze_var, obere_grenze_var, untere_grenze_sigma, obere_grenze_sigma, chi2_links if seite != "einseitig_rechts" else chi2.ppf(alpha, df), chi2_rechts if seite != "einseitig_links" else chi2.ppf(1 - alpha, df), df


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
    print("\nFormel 1 (Z-Test, mu bei bekannter sigma): x_bar +/- z_{1-alpha/2} * sigma/sqrt(n)")
    print("Formel 2 (t-Test, mu bei unbekannter sigma): x_bar +/- t_{n-1; 1-alpha/2} * s/sqrt(n)")
    print("Formel 3 (Chi²-Test, sigma²): [(n-1)*s²/Chi²_{alpha/2}(n-1) ; (n-1)*s²/Chi²_{1-alpha/2}(n-1)]")
    print("\nVerwendung:")
    print("  # Konfidenzintervall fuer mu (Mittelwert):")
    print("  python konfidenzintervall.py x_bar=<wert> n=<wert> alpha=<wert> seite=<art> [sigma=<wert>] [s=<wert>] [shoch2=<wert>]")
    print("  # Konfidenzintervall fuer sigma² (Varianz):")
    print("  python konfidenzintervall.py n=<wert> alpha=<wert> seite=<art> s=<wert> [shoch2=<wert>] [fuer_varianz=true]")
    print("\nWenn ein Wert unbekannt ist, verwende '-' als Platzhalter")
    print("shoch2 = Varianz (wird automatisch in s umgerechnet: s = sqrt(shoch2))")
    print("fuer_varianz = true wenn Konfidenzintervall für Varianz/Standardabweichung gewünscht")
    print("\nSeiten: zweiseitig, einseitig_links, einseitig_rechts (oder: links, rechts)")
    print("\nBeispiele:")
    print("  # Konfidenzintervall fuer mu (t-Test)")
    print("  python konfidenzintervall.py x_bar=9 n=31 alpha=0.05 seite=zweiseitig shoch2=31/4")
    print("  # Konfidenzintervall fuer sigma² (Varianz)")
    print("  python konfidenzintervall.py n=31 alpha=0.05 seite=zweiseitig s=2.78 fuer_varianz=true")
    print("  # Konfidenzintervall fuer mu (Z-Test)")
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
    fuer_varianz = False  # Ob Konfidenzintervall für Varianz berechnet werden soll
    
    for arg in sys.argv[1:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            key = key.lower().strip()
            
            # Seite wird nicht als Zahl geparst
            if key in ['seite', 'side', 'art', 'test']:
                seite = value.strip().lower()
                continue
            
            # fuer_varianz wird nicht als Zahl geparst
            if key in ['fuer_varianz', 'fuervarianz', 'fuer_variance', 'typ', 'type']:
                if value.strip().lower() in ['true', '1', 'yes', 'ja', 'varianz', 'variance', 'sigma2']:
                    fuer_varianz = True
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
    
    # Bestimme, was berechnet werden soll
    # Wenn fuer_varianz=true ODER x_bar nicht gegeben aber s/shoch2 gegeben → Varianz-KI
    if fuer_varianz or (x_bar is None and (s is not None or shoch2 is not None)):
        intervalltyp = "varianz"
    else:
        # Bestimme Testtyp für Mittelwert: Z-Test wenn sigma gegeben, sonst t-Test
        if sigma is not None:
            testtyp = "z"
        elif s is not None:
            testtyp = "t"
        else:
            print("\nFEHLER: Entweder sigma (für Z-Test) oder s/shoch2 (für t-Test/Varianz-KI) muss angegeben werden!")
            sys.exit(1)
        intervalltyp = "mittelwert"
    
    # Validierung
    if intervalltyp == "mittelwert" and x_bar is None:
        print("\nFEHLER: x_bar muss für Konfidenzintervall des Mittelwerts angegeben werden!")
        sys.exit(1)
    if intervalltyp == "varianz" and s is None:
        print("\nFEHLER: s oder shoch2 muss für Konfidenzintervall der Varianz angegeben werden!")
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
    if intervalltyp == "mittelwert":
        print(f"  x_bar (Stichprobenmittelwert) = {x_bar}")
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
    else:  # varianz
        if s_verwendet:
            print(f"  shoch2 (Varianz) = {shoch2}")
            print(f"  s (Stichprobenstandardabweichung) = {s:.6f} (aus shoch2 berechnet: s = sqrt(shoch2))")
        else:
            print(f"  s (Stichprobenstandardabweichung) = {s}")
        print(f"  Testtyp: Chi²-Test (Konfidenzintervall fuer Varianz sigma², df = {n-1})")
    print(f"  n (Stichprobenumfang) = {n}")
    print(f"  alpha (Irrtumswahrscheinlichkeit) = {alpha}")
    print(f"  Seite = {seite}")
    
    # Berechne Konfidenzintervall
    print("\n" + "=" * 70)
    print("BERECHNUNGEN")
    print("=" * 70)
    
    berechnungen = []
    
    if s_verwendet:
        berechnungen.append(f"s = sqrt(shoch2) = sqrt({shoch2}) = {s:.6f}")
    
    if intervalltyp == "varianz":
        # KONFIDENZINTERVALL FÜR VARIANZ
        untere_grenze_var, obere_grenze_var, untere_grenze_sigma, obere_grenze_sigma, chi2_links, chi2_rechts, df = berechne_konfidenzintervall_varianz(s, n, alpha, seite)
        s_quadrat = s * s
        berechnungen.append(f"Freiheitsgrade (df) = n - 1 = {n} - 1 = {df}")
        berechnungen.append(f"Stichprobenvarianz s² = {s:.6f}² = {s_quadrat:.6f}")
        
        if seite == "zweiseitig":
            berechnungen.append(f"Chi²_{{alpha/2}} = Chi²_{{{alpha/2:.4f}}} = Chi²_{{{df}}} = {chi2_links:.6f}")
            berechnungen.append(f"Chi²_{{1-alpha/2}} = Chi²_{{{1-alpha/2:.4f}}} = Chi²_{{{df}}} = {chi2_rechts:.6f}")
            berechnungen.append(f"Untere Grenze sigma² = (n-1)*s² / Chi²_{{1-alpha/2}} = {df} * {s_quadrat:.6f} / {chi2_rechts:.6f} = {untere_grenze_var:.6f}")
            berechnungen.append(f"Obere Grenze sigma² = (n-1)*s² / Chi²_{{alpha/2}} = {df} * {s_quadrat:.6f} / {chi2_links:.6f} = {obere_grenze_var:.6f}")
            berechnungen.append(f"Konfidenzintervall fuer sigma²: [{untere_grenze_var:.6f}, {obere_grenze_var:.6f}]")
            berechnungen.append(f"Konfidenzintervall fuer sigma: [{untere_grenze_sigma:.6f}, {obere_grenze_sigma:.6f}]")
        elif seite == "einseitig_links":
            berechnungen.append(f"Chi²_{{1-alpha}} = Chi²_{{{1-alpha:.4f}}} = Chi²_{{{df}}} = {chi2_rechts:.6f}")
            berechnungen.append(f"Obere Grenze sigma² = (n-1)*s² / Chi²_{{1-alpha}} = {df} * {s_quadrat:.6f} / {chi2_rechts:.6f} = {obere_grenze_var:.6f}")
            berechnungen.append(f"Konfidenzintervall fuer sigma²: [0, {obere_grenze_var:.6f}]")
            berechnungen.append(f"Konfidenzintervall fuer sigma: [0, {obere_grenze_sigma:.6f}]")
        else:
            berechnungen.append(f"Chi²_{{alpha}} = Chi²_{{{alpha:.4f}}} = Chi²_{{{df}}} = {chi2_links:.6f}")
            berechnungen.append(f"Untere Grenze sigma² = (n-1)*s² / Chi²_{{alpha}} = {df} * {s_quadrat:.6f} / {chi2_links:.6f} = {untere_grenze_var:.6f}")
            berechnungen.append(f"Konfidenzintervall fuer sigma²: [{untere_grenze_var:.6f}, +inf)")
            berechnungen.append(f"Konfidenzintervall fuer sigma: [{untere_grenze_sigma:.6f}, +inf)")
    
    elif testtyp == "z":
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
    
    if intervalltyp == "varianz":
        print(f"  s (Stichprobenstandardabweichung) = {s:.6f}")
        print(f"  s² (Stichprobenvarianz) = {s*s:.6f}")
        print(f"  n (Stichprobenumfang) = {n}")
        print(f"  Freiheitsgrade (df) = {df}")
        print(f"  alpha (Irrtumswahrscheinlichkeit) = {alpha}")
        print(f"  Konfidenzniveau = {(1-alpha)*100:.2f}%")
        print(f"  Seite = {seite}")
        
        if seite == "zweiseitig":
            print(f"\n  Konfidenzintervall fuer sigma² ({(1-alpha)*100:.2f}%): [{untere_grenze_var:.6f}, {obere_grenze_var:.6f}]")
            print(f"  Konfidenzintervall fuer sigma ({(1-alpha)*100:.2f}%): [{untere_grenze_sigma:.6f}, {obere_grenze_sigma:.6f}]")
            print(f"  Breite des Intervalls (sigma²): {obere_grenze_var - untere_grenze_var:.6f}")
            print(f"  Breite des Intervalls (sigma): {obere_grenze_sigma - untere_grenze_sigma:.6f}")
        elif seite == "einseitig_links":
            print(f"\n  Konfidenzintervall fuer sigma² ({(1-alpha)*100:.2f}%): [0, {obere_grenze_var:.6f}]")
            print(f"  Konfidenzintervall fuer sigma ({(1-alpha)*100:.2f}%): [0, {obere_grenze_sigma:.6f}]")
        else:  # einseitig_rechts
            print(f"\n  Konfidenzintervall fuer sigma² ({(1-alpha)*100:.2f}%): [{untere_grenze_var:.6f}, +inf)")
            print(f"  Konfidenzintervall fuer sigma ({(1-alpha)*100:.2f}%): [{untere_grenze_sigma:.6f}, +inf)")
    else:
        # Mittelwert-KI
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
            print(f"\n  Konfidenzintervall fuer mu ({(1-alpha)*100:.2f}%): [{untere_grenze:.6f}, {obere_grenze:.6f}]")
            print(f"  Breite des Intervalls: {obere_grenze - untere_grenze:.6f}")
        elif seite == "einseitig_links":
            print(f"\n  Konfidenzintervall fuer mu ({(1-alpha)*100:.2f}%): (-inf, {obere_grenze:.6f}]")
        else:  # einseitig_rechts
            print(f"\n  Konfidenzintervall fuer mu ({(1-alpha)*100:.2f}%): (-inf, {obere_grenze:.6f}]")
