#!/usr/bin/env python
# coding: utf-8

# ## Load Twitter API and some useful functions

# In[ ]:


import tweepy 
import csv
import json
import re
import datetime

#load twitter credentials from file 
"""
with open('twitter_credentials.json') as cred_data:
    info = json.load(cred_data)
    consumer_key = info['CONSUMER_KEY']
    consumer_secret = info['CONSUMER_SECRET']
    access_key = info['ACCESS_KEY']
    access_secret = info['ACCESS_SECRET']

#save authentication info 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
"""

#load twitter credentials from file 
consumer_key = 'kAULSmYrpuA7idFEYJmmVJqsZ'
consumer_secret = 'NGyXI8OEKbNkpCfL1jrSLWy2pCSsZPz1nCE3P6qFXzh2Nqsog2'
access_token = '466693964-vVTSjjGghi6K4qnlReqfrUq0uPj4o4Jw8UYVGTNz'
access_token_secret = '7gweeKfNBJzDj4hqy4OmDqufBjcI7pP2KMpb5SWYqUxu0'

# Set up OAuth and integrate with API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# In[ ]:


#function to clean up the text of tweet 
def clean_tweet(tweet): 
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) (\w+:\/\/\S+)", " ", tweet).split())


# In[ ]:


#simpler function to get tweets, doesnt work? 
def get_tweets_simple(query, max_tweets):
    searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]
    tweets = []
    for tweet in searched_tweets:
        # empty dictionary to store required params of a tweet 
        parsed_tweet = {}
        # saving text of tweet 
        parsed_tweet['text'] = clean_tweet(tweet.text)
        tweets.append(parsed_tweet)


# In[ ]:


#more complicated function to download tweets for given query
def get_tweets(query, max_tweets):
    searched_tweets = []
    last_id = -1
    while len(searched_tweets) < max_tweets:
        count = max_tweets - len(searched_tweets)
        try:
            new_tweets = api.search(q = query, count = count, max_id = str(last_id - 1))
            if not new_tweets:
                break
            searched_tweets.extend(new_tweets)
            last_id = new_tweets[-1].id
        except tweepy.TweepError as e:
        # depending on TweepError.code, one may want to retry or wait
        # to keep things simple, we will give up on an error
            break
            
    tweets = []
    for tweet in searched_tweets:
        # empty dictionary to store required params of a tweet 
        parsed_tweet = {}
        # saving text of tweet 
        parsed_tweet['text'] = clean_tweet(tweet.text)
        tweets.append(parsed_tweet)
            
    return tweets


# In[ ]:


#return all tweets from given screenname
def get_tweets_user(screen_name, max_tweets, startDate, endDate):
    searched_tweets = []
    last_id = -1
    while len(searched_tweets) < max_tweets:
        count = max_tweets - len(searched_tweets)
        try:
            #new_tweets = api.user_timeline(id = screenname, count = count, max_id = str(last_id - 1))
            new_tweets = api.user_timeline(screen_name = screen_name, count = max_tweets, include_rts = True)
            if not new_tweets:
                break
            searched_tweets.extend(new_tweets)
            last_id = new_tweets[-1].id
        except tweepy.TweepError as e:
        # depending on TweepError.code, one may want to retry or wait
        # to keep things simple, we will give up on an error
            break
            
    tweets = []
    for tweet in searched_tweets:
        if tweet.created_at < endDate and tweet.created_at > startDate:   
            # empty dictionary to store required params of a tweet 
            parsed_tweet = {}
            # saving text of tweet 
            parsed_tweet['text'] = clean_tweet(tweet.text)
            parsed_tweet['datetime'] = tweet.created_at
            tweets.append(parsed_tweet)
            
    return tweets


# ## Load Quandl stock data

# In[2]:


import pandas as pd
import quandl #quandl is not installed by default. You'll need to install it and get an account.
import datetime 
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('pylab', 'inline')
quandl.ApiConfig.api_key = "cHs3hSC-ys83Msb8qXyh"#This is Jorge's key, get yourself a new one.


# In[3]:


start_date = datetime.datetime(2015,1,1) # Beginning of period 
end_date = datetime.datetime(2015,2,1) # End of period 
stock = "TSLA" # some stock label we are interested in
tesla = quandl.get("WIKI/" + stock, start_date=start_date, end_date=end_date) #download data with quandl


# In[4]:


pylab.rcParams['figure.figsize'] = (15, 9)
plt.title(stock + " Closing Prices")
tesla["Close"].plot() # plot daily closing prices 
plt.show()


# In[ ]:


tesla["DailyPercentDiff"] = (tesla["Close"] - tesla["Open"]) / tesla["Open"]
plt.title(stock + " Daily Percent Differences")
tesla["DailyPercentDiff"].plot() # plot daily closing prices 
plt.show()


# ## Proof of Principle : Do Barack Obama's tweets effect TSLA closing prices?

# In[ ]:


start_date = datetime.datetime(2015,1,1) # Beginning of period 
end_date = datetime.datetime(2016,1,1) # End of period 
stock = "TSLA" # some stock label we are interested in
tesla = quandl.get("WIKI/" + stock, start_date=start_date, end_date=end_date) #download data with quandl


# In[12]:


baracks_tweets = get_tweets_user('BarackObama', 1000, start_date, end_date)


# In[13]:


baracks_tweets


# In[ ]:




