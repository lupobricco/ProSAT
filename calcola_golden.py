import csv

thisdict = {}


# file = open('TWITA_1/TWITA-annotation.csv', 'r')
# reader = csv.DictReader(file)

# file2 = open('TWITA_2_results/TWITA_2-annotation.csv','r')
# reader = csv.DictReader(file2)

file = open('TWITA_2_results/TWITA_2_multi-annotation.csv', 'r')
reader = csv.DictReader(file)

fileW = open('gold_standard_Multi.csv', "w", newline='', encoding='utf-8')
writer = csv.writer(fileW)

writer.writerow(['uri', 'tag_name'])

for row in reader:
    if row['uri'] not in thisdict:
        thisdict[row['uri']] = {'labels': []}
    thisdict[row['uri']]['labels'].append(row['tag_name'])

# for row in reader2:
#     if row['uri'] not in thisdict:
#         thisdict[row['uri']] = {'labels': []}
#     thisdict[row['uri']]['labels'].append(row['tag_name'])

for key_tweet_id, value in thisdict.items():
    labelDict= {}
    for label in value['labels']:
        if label not in labelDict:
            labelDict[label] = {'count': 1}
        else:
            labelDict[label]['count'] += 1

    print(value['labels'], labelDict)

    for key_label_name, summ in labelDict.items():
        if summ['count'] > 1:
            toWrite = [key_tweet_id, key_label_name]
            writer.writerow(toWrite)
