# Code um Graphen mit mehreren Achsen zu erstllen
import matplotlib as plt
import numpy as np
import pandas as pd

df_sourcedata = pd.read_excel('data\W4007C04428 2159677804 0000000019 2025-12-22 00-00-00 GROUP01.xlsx', sheet_name=0, header=0)
# Erstellen Sie eine neue Figur und Achse
fig, ax1 = plt.subplots()
# Plotten Sie die erste Datenreihe auf der ersten Achse
ax1.plot(df_sourcedata['Zeitstempel'], df_sourcedata['Druck'], color='blue', label='Druck')
ax1.set_xlabel('Zeitstempel')
ax1.set_ylabel('Druck', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
# Erstellen Sie eine zweite Achse, die die erste Achse teilt
ax2 = ax1.twinx()
# Plotten Sie die zweite Datenreihe auf der zweiten Achse
ax2.plot(df_sourcedata['Zeitstempel'], df_sourcedata['Temperatur'], color='red', label='Temperatur')
ax2.set_ylabel('Temperatur', color='red')
ax2.tick_params(axis='y', labelcolor='red')
# Fügen Sie eine Legende hinzu
fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
# Zeigen Sie den Graphen an
plt.title('Druck und Temperatur über Zeit')
plt.show()
