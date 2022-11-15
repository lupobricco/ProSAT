from statsmodels.stats.inter_rater import fleiss_kappa
#riferimento bibliografico: Fleiss, Joseph L. 1971. “Measuring Nominal Scale Agreement among Many Raters.” Psychological Bulletin 76 (5): 378-82. https://doi.org/10.1037/h0031619.
import csv
import numpy as np

thisdict={}
file = open('TWITA_1/TWITA-annotation.csv','r')
reader = csv.DictReader(file)

file2 = open('TWITA_2_results/TWITA_2-annotation.csv','r')
reader2 = csv.DictReader(file2)

# for row in reader:
#     if row['uri'] not in thisdict:
#         thisdict[row['uri']] = {'labels': []}
#     thisdict[row['uri']]['labels'].append(row['tag_name'])

for row in reader2:
    if row['uri'] not in thisdict:
        thisdict[row['uri']] = {'labels': []}
    thisdict[row['uri']]['labels'].append(row['tag_name'])

table=[]
for key_tweet_id, value in thisdict.items():
    labels=[0,0]
    for label in value['labels']:
        if label == "Neutro":
            labels[0]+=1

    labels = [labels[0], 3-labels[0]]
    print(value['labels'],labels)
    table.append(labels)


print(fleiss_kappa(table))
"""
< 0 	Poor agreement
0.01 – 0.20 	Slight agreement
0.21 – 0.40 	Fair agreement
0.41 – 0.60 	Moderate agreement
0.61 – 0.80 	Substantial agreement
0.81 – 1.00 	Almost perfect agreement
"""
