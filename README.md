# display-csv

Ein Python-Skript zur automatischen Generierung von Verlaufsdiagrammen aus Excel-Dateien mit mehreren Y-Achsen.

## Installation

Installieren Sie zunächst die erforderliche Bibliothek:

```bash
python -m pip install openpyxl
```

Weitere benötigte Bibliotheken (matplotlib, pandas) sind normalerweise bereits installiert.

## Beschreibung

Das Skript `graph.py` durchläuft automatisch alle Excel-Dateien im Ordner `data/` und erstellt für jede Datei ein Verlaufsdiagramm im Ordner `graphs/`.

### Funktionsweise

1. **Datenstruktur**: Die Excel-Dateien müssen folgende Struktur haben:
   - **Spalte 1**: Datum (z.B. 2025-12-22)
   - **Spalte 2**: Uhrzeit (z.B. 14:30:00)
   - **Spalte 3+**: Numerische Daten (pH, µS/cm, FNU, °C)

2. **Timestamp-Kombination**: Die ersten zwei Spalten werden zu einem Timestamp kombiniert und bilden die X-Achse

3. **Multiple Y-Achsen**: Jede Datenreihe erhält eine eigene Y-Achse mit individueller Skalierung
   - Erste Spalte: Linke Achse
   - Weitere Spalten: Rechts positioniert

4. **Automatische Benennung**: Falls die Spaltennamen fehlen oder "Unnamed" sind, werden diese Standard-Namen verwendet:
   - pH, µS/cm, FNU, °C

## Konfiguration

Alle Einstellungen befinden sich im **KONFIGURATIONSBEREICH** am Anfang der Datei `graph.py`:

### Farben anpassen

```python
COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']
```
**Funktion**: Definiert die Farben für die Datenreihen (in Hex-Format oder benannte Farben wie 'red', 'blue')

**Beispiele**:
- `'#1f77b4'` → Blau
- `'red'` → Rot
- `'#00FF00'` → Grün

### Y-Achsen-Bereiche festlegen

```python
Y_AXIS_RANGES = {
    'pH': (0, 14),          # von 0 bis 14
    'µS/cm': None,          # Automatische Bestimmung
    'FNU': None,            # Automatische Bestimmung  
    '°C': None              # Automatische Bestimmung
}
```

**Funktion**: Setzt die Min/Max-Werte für jede Datenreihe. `None` bedeutet automatische Bestimmung.

**Beispiele**:
```python
'pH': (0, 14)              # Fester Bereich
'µS/cm': (None, 5000)      # Nur Maximum vorgegeben
'FNU': (0, None)           # Nur Minimum vorgegeben
'°C': None                 # Automatisch (min und max aus Daten)
```

### Diagramm-Größe

```python
FIGURE_SIZE = (14, 7)
```

**Funktion**: Größe des Diagramms in Zoll (Breite, Höhe)

**Beispiele**:
- `(12, 6)` → Schmaleres Diagramm
- `(16, 8)` → Breiteres Diagramm

### Diagramm-Titel

```python
CHART_TITLE = ""
```

**Funktion**: Titel des Diagramms. Bei leerem String wird der Dateiname verwendet.

**Beispiele**:
```python
CHART_TITLE = "Messwerte Gruppe 01"  # Benutzerdefinierter Titel
CHART_TITLE = ""                      # Dateiname wird als Titel verwendet
```

### Gitter anzeigen

```python
SHOW_GRID = True
```

**Funktion**: Zeigt das Hintergrund-Gitter an (`True` oder `False`)

### Legende anzeigen

```python
SHOW_LEGEND = True
```

**Funktion**: Zeigt die Legende mit den Spaltennamen an (`True` oder `False`)

### Auflösung

```python
DPI = 300
```

**Funktion**: Auflösung der gespeicherten PNG-Dateien (dots per inch)

**Beispiele**:
- `150` → Niedrigere Auflösung, kleinere Dateigröße
- `300` → Standard (wird empfohlen)
- `600` → Hohe Auflösung, größere Dateigröße

### Zeitstempel-Format

```python
TIMESTAMP_FORMAT = '%d.%m %H:%M'
```

**Funktion**: Format der Zeitanzeige auf der X-Achse

**Beispiele**:
```python
'%d.%m %H:%M'        # 22.12 14:30
'%d.%m'              # 22.12
'%H:%M'              # 14:30
'%Y-%m-%d %H:%M'     # 2025-12-22 14:30
'%d.%m.%Y %H:%M:%S'  # 22.12.2025 14:30:45
```

strftime-Formate:
- `%d` = Tag (01-31)
- `%m` = Monat (01-12)
- `%Y` = Jahr (4-stellig)
- `%H` = Stunde (00-23)
- `%M` = Minute (00-59)
- `%S` = Sekunde (00-59)

## Verwendung

1. Legen Sie Excel-Dateien im Ordner `data/` ab
2. Passen Sie bei Bedarf die Variablen in `graph.py` an
3. Führen Sie das Skript aus:

```bash
python graph.py
```

4. Die generierten Grafiken erscheinen im Ordner `graphs/`

## Spalten

Datenformat (erste zwei Spalten sind Datum/Uhrzeit, weitere sind Datenreihen):

* date
* time
* pH
* µS/cm
* FNU
* °C