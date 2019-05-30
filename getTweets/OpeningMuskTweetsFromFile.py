#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import datetime
import matplotlib.pyplot as plt
import random
get_ipython().run_line_magic('matplotlib', 'inline')
#textblob to apply sentiment analysis 
from textblob import TextBlob
 


# In[2]:


#read the csv file containing musks tweets
tweets = pd.read_csv('../using_twint/musks_tweets.csv')
tweets.head()


# In[3]:


#specify the random seed for reproducibility
random.seed(0)

#get a particular tweet text
some_tweet = tweets.iloc[random.randint(1, 100)]['tweet']
print(some_tweet)
#get the 'sentiment' of a particular tweet 
analysis = TextBlob(some_tweet)
print(analysis.sentiment)


# In[4]:


test = tweets['tweet'][:5]
[TextBlob(x).sentiment for x in test[:5]]


# In[5]:


tweets['polarity'] = a= tweets['tweet'].apply(lambda x:TextBlob(x).polarity)
tweets['subjectivity'] = b= tweets['tweet'].apply(lambda x:TextBlob(x).subjectivity)
print(a[:5])
print(b[:5])


# In[6]:


tweets.head()


# In[7]:


# #store sentiments into dataframe
# #I DONT KNOW HOW TO GET THIS TO WORK?? 
# for index, row in tweets.iterrows():
#     text = tweets.iloc[index]['tweet']
#     analysis = TextBlob(text)
#     row['Polarity'] = analysis.sentiment[0]
#     row['Subjectivity'] = analysis.sentiment[1]


# In[ ]:




