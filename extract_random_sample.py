import csv
import random
import langdetect
import re
import json

def get_jaccard_sim(str1, str2):
    a = set(str1.split())
    b = set(str2.split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))

########################################################
# parameters
sample_size = 3000
similarity_threshold = 0.7  # between 0 and 1
language_threshold = 0.7  # between 0 and 1
max_same_user = 5
min_popularity = 2
########################################################

tweets = {}
sample = []

# read all the tweets from merge.csv
fileIn = open('merge.csv', 'r', encoding="utf-8")
reader = csv.reader(fileIn, delimiter=",", quotechar="\"")
next(reader, None)
for row in reader:
    tweets[row[0]] = row
fileIn.close()

# filter the tweets
print("recoveder ", len(tweets.keys()))
tweets = [*tweets.values()]
random.shuffle(tweets)
for tweet in tweets:
    if len(sample) >= sample_size:
        continue

    # filter by text token lenght
    if len(tweet[3].split(" ")) < 5:
        continue

    # filter by language
    prediction = langdetect.detect(tweet[3].replace("\n", " "))
    if prediction != 'it':
        continue

    # filter if text contains an url
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, tweet[3])
    if len(url) > 0:
        continue

    # filter by similarity
    flag = False
    for sampled_tweet in sample:
        if flag:
            continue
        similarity = get_jaccard_sim(tweet[3], sampled_tweet[3])
        if round(similarity, 1) >= similarity_threshold:
            flag = True
    if flag:
        continue

    #filter by same user id
    same_user = 0
    for sampled_tweet in sample:
        if same_user > max_same_user:
            continue
        if tweet[1] == sampled_tweet[1]:
            same_user+=1
    if same_user > max_same_user:
        continue

    # Filter by popularity:
    # like = 1, reply = 2, retweet = 2, quote = 3
    if tweet[5] != 'NULL':
        json_str = tweet[5].replace("\'", "\"")
        popular_details = json.loads(json_str)
        popularity = (popular_details['retweet_count'] * 2) + (popular_details['reply_count'] * 2) + popular_details['like_count'] + (popular_details['quote_count'] * 3)
        if popularity < min_popularity:
            continue

    sample.append(tweet)

print("final sample of size: ", len(sample))
output = open("images/propaganda_sample.csv", "w", newline='', encoding='utf-8')
output_csv = csv.writer(output)
for tweet in sample:
    sensitag = [tweet[0], tweet[3], 'PropagandaLive (tweet)']
    output_csv.writerow(sensitag)
output.close()