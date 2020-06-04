#code by duck_master; written 31 may 2020 - 2 june 2020 AD; open source
import pathlib      #thx StackOverflow user YaOzl for pathlib
import csv
import random
import markovify
import datetime     #for diary structure

cwd = str(pathlib.Path.cwd())

#tweet cleaner
def cleantweet(tweet):
    '''Removes hashtags, tags and hyperlinks.
    str -> str'''
    splittweet = tweet.split(' ')
    result = []
    for thing in splittweet:
        if not(thing == ''):
            if not (thing[0] == '#' or thing[0] == '@' or thing[:4] == 'http'):
                result.append(thing)
    return ' '.join(result)

#getting content
tweets = []
inf = open(cwd + '/tweets.csv')
csvdreader = csv.DictReader(inf)
for thing in csvdreader:
    if 'duck' in thing['text']:
        tweets.extend([cleantweet(thing['text'])]*1000)
    else:
        if random.randrange(10) == 0:
            tweets.append(cleantweet(thing['text']))
inf.close()
random.shuffle(tweets)
print(f'debug: len(tweets) = {len(tweets)}')

#diary setup
diaryday = datetime.date(2019, 11, 1)
oneday = datetime.timedelta(days = 1)
def englishDate(date):
    '''Returns an English name for the date.
    datetime.date -> str'''
    monthnames = ['Undefined', 'January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
    daysofweek = ['Undefined', 'Monday', 'Tuesday', 'Wednesday',
                  'Thursday',  'Friday', 'Saturday', 'Sunday']
    return f'{daysofweek[date.isoweekday()]}, {date.day} {monthnames[date.month]} {date.year}'

#markov-chaining (plus diary structure)
content = ' '.join(tweets)
textmodel = markovify.Text(content, state_size = 2)
outf = open(cwd + '/nanogenmo19.txt', 'w')
wordcount = 0
outf.write(f'==={englishDate(diaryday)}===\n')
diaryday += oneday
while wordcount < 50000:            #main driver loop
    sentence = textmodel.make_sentence()
    if random.randrange(7) == 0:    #for diary thingy
        outf.write(f'\n=== {englishDate(diaryday)} ===\n\n')
        print(f'day {diaryday} written; wordcount = {wordcount}')
        diaryday += oneday
    if sentence != None:
        if random.randrange(3) == 0:
            outf.write(sentence + '\n')
        else:
            outf.write(sentence + ' ')
        wordcount += len(sentence.split(' '))
print('done')
outf.close()
