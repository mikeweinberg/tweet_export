#!/usr/bin/env python3
# encoding: utf-8
# command to download tweets of user "username": python3 tweet_export.py username 
# requires python 3.6+ and Tweepy (pip install tweepy)
# rename config-sample.yml to config.yml and add your Twitter credentials

#based on tweet_dumper.py https://gist.github.com/yanofsky/5436496
#upgraded to download tweets for arbitrary 

import tweepy #https://github.com/tweepy/tweepy
import csv
import time
import os
import sys
import yaml

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

#load config.yml
config_location = os.path.join(get_script_path(),'config.yml')
with open(config_location, 'r') as ymlfile:
    config = yaml.load(ymlfile)

#Twitter API credentials read from config.yml
consumer_key = config['consumer_key']
consumer_secret = config['consumer_secret']
access_key = config['access_key']
access_secret = config['access_secret']


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200, tweet_mode='extended')
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print ("getting tweets before %s" % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200, tweet_mode='extended', max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print ("...%s tweets downloaded so far" % (len(alltweets)))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.full_text.encode("utf-8")] for tweet in alltweets]
	
	now = time.strftime("%Y-%m-%d-%H-%M-%S%Z")
	#write the csv	
	with open(f'{screen_name}_tweets_{now}.csv', 'w') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)
	
	pass


if __name__ == '__main__':
	if len(sys.argv) == 2:
		get_all_tweets(sys.argv[1])
	else:
		print("Please provide a screen name to download tweets.")
		
