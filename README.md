# Statistik-Programme

Sammlung von Python-Programmen für statistische Berechnungen.

## Übersicht

- **z_score.py** - Z-Score Berechnung
- **hypothesentest.py** - Hypothesentest (Z-Test)
- **binomial.py** - Binomialverteilung
- **hypergeometrisch.py** - Hypergeometrische Verteilung
- **poisson.py** - Poisson-Verteilung
- **cohens_d.py** - Cohens d (Effektgröße)

---

## z_score.py

Berechnet Z-Score, Mittelwert, Standardabweichung oder x-Wert.

**Formel:** `z = (x - μ) / σ`

**Verwendung:**
```bash
python z_score.py z=<wert> mu=<wert> sigma=<wert> x=<wert> [p=<wert>]
```

**Beispiele:**
```bash
# Z-Score berechnen
python z_score.py z=- x=85 mu=100 sigma=15

# x-Wert berechnen
python z_score.py z=1.5 mu=100 sigma=15 x=-

# Wahrscheinlichkeit berechnen
python z_score.py z=1.5 p=-
```

**Parameter:**
- `z` - Z-Score
- `mu` - Mittelwert (μ)
- `sigma` - Standardabweichung (σ)
- `x` - Wert
- `p` - Wahrscheinlichkeit P(Z ≤ z)

**Hinweis:** Mindestens 3 der 4 Werte (z, mu, sigma, x) müssen angegeben werden. Verwende `-` für unbekannte Werte.

---

## hypothesentest.py

Führt einen Hypothesentest (Z-Test) durch und berechnet alle relevanten Werte.

**Formel:** `z = (x̄ - μ₀) / (σ / √n)`

**Verwendung:**
```bash
python hypothesentest.py x_bar=<wert> mu0=<wert> sigma=<wert> n=<wert> alpha=<wert> test=<art> [z=<wert>] [p=<wert>]
```

**Beispiele:**
```bash
# Hypothesentest durchführen
python hypothesentest.py x_bar=105 mu0=100 sigma=15 n=25 alpha=0.05 test=zweiseitig

# Z-Wert berechnen
python hypothesentest.py x_bar=105 mu0=100 sigma=15 n=25 alpha=0.05 test=zweiseitig z=-

# p-Wert berechnen
python hypothesentest.py z=1.67 mu0=100 sigma=15 n=25 alpha=0.05 test=zweiseitig
```

**Parameter:**
- `x_bar` - Stichprobenmittelwert (x̄)
- `mu0` - angenommener Populationsmittelwert (μ₀)
- `sigma` - Standardabweichung (σ)
- `n` - Stichprobenumfang
- `alpha` - Signifikanzniveau
- `test` - Testart: `zweiseitig`, `einseitig_links`, `einseitig_rechts` (oder `links`, `rechts`)
- `z` - Teststatistik (optional)
- `p` - p-Wert (optional)

---

## binomial.py

Berechnet Wahrscheinlichkeiten für die Binomialverteilung.

**Formel:** `P(X = k) = (n über k) * p^k * (1-p)^(n-k)`

**Verwendung:**
```bash
python binomial.py k=<wert> n=<wert> p=<wert> [art=<wert>] [--graph]
```

**Beispiele:**
```bash
# Genau k Erfolge
python binomial.py k=2 n=8 p=0.1

# Höchstens k Erfolge
python binomial.py k=2 n=8 p=0.1 art=hoechstens

# Mit Graph
python binomial.py k=2 n=8 p=0.1 art=genau --graph
```

**Parameter:**
- `k` - Anzahl Erfolge
- `n` - Anzahl Versuche
- `p` - Erfolgswahrscheinlichkeit (0-1)
- `art` - Art der Berechnung: `genau`, `höchstens`, `mindestens`, `mehr_als`, `weniger_als` (Standard: `genau`)
- `--graph` - Erstellt einen Graph

---

## hypergeometrisch.py

Berechnet Wahrscheinlichkeiten für die hypergeometrische Verteilung (Ziehen ohne Zurücklegen).

**Formel:** `P(X = k) = (M über k) * (N-M über n-k) / (N über n)`

**Verwendung:**
```bash
python hypergeometrisch.py k=<wert> N=<wert> M=<wert> n=<wert> [art=<wert>] [--graph]
```

**Beispiele:**
```bash
# Genau k Erfolge
python hypergeometrisch.py k=3 N=20 M=12 n=5

# Höchstens k Erfolge
python hypergeometrisch.py k=3 N=20 M=12 n=5 art=hoechstens

# Mit Graph
python hypergeometrisch.py k=3 N=20 M=12 n=5 art=genau --graph
```

**Parameter:**
- `k` - Anzahl Erfolge in Stichprobe
- `N` - Grundgesamtheit
- `M` - Anzahl Erfolge in Grundgesamtheit
- `n` - Stichprobengröße
- `art` - Art der Berechnung: `genau`, `höchstens`, `mindestens`, `mehr_als`, `weniger_als` (Standard: `genau`)
- `--graph` - Erstellt einen Graph

---

## poisson.py

Berechnet Wahrscheinlichkeiten für die Poisson-Verteilung (seltene Ereignisse).

**Formel:** `P(X = k) = (λ^k * e^(-λ)) / k!`

**Verwendung:**
```bash
python poisson.py k=<wert> lambda=<wert> [art=<wert>] [--graph]
```

**Beispiele:**
```bash
# Genau k Ereignisse
python poisson.py k=5 lambda=3

# Höchstens k Ereignisse
python poisson.py k=5 lambda=3 art=hoechstens

# Mit Graph
python poisson.py k=5 lambda=3 art=genau --graph
```

**Parameter:**
- `k` - Anzahl Ereignisse
- `lambda` - Mittlere Rate (λ)
- `art` - Art der Berechnung: `genau`, `höchstens`, `mindestens`, `mehr_als`, `weniger_als` (Standard: `genau`)
- `--graph` - Erstellt einen Graph

---

## cohens_d.py

Berechnet Cohens d (Effektgröße) und alle zugehörigen Werte.

**Formel:** `d = (x̄ - μ) / σ`

**Verwendung:**
```bash
python cohens_d.py d=<wert> x_bar=<wert> mu0=<wert> sigma=<wert>
```

**Beispiele:**
```bash
# Cohens d berechnen
python cohens_d.py x_bar=105 mu0=100 sigma=15 d=-

# x_bar berechnen
python cohens_d.py d=0.5 x_bar=- mu0=100 sigma=15

# mu0 berechnen
python cohens_d.py d=-0.8 x_bar=88 mu0=- sigma=15

# sigma berechnen
python cohens_d.py d=1.2 x_bar=118 mu0=100 sigma=-
```

**Parameter:**
- `d` - Cohens d (Effektgröße)
- `x_bar` - Stichprobenmittelwert (x̄)
- `mu0` - Populationsmittelwert (μ)
- `sigma` - Standardabweichung (σ)

**Hinweis:** Mindestens 3 der 4 Werte müssen angegeben werden. Verwende `-` für unbekannte Werte.

**Interpretation von Cohens d:**
- |d| < 0.2: sehr klein (vernachlässigbar)
- 0.2 ≤ |d| < 0.5: klein
- 0.5 ≤ |d| < 0.8: mittel
- |d| ≥ 0.8: groß

---

## Allgemeine Hinweise

- **Brüche:** Alle Programme unterstützen Brüche als Eingabe, z.B. `p=1/3` oder `sigma=15/2`
- **Unbekannte Werte:** Verwende `-` als Platzhalter für unbekannte Werte
- **Graphs:** Programme mit `--graph` Option erstellen Visualisierungen der Verteilungen
- **Ausgabe:** Alle Programme zeigen detaillierte Berechnungsschritte und Ergebnisse

## Abhängigkeiten

- Python 3.x
- numpy
- scipy
- matplotlib (für Graphs)

Installation:
```bash
pip install numpy scipy matplotlib
```
