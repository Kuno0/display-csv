# Code zum Erstellen von Verlaufsdiagrammen aus Excel-Dateien mit mehreren Y-Achsen
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import os
from pathlib import Path

# ============================================================================
# KONFIGURATIONSBEREICH - Hier können Farben und Achsenbereiche angepasst werden
# ============================================================================

# Farben für die Datenreihen (Hex-Farben oder benannte Farben)
COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']

# Y-Achsen-Bereiche für einzelne Spalten
# Format: {'Spaltenname': (min, max)} oder None für automatische Bestimmung
# Beispiele:
#   'pH': (6.5, 8.5)           -> pH zwischen 6.5 und 8.5
#   'µS/cm': (None, 5000)      -> µS/cm Maximum 5000, Minimum automatisch
#   '°C': None                 -> Bereich automatisch bestimmen
Y_AXIS_RANGES = {
    'pH': (0, 14),
    'µS/cm': (5000, 10000),
    'FNU': (0, 200),
    '°C': (0, 100),
}

# Diagramm-Größe (Breite, Höhe) in Zoll
FIGURE_SIZE = (14, 7)

# Diagramm-Titel (kann leer bleiben "")
CHART_TITLE = ""

# Gitter anzeigen? True oder False
SHOW_GRID = True

# Legende anzeigen? True oder False
SHOW_LEGEND = True

# DPI für die Auflösung der gespeicherten Bilder
DPI = 300

# Zeitformat für die X-Achse (Timestamp)
# Beispiele: '%d.%m %H:%M', '%Y-%m-%d %H:%M:%S', '%d.%m.%Y %H:%M'
TIMESTAMP_FORMAT = '%d.%m %H:%M'

def create_line_chart(excel_file, output_dir='graphs'):
    """
    Erstellt ein Multi-Achsen-Verlaufsdiagramm aus einer Excel-Datei.
    
    Die ersten zwei Spalten werden als Datum und Uhrzeit interpretiert und
    zu einem Timestamp kombiniert (X-Achse).
    Jede weitere numerische Spalte erhält eine eigene Y-Achse.
    
    Falls keine Spaltennamen vorhanden sind, werden die Spalten automatisch
    in dieser Reihenfolge benannt: pH, µS/cm, FNU, °C
    
    Parameters:
    -----------
    excel_file : str
        Pfad zur Excel-Datei
    output_dir : str
        Verzeichnis, in dem die Grafik gespeichert wird
    """
    try:
        # Excel-Datei einlesen (erstes Blatt)
        df = pd.read_excel(excel_file, sheet_name=0)
        
        if df.shape[1] < 3:
            print(f'✗ Zu wenige Spalten in {excel_file}. Benötigt: Datum, Uhrzeit, mindestens 1 Datenspalte.')
            return
        
        # Dateiname ohne Pfad und Endung für die Ausgabedatei
        base_filename = Path(excel_file).stem
        output_file = os.path.join(output_dir, f'{base_filename}.png')
        
        # Erste zwei Spalten (Datum und Uhrzeit) zu Timestamp kombinieren
        date_col = df.iloc[:, 0]
        time_col = df.iloc[:, 1]
        
        # Timestamp erstellen
        try:
            timestamp = pd.to_datetime(date_col.astype(str) + ' ' + time_col.astype(str))
        except Exception as e:
            print(f'✗ Fehler beim Kombinieren von Datum und Uhrzeit in {excel_file}: {str(e)}')
            return
        
        # Datenreihen (ab Spalte 3)
        data_columns = df.iloc[:, 2:]
        
        # Nur numerische Spalten behalten
        numeric_data = data_columns.select_dtypes(include=['number'])
        
        if numeric_data.empty:
            print(f'✗ Keine numerischen Daten in {excel_file} gefunden.')
            return
        
        # Standard-Spaltennamen für die erwartete Reihenfolge
        standard_names = ['pH', 'µS/cm', 'FNU', '°C']
        
        # Spaltennamen überprüfen und ggf. umbenennen
        columns_to_use = []
        for idx, col_name in enumerate(numeric_data.columns):
            # Überprüfe, ob der Spaltenname "Unnamed" ist oder ähnlich
            if str(col_name).startswith('Unnamed') or col_name not in Y_AXIS_RANGES:
                # Nutze Standard-Namen, falls verfügbar
                if idx < len(standard_names):
                    columns_to_use.append(standard_names[idx])
                else:
                    columns_to_use.append(col_name)
            else:
                columns_to_use.append(col_name)
        
        # DataFrame mit neuen Spaltennamen erstellen
        numeric_data.columns = columns_to_use
        
        # Diagramm mit mehreren Y-Achsen erstellen
        fig, ax1 = plt.subplots(figsize=FIGURE_SIZE)
        
        axes = [ax1]  # Erste Achse
        lines = []    # Zur Sammlung aller Linien für die Legende
        
        # Für jede numerische Spalte eine Linie zeichnen
        for idx, (col_name, col_data) in enumerate(numeric_data.items()):
            color = COLORS[idx % len(COLORS)]
            
            if idx == 0:
                # Erste Datenreihe auf der linken Achse
                ax = ax1
                ax.set_xlabel('Zeit', fontsize=12)
                ax.set_ylabel(col_name, fontsize=11, color=color)
                ax.tick_params(axis='y', labelcolor=color)
            else:
                # Zusätzliche Achsen rechts hinzufügen
                ax = ax1.twinx()
                
                # Achse nach rechts verschieben (offset)
                ax.spines['right'].set_position(('outward', 60 * (idx - 1)))
                ax.set_ylabel(col_name, fontsize=11, color=color)
                ax.tick_params(axis='y', labelcolor=color)
                
                axes.append(ax)
            
            # Linie zeichnen
            line, = ax.plot(timestamp, col_data, label=col_name, color=color, 
                           linewidth=2, marker='o', markersize=3)
            lines.append(line)
            
            # Y-Achsen-Bereich setzen
            y_min, y_max = col_data.min(), col_data.max()
            
            # Aus Konfiguration übernehmen, falls vorhanden
            if col_name in Y_AXIS_RANGES and Y_AXIS_RANGES[col_name] is not None:
                config_min, config_max = Y_AXIS_RANGES[col_name]
                if config_min is not None:
                    y_min = config_min
                if config_max is not None:
                    y_max = config_max
            
            # Leichter Puffer für bessere Sichtbarkeit
            puffer = (y_max - y_min) * 0.05 if y_max != y_min else 0.1
            ax.set_ylim(y_min - puffer, y_max + puffer)
        
        # Gitter (nur auf der Hauptachse)
        if SHOW_GRID:
            ax1.grid(True, alpha=0.3, linestyle='--')
        
        # Titel
        if CHART_TITLE:
            ax1.set_title(CHART_TITLE, fontsize=14, fontweight='bold')
        else:
            ax1.set_title(base_filename, fontsize=14, fontweight='bold')
        
        # Legende kombinieren von allen Achsen
        if SHOW_LEGEND:
            ax1.legend(lines, [l.get_label() for l in lines], loc='upper left', fontsize=10)
        
        # X-Achsen-Zeitformat konfigurieren
        date_formatter = mdates.DateFormatter(TIMESTAMP_FORMAT)
        ax1.xaxis.set_major_formatter(date_formatter)
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Layout anpassen
        plt.tight_layout()
        
        # Datei speichern
        plt.savefig(output_file, dpi=DPI, bbox_inches='tight')
        plt.close(fig)
        
        print(f'Grafik erstellt: {output_file}')
        
    except Exception as e:
        print(f'✗ Fehler bei {excel_file}: {str(e)}')


def main():
    """
    Durchläuft alle Excel-Dateien im data-Ordner und erstellt Grafiken.
    """
    data_dir = 'data'
    output_dir = 'graphs'
    
    # Ausgabeverzeichnis erstellen, falls nicht vorhanden
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Alle Excel-Dateien im data-Ordner finden
    excel_files = []
    for file in os.listdir(data_dir):
        if file.endswith('.xlsx') or file.endswith('.xls'):
            excel_files.append(os.path.join(data_dir, file))
    
    if not excel_files:
        print(f"Keine Excel-Dateien im Ordner '{data_dir}' gefunden.")
        return
    
    print(f"Es wurden {len(excel_files)} Excel-Dateien gefunden.\n")
    
    # Für jede Excel-Datei ein Diagramm erstellen
    for excel_file in excel_files:
        print(f"Verarbeite: {excel_file}")
        create_line_chart(excel_file, output_dir)
    
    print(f"\nFertig! Alle Grafiken wurden im Ordner '{output_dir}' gespeichert.")


if __name__ == '__main__':
    main()
