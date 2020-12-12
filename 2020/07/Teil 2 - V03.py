import sys
import re

with open('input.txt') as f:
    lines = f.readlines()  # ganze Datei lesen

rules = dict()
outer = dict()
for line in lines:
    # line und rechts von "bags contain" finden
    (f, to_text) = re.match(r"(.+) bags contain (.+)[.]", line).groups()
    if f in rules:
        raise AssertionError('Outer bag tritt zweites Mal auf:' + line)
    # enthaltene Bags aufsammeln
    t = []
    if to_text != 'no other bags':
        # bag-Liste in Elemente zerlegen
        tos = re.split(r", |[.]", to_text)
        if len(tos) == 0:
            raise AssertionError('no tos in line:' + line)
        for bag in tos:
            # Pro Element die Anzahl und den Bag-Name extrahieren
            (n, b) = re.match(r"(\d+) (.+)+ bag(?:s?)", bag).groups()
            n=int(n)
            if n == 0:
                raise AssertionError('empty to:' + line)
            # Paare von Anzahl und Bag sammeln
            t.append((n, b))
            # Für jedes enthaltene Bag ablegen, in welchem anderen es enthalten ist
            if not (b in outer):
                outer[b] = []
            outer[b].append(f)
    # Zum Bag den Inhalt merken
    rules[f] = t
    # print (f">> '{f}' -> {t}")
print('Anzahl Regeln:', len(rules))

# ------------Teil 1 lösen ------------ 332

todos = ['shiny gold']
r = []
while len(todos) != 0:
    new_todos = []
    for o in todos:
        if o in r: continue
        # für jedes erstmalig betrachtete Bag: in die Lösung aufnehmen,
        r.append(o)
        # und eventuelle darum herum packbare Bags in die nächste
        # Runde der Betrachtung aufnehmen
        if o in outer:
            new_todos.extend(outer[o])
    todos = new_todos
print('Anzahl Farben:', len(r)-1)

# ------------ Teil 2 lösen ------------ 10875

cache=dict()
def count_bags(bag):
    # Bag-Anzahl aus Cache bedienen, wenn bereits ermittelt
    if bag in cache:
        return(cache[bag])
    else:
        # Bag-Anzahl ist der aktuelle Bag plus das jeweils richtige
        # Mehrfache der enthaltenen Bags
        count= 1 + sum( n*count_bags(b) for (n, b ) in rules[bag])
        cache[bag] = count
        return(count)
print( 'Anzahl enthaltener Bags:', count_bags('shiny gold')-1 )
