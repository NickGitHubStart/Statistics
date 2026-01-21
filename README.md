# Statistik-Programme

Sammlung von Python-Programmen für statistische Berechnungen.

## Übersicht

- **z_score.py** - Z-Score Berechnung
- **hypothesentest.py** - Hypothesentest (Z-Test und t-Test)
- **konfidenzintervall.py** - Konfidenzintervalle (Z-Test, t-Test, Chi²-Test für Varianz)
- **k_sigma.py** - k-Sigma-Regel (Vorhersageintervall für einzelne Beobachtungen)
- **trennschaerfe.py** - Trennschärfe (Power) Berechnung (Einstichproben und Zweistichproben)
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
python z_score.py z=<wert> mu=<wert> sigma=<wert> x=<wert> [p=<wert>] [var=<wert>]
```

**Beispiele:**
```bash
# Z-Score berechnen
python z_score.py z=- x=85 mu=100 sigma=15

# Mit Varianz (wird automatisch in sigma umgerechnet)
python z_score.py z=- x=85 mu=100 var=225

# x-Wert berechnen
python z_score.py z=1.5 mu=100 sigma=15 x=-

# Wahrscheinlichkeit berechnen
python z_score.py z=1.5 p=-
```

**Parameter:**
- `z` - Z-Score (wird mit Prozentwert in Klammern ausgegeben)
- `mu` oder `mu0` - Mittelwert (μ)
- `sigma` - Standardabweichung (σ)
- `var` - Varianz (wird automatisch in sigma umgerechnet: `sigma = sqrt(var)`)
- `x` oder `x_bar` - Wert
- `p` - Wahrscheinlichkeit P(Z ≤ z)

**Hinweis:** 
- Mindestens 3 der 4 Werte (z, mu, sigma, x) müssen angegeben werden. Verwende `-` für unbekannte Werte.
- Wenn `var` angegeben wird, wird es automatisch in `sigma` umgerechnet. Wenn sowohl `var` als auch `sigma` angegeben werden, wird `sigma` verwendet.
- Der Z-Score wird mit dem Prozentwert (p-Wert) in Klammern ausgegeben, z.B. `z = 1.500000 (93.32%)`

---

## hypothesentest.py

Führt einen Hypothesentest durch und berechnet alle relevanten Werte. **Das Programm wählt automatisch zwischen Z-Test und t-Test** basierend auf den eingegebenen Parametern.

**Formeln:**
- **Z-Test** (σ bekannt): `z = (x̄ - μ₀) / (σ / √n)`
- **t-Test** (nur s bekannt): `t = (x̄ - μ₀) / (s / √n)` mit df = n-1

**Automatische Testauswahl:**
- Wenn `sigma` angegeben wird → **Z-Test** wird verwendet
- Wenn `s` oder `shoch2` angegeben wird → **t-Test** wird verwendet

**Verwendung:**
```bash
python hypothesentest.py x_bar=<wert> mu0=<wert> n=<wert> alpha=<wert> test=<art> [sigma=<wert>] [s=<wert>] [shoch2=<wert>] [z=<wert>] [t=<wert>] [p=<wert>]
```

**Beispiele:**
```bash
# Z-Test (sigma bekannt)
python hypothesentest.py x_bar=105 mu0=100 sigma=15 n=25 alpha=0.05 test=zweiseitig

# t-Test (nur s bekannt)
python hypothesentest.py x_bar=105 mu0=100 s=15 n=25 alpha=0.05 test=zweiseitig

# t-Test mit Varianz (wird automatisch in s umgerechnet)
python hypothesentest.py x_bar=105 mu0=100 shoch2=225 n=25 alpha=0.05 test=zweiseitig
```

**Parameter:**
- `x_bar` - Stichprobenmittelwert (x̄)
- `mu0` - angenommener Populationsmittelwert (μ₀)
- `sigma` - Populationsstandardabweichung (σ) - verwendet **Z-Test**
- `s` - Stichprobenstandardabweichung - verwendet **t-Test**
- `shoch2` - Varianz (wird automatisch in s umgerechnet: `s = sqrt(shoch2)`) - verwendet **t-Test**
- `n` - Stichprobenumfang
- `alpha` - Signifikanzniveau
- `test` - Testart: `zweiseitig`, `einseitig_links`, `einseitig_rechts` (oder `links`, `rechts`)
- `z` - Z-Teststatistik (optional)
- `t` - t-Teststatistik (optional)
- `p` - p-Wert (optional)

**Hinweise:**
- **Testauswahl:** Das Programm erkennt automatisch, welcher Test verwendet werden soll
- Wenn `shoch2` angegeben wird, wird es automatisch in `s` umgerechnet
- Für t-Test werden Freiheitsgrade (df = n-1) automatisch berechnet

---

## konfidenzintervall.py

Berechnet Konfidenzintervalle für den Mittelwert μ und für die Varianz σ². **Das Programm wählt automatisch die passende Formel** basierend auf den eingegebenen Parametern.

**Formeln:**
- **Z-Test** (μ bei bekannter σ): `x̄ ± z_{1-α/2} · σ/√n`
- **t-Test** (μ bei unbekannter σ): `x̄ ± t_{n-1; 1-α/2} · s/√n`
- **Chi²-Test** (σ²): `[(n-1)·s²/χ²_{α/2}(n-1) ; (n-1)·s²/χ²_{1-α/2}(n-1)]`

**Automatische Formelauswahl:**
- Wenn `x_bar` gegeben ist:
  - `sigma` gegeben → **Z-Test** für Mittelwert
  - `s` oder `shoch2` gegeben → **t-Test** für Mittelwert
- Wenn `x_bar` NICHT gegeben, aber `s` oder `shoch2` gegeben → **Chi²-Test** für Varianz
- Oder explizit: `fuer_varianz=true` → **Chi²-Test** für Varianz

**Verwendung:**
```bash
# Konfidenzintervall für Mittelwert
python konfidenzintervall.py x_bar=<wert> n=<wert> alpha=<wert> seite=<art> [sigma=<wert>] [s=<wert>] [shoch2=<wert>]

# Konfidenzintervall für Varianz
python konfidenzintervall.py n=<wert> alpha=<wert> seite=<art> s=<wert> [fuer_varianz=true]
```

**Beispiele:**
```bash
# t-Test für Mittelwert mit Varianz (wird automatisch in s umgerechnet)
python konfidenzintervall.py x_bar=9 n=31 alpha=0.05 seite=zweiseitig shoch2=31/4

# t-Test für Mittelwert mit Standardabweichung
python konfidenzintervall.py x_bar=9 n=31 alpha=0.05 seite=zweiseitig s=2.78

# Z-Test für Mittelwert (sigma bekannt)
python konfidenzintervall.py x_bar=100 n=25 alpha=0.05 seite=zweiseitig sigma=15

# Chi²-Test für Varianz
python konfidenzintervall.py n=31 alpha=0.05 seite=zweiseitig s=2.78 fuer_varianz=true

# Einseitiges Intervall
python konfidenzintervall.py x_bar=9 n=31 alpha=0.05 seite=einseitig_rechts shoch2=31/4
```

**Parameter:**
- `x_bar` - Stichprobenmittelwert (x̄) - für Konfidenzintervall des Mittelwerts
- `n` - Stichprobenumfang
- `alpha` - Irrtumswahrscheinlichkeit
- `seite` - Intervallart: `zweiseitig`, `einseitig_links`, `einseitig_rechts` (oder `links`, `rechts`)
- `sigma` - Populationsstandardabweichung (σ) - verwendet **Z-Test** für Mittelwert
- `s` - Stichprobenstandardabweichung - verwendet **t-Test** für Mittelwert oder **Chi²-Test** für Varianz
- `shoch2` - Varianz (wird automatisch in s umgerechnet: `s = sqrt(shoch2)`)
- `fuer_varianz` - Wenn `true`, wird Konfidenzintervall für Varianz berechnet

**Hinweise:**
- **Formelauswahl:** Das Programm erkennt automatisch, welche Formel verwendet werden soll:
  - `x_bar` + `sigma` → Z-Test für Mittelwert
  - `x_bar` + `s`/`shoch2` → t-Test für Mittelwert
  - Kein `x_bar`, aber `s`/`shoch2` → Chi²-Test für Varianz
- Wenn `shoch2` angegeben wird, wird es automatisch in `s` umgerechnet
- Das Programm berechnet automatisch z/t/χ²-Werte, Wahrscheinlichkeiten und die Konfidenzintervalle
- **Konfidenzniveau** = (1 - alpha) × 100%
- Für Varianz-Konfidenzintervall wird auch das Intervall für die Standardabweichung σ ausgegeben

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

## trennschaerfe.py

Berechnet die Trennschärfe (Power) eines Hypothesentests. Die Power ist die Wahrscheinlichkeit, H0 abzulehnen, wenn H1 wahr ist. **Das Programm wählt automatisch zwischen Einstichproben- und Zweistichproben-Tests** basierend auf den eingegebenen Parametern.

**Formeln:**
- **Einstichproben-Z-Test** (σ bekannt): Power = 1 - Beta
- **Einstichproben-t-Test** (nur s bekannt): Power = 1 - Beta (mit t-Verteilung)
- **Zweistichproben-t-Test** (unverbundene Stichproben): Power = 1 - Beta (mit gepoolter Varianz)

**Automatische Testauswahl:**
- Wenn `n1`, `n2`, `s1`, `s2`, `mu1`, `mu2` gegeben sind → **Zweistichproben-t-Test**
- Sonst:
  - `sigma` gegeben → **Einstichproben-Z-Test**
  - `s` oder `shoch2` gegeben → **Einstichproben-t-Test**

**Verwendung:**
```bash
# Einstichproben-Test
python trennschaerfe.py mu0=<wert> mu1=<wert> n=<wert> alpha=<wert> test=<art> [sigma=<wert>] [s=<wert>] [shoch2=<wert>] [power=<wert>]

# Zweistichproben-t-Test
python trennschaerfe.py mu1=<wert> mu2=<wert> n1=<wert> n2=<wert> s1=<wert> s2=<wert> alpha=<wert> test=<art>
```

**Beispiele:**
```bash
# Power berechnen (Einstichproben-Z-Test)
python trennschaerfe.py mu0=100 mu1=105 sigma=15 n=25 alpha=0.05 test=zweiseitig

# Power berechnen (Einstichproben-t-Test)
python trennschaerfe.py mu0=100 mu1=105 s=15 n=25 alpha=0.05 test=zweiseitig

# Power berechnen (Zweistichproben-t-Test)
python trennschaerfe.py mu1=26 mu2=28 n1=10 n2=10 s1=4 s2=3 alpha=0.05 test=einseitig_links

# Benötigtes n für gewünschte Power berechnen (Einstichproben)
python trennschaerfe.py mu0=100 mu1=105 sigma=15 alpha=0.05 power=0.8 test=zweiseitig n=-

# mu1 für gewünschte Power berechnen (Einstichproben)
python trennschaerfe.py mu0=100 sigma=15 n=25 alpha=0.05 power=0.8 test=zweiseitig mu1=-
```

**Parameter (Einstichproben-Test):**
- `mu0` - Wert unter H0
- `mu1` - Wert unter H1
- `n` - Stichprobenumfang
- `alpha` - Signifikanzniveau
- `test` - Testart: `zweiseitig`, `einseitig_links`, `einseitig_rechts` (oder `links`, `rechts`)
- `sigma` - Populationsstandardabweichung (σ) - verwendet **Z-Test**
- `s` - Stichprobenstandardabweichung - verwendet **t-Test**
- `shoch2` - Varianz (wird automatisch in s umgerechnet: `s = sqrt(shoch2)`) - verwendet **t-Test**
- `power` - Gewünschte Trennschärfe (wenn n oder mu1 berechnet werden soll)

**Parameter (Zweistichproben-t-Test):**
- `mu1` - Mittelwert Gruppe 1
- `mu2` - Mittelwert Gruppe 2
- `n1` - Stichprobenumfang Gruppe 1
- `n2` - Stichprobenumfang Gruppe 2
- `s1` - Standardabweichung Gruppe 1
- `s2` - Standardabweichung Gruppe 2
- `alpha` - Signifikanzniveau
- `test` - Testart: `zweiseitig`, `einseitig_links`, `einseitig_rechts` (oder `links`, `rechts`)

**Hinweise:**
- **Testauswahl:** Das Programm erkennt automatisch, welcher Test verwendet werden soll
- Wenn `shoch2` angegeben wird, wird es automatisch in `s` umgerechnet
- Für Zweistichproben-t-Test wird gepoolte Varianz verwendet: `s_pooled² = ((n1-1)·s1² + (n2-1)·s2²) / (n1+n2-2)`
- **Power-Interpretation:**
  - Power < 0.5: niedrig (geringe Trennschärfe)
  - 0.5 ≤ Power < 0.8: moderat
  - Power ≥ 0.8: ausreichend (empfohlen)
- Beta (Fehler 2. Art) = 1 - Power

---

## Konfidenzintervall vs. k-Sigma-Regel

**Unterschied:**

- **Konfidenzintervall** (`konfidenzintervall.py`):
  - Berechnet ein Intervall für den **Mittelwert** (Parameter)
  - Formel: `[x̄ ± z·σ/√n]`
  - Beispiel: "Mit 95% Wahrscheinlichkeit liegt der wahre Mittelwert im Intervall [9.98, 10.02]"
  - **Verwendung:** Parameter-Schätzung

- **k-Sigma-Regel** (`k_sigma.py`):
  - Berechnet ein Intervall für eine **einzelne Beobachtung**
  - Formel: `[μ - k·σ; μ + k·σ]`
  - Beispiel: "Mit 95% Wahrscheinlichkeit liegt eine einzelne Beobachtung im Intervall [9.967, 10.033]"
  - **Verwendung:** Einzelwerte vorhersagen
  - **Programm:** `k_sigma.py` (kann z-Wert oder Konfidenzniveau als Eingabe verwenden)

**Zusammenfassung:**
- Konfidenzintervall: Intervall für den **Mittelwert** bei gegebenem Konfidenzniveau
- k-Sigma-Regel: Intervall für eine **Beobachtung** bei gegebener Wahrscheinlichkeit

---

## k_sigma.py

Berechnet das k-Sigma-Intervall (Vorhersageintervall) für eine einzelne Beobachtung. Das Intervall gibt an, in welchem Bereich eine einzelne Beobachtung mit gegebener Wahrscheinlichkeit liegt.

**Formel:** `[μ - k·σ; μ + k·σ]` wobei k der z-Wert für die gewünschte Wahrscheinlichkeit ist.

**Verwendung:**
```bash
python k_sigma.py mu=<wert> sigma=<wert> [z=<wert>] [conf=<wert>]
```

**Beispiele:**
```bash
# Mit z-Wert
python k_sigma.py mu=10 sigma=0.0167 z=1.96

# Mit Konfidenzniveau (95%)
python k_sigma.py mu=10 sigma=0.0167 conf=0.95

# Mit Konfidenzniveau als Prozent
python k_sigma.py mu=10 sigma=0.0167 conf=95
```

**Parameter:**
- `mu` - Mittelwert (μ)
- `sigma` - Standardabweichung (σ)
- `z` - z-Wert (z.B. 1.96 für 95%) - **entweder z oder conf muss angegeben werden**
- `conf` - Konfidenzniveau (z.B. 0.95 oder 95 für 95%) - **entweder z oder conf muss angegeben werden**

**Hinweise:**
- Das Programm berechnet automatisch den z-Wert aus dem Konfidenzniveau, wenn `conf` angegeben wird
- `conf` kann als Dezimalzahl (0.95) oder als Prozent (95) angegeben werden
- Wenn sowohl `z` als auch `conf` angegeben werden, wird `z` verwendet
- **Unterschied zu Konfidenzintervall:** k-Sigma-Regel gibt Intervall für einzelne Beobachtungen, Konfidenzintervall gibt Intervall für den Mittelwert

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
