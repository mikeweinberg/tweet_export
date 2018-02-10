## tweet_export.py
Easy exporting of tweets to a CSV file

#### Requirements:
* A Twitter account with API credentials
* Python 3.6+
* [Tweepy](https://github.com/tweepy/tweepy) 

#### Instructions:
* Install Tweepy:
`pip3 install tweepy`
* Rename `config-sample.yml` to `config.yml` and add your Twitter API credentials. 
* To download the Tweets of "username", run the following command:
`python3 tweet_export.py username`
* Results are subject to Twitter's API limits, which are [3,200](https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline.html) as of this writing.
* **Protect your Twitter API credentials as you would a password.**


####Acknowledgements:
Based on [tweet_dumper.py](https://gist.github.com/yanofsky/5436496) 
