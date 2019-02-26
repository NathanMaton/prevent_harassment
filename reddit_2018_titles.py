import datetime
import json
import requests
import time
from collections import defaultdict
import pickle

from pymongo import MongoClient, InsertOne, DeleteOne, ReplaceOne


# Generates a list of date time needed from START to END
start = datetime.datetime.strptime("01-01-2018", "%d-%m-%Y")
end = datetime.datetime.strptime("01-01-2019", "%d-%m-%Y")
date_generated = [
    start + datetime.timedelta(days=x) for x in range(0, (end - start).days)]

post_dict = defaultdict(list)

client = MongoClient()
db = client["reddit"]

overnight_collection = db.get_collection('reddit_overnight')

sub_reddit_list = ['mademesmile', 'natureisf-----glit','nevertellmetheodds', 'whatcouldgowrong', 'thisblewmymind', 'wholesomegifs', \
        'childrenfallingover', 'childrenfallingover', 'oddlysatisfying', 'aww', 'getmotivated', 'youshouldknow','tinder']

for sub_reddit in sub_reddit_list:
    for i, date, in enumerate(date_generated):
        #print("Working {}".format(date))
        # time.sleep(1)
        if i == len(date_generated) - 1:
            continue

        # Builds link
        start_date = str(int(date_generated[i].timestamp()))
        end_date = str(int(date_generated[i + 1].timestamp()))
        link = 'https://api.pushshift.io/reddit/submission/search/?after=' + start_date + \
            '&before=' + end_date + '&sort_type=score&sort=desc&subreddit=' + sub_reddit

        # Request data from api
        r = requests.get(link)

        # Pulls data from link into json object
        data = json.loads(r.text)
        # Pulls titles from each submission for that days
        for post in data['data']:
            if overnight_collection.find({'id':post['id']}).count() > 0:
                print ('dupe')
            else:
                overnight_collection.insert_one(post)
            #post_dict[date].append(post['title'])
            #print (post['title'])
