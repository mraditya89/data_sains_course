import csv
import json
import math
import time
from datetime import datetime, timedelta

import tweepy

offset = time.timezone/3600

def getUtcDateTime(localTime):
    localTime += timedelta(hours=offset)
    return localTime

def getLocalDatetime(utcTime):
    utcTime -= timedelta(hours=offset)
    return utcTime

class TwitterAPI:
    delay = (60*15)+5
    def __init__(self, tokenFile):
        self.readToken(tokenFile)
        self.createConnection()

    def readToken(self, tokenFile):
        with open(tokenFile) as f:
            self.token = json.load(f)

    def createConnection(self):
        self.client = tweepy.Client(
            bearer_token = self.token["bearer_token"], 
            wait_on_rate_limit=True
            )

    def getTweet(self, query, dateTime):
        responses = tweepy.Paginator(
            self.client.search_recent_tweets, 
            query=query,
            tweet_fields=['text', 'created_at', 'author_id', 'public_metrics'], 
            max_results=100, 
            end_time = dateTime, 
        ).flatten(limit=600)
        return responses
    
    def log(self, text):
        print(f"[script] {datetime.now()} : {text}")
        
    def crawl(self, query, dateTime, numberOfDays=1):
        mode="w"
        for i in range(numberOfDays):
            tweetData = []
            if (i!=0):
                mode="a"
                delayText =  f"{TwitterAPI.delay} seconds"
                if TwitterAPI.delay > 60:
                    minutes = math.floor(TwitterAPI.delay / 60)
                    secods = TwitterAPI.delay % 60
                    delayText =  f"{minutes} minutes {secods} seconds"
                self.log(f"wait for {delayText}")
                time.sleep(TwitterAPI.delay)

            self.log(f"request tweet before {getLocalDatetime(dateTime)}")
            
            responses = self.getTweet(query, dateTime)
            for (idx, response) in  enumerate(responses):
                # print(f'[{idx+1}] : {response.author_id}')
                # print(response.created_at, response.text)
                # print("-"*80)
                tweetData.append([
                    response.created_at,
                    response.author_id,
                    response.text,
                    response.public_metrics["retweet_count"],
                    response.public_metrics["reply_count"],
                    response.public_metrics["like_count"],
                    response.public_metrics["reply_count"],
                    response.public_metrics["quote_count"]
                ])
            dateTime += timedelta(days=1)
            self.writeToCsv(tweetData, mode=mode)
        
        self.log("done")

    def writeToCsv(self, data, mode="w"):
        self.log("write to file") if (mode=="w") else self.log("append to file")
        with open('./tweet_data.csv', mode, encoding='UTF8', newline="") as f:
            writer = csv.writer(f)
            if (mode=="w"):
                header = ["created_at", "author_id", "tweet", "retweet_count", "reply_count", "like_count", "reply_count","quote_count"]
                writer.writerow(header)
            writer.writerows(data)


# create twitterAPI object
tweet = TwitterAPI("./token.json")

# query parameter setup
query = 'ppkm - is:retweet lang:id'
localTime = datetime(2021, 12, 3, 23, 59, 59)
dateTime = getUtcDateTime(localTime)
numberOfDays = 4

# crawl data
tweet.crawl(query, dateTime, numberOfDays)
