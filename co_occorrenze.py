import pandas
from collections import Counter

Instagram_annotation = pandas.read_csv("gold_standard_text.csv")

array_uris = []

labels = ["Amore", "Anticipazione", "Disgusto", "Fiducia", "Gioia", "Paura", "Rabbia", "Sorpresa", "Tristezza", "Neutro", "Ironia", "Sarcasmo", "Offensivita"]

for row in Instagram_annotation.itertuples():
    if getattr(row, 'tag_name') == "Sarcasmo":
        array_uris.append(getattr(row, 'uri'))

frequency = Counter(array_uris)
for label in labels:
    counter = 0
    for row in Instagram_annotation.itertuples():
        if getattr(row, 'tag_name') == label and frequency[getattr(row, 'uri')] > 0:
            counter += 1
    print(label + " " +str(counter))