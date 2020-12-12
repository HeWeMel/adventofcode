import sys
import re

with open('input.txt') as f:
    lines = f.readlines()  # ganze Datei lesen

pat_rule = re.compile(r"(.+) bags contain (.+)[.]")
pat_split = re.compile(r", |[.]")
pat_tobags = re.compile(r"(\d+) (.+)+ bag(?:s?)")

rules = dict()
outer = dict()
for line in lines:
    # line und rechts von "bags contain" finden
    m = pat_rule.match(line)
    (f, to_text) = m.groups()
    if f in rules:
        raise AssertionError('Outer bag tritt zweites Mal auf:' + line)
    # enthaltene Bags aufsammeln
    t = []
    if to_text != 'no other bags':
        # bag-Liste in Elemente zerlegen
        tos = pat_split.split(to_text)
        if len(tos) == 0:
            raise AssertionError('no tos in line:' + line)
        for bag in tos:
            # Pro Element die Anzahl und den Bag-Name extrahieren
            m = pat_tobags.match(bag)
            (n, b) = m.groups()
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
print(len(rules), 'Regeln')

cache=dict()
def count_bags(bag):
    if bag in cache:
        return(cache[bag])
    else:
        count= 1 + sum( n*count_bags(b) for (n, b ) in rules[bag])
        cache[bag] = count
        return(count)

print( 'Anzahl enthaltener Bags: ', count_bags('shiny gold')-1 )
#10875