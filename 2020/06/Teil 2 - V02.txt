import sys
import functools

# ganze Datei lesen
with open('input.txt', 'rt') as f: t=f.read()
# Daten am Ende mit Leerzeile abschließen (steht in Input nur zwischen Gruppen
t+='\n'
# Gruppen von Zeilen bilden. Leere Zeilen sind die Trennung zwischen Daten im Imput.
groups=t.split('\n\n')

# Für jede Gruppe: Gesamttext durch Zeilenliste ersetzen (Zeilen im Imput durch \n getrennt)
groups=map( lambda g: g.split('\n'), groups )
# oder: groups = (group.split('\n') for group in groups)

sum_group_answers = sum(
    # Jede Gruppe durch die Antwortzahl ersetzen
    [ # Anzahl der Antworten der Gruppe
        len(
        # Die Zeilen der Gruppe durch intersection reduzieren
        functools.reduce(
            lambda a, b: a.intersection(b),
            # In jeder Gruppe die Zeile durch ein Set von Zeichen ersetzen
            map(lambda l: set(l), group)
            # Oder: [ set(l) for l in group]
            )
        )
      for group in groups ]
    )

print(sum_group_answers)
#3360
