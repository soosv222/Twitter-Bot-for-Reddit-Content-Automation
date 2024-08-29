import requests
from requests_oauthlib import OAuth1
import time
import praw
import tweepy
import json
import os
from dotenv import load_dotenv
import sys

# load environment variables
load_dotenv()

# twitter API keys
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)
auth = tweepy.OAuth1UserHandler(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)
api = tweepy.API(auth)

# reddit API keys
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
user_agent = os.getenv("USER_AGENT")

reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

# functions
def tweet(text = None, media = None): # sends an individual tweet
    if media == None:
        return client.create_tweet(text=text)
    else:
        if type(media) == list:
            media_ids = [api.media_upload(filename=m).media_id for m in media]
        else:
            media_ids = [api.media_upload(filename=media).media_id]
        return client.create_tweet(text=text, media_ids = media_ids)
def thread(tweets): # sends a thread of tweets
    root = tweet(text=tweets[0])
    last = root
    for i in range(1, len(tweets)):
        last = client.create_tweet(text=tweets[i], in_reply_to_tweet_id=last.data['id'])
    return root
def process(text): # processes reddit post into twitter thread format
    if len(text) > 280:
        paragraphs = [p + '\n\n' for p in text.split('\n\n')]
        blocks = []
        for para in paragraphs:
            if len(para) > 280:
                sentences = para.split('. ')
                sentences = [s + '.' for s in sentences[0:-1]] + [sentences[-1]]
                temp = []
                for sent in sentences:
                    if len(sent) > 280:
                        phrases = sent.split(', ')
                        phrases = [s + ',' for s in phrases[0:-1]] + [phrases[-1]]
                        temp2 = []
                        for phrase in phrases:
                            if len(phrase) > 280:
                                temp2 += [phrase.split('* ')[0]] + ['* ' + p for p in phrase.split('* ')[1:]]
                            else:
                                temp2.append(phrase)
                        temp += temp2
                    else:
                        temp.append(sent)
                blocks += temp
            else:
                blocks.append(para)
        temp = []
        for block in blocks:
            if len(block) > 280 and block.find('(https:') != -1:
                t = block[:block.find('(https:')] + block[block.find(')'):]
                if len(t) > 280:
                    temp += t.split(' ')
                else:
                    temp.append(t)
                    continue
            if len(block) > 280:
                temp += block.split(' ')
            else:
                temp.append(block)
        blocks = temp
        final = []
        curr = blocks[0]
        for i in range(1, len(blocks)):
            nxt = blocks[i]
            if nxt == '':
                continue
            if len(nxt) + len(curr) < 280:
                if len(curr) > 0 and (curr[-1] == '\n' or nxt == '\n\n'):
                    curr += nxt
                else:
                    curr += ' ' + nxt
            else:
                final.append(curr)
                curr = nxt
        final.append(curr)
        return final
    else:
        return [text]
# def printtwt(threadarr): # prints processed post in twitter-esque format (used for testing)
#     print(len(threadarr), "tweets long\n")
#     for twt in threadarr:
#         print(str(len(twt)) + ": " + twt + '\n')
        
# creating post
with open('posthist.json', 'r') as infile: # load post history
    posthist = json.load(infile)
# print('loaded posthist')
while len(posthist) > 0 and (time.time() - posthist[0]['time']) > 60*60*24*7: # wipe history past 1 week
    posthist.pop(0)
postedids = set([post['id'] for post in posthist])
tweet_allowance = 50
for post in posthist: # calculate how many tweets can be put out in accordance to the twitter API rate limits
    if time.time() - post['time'] < 24*60*60:
        tweet_allowance -= post['length']
for post in reddit.subreddit(sys.argv[1]).top(time_filter='week'):
    if post.id not in postedids: # search for a top post that hasn't been posted already
        proctext = process(post.title) + process(post.selftext + ' ' + post.url) # format post for twitter
        if len(proctext) <= tweet_allowance: # make sure thread length is within API limits
            print(thread(proctext)) # post the thread on twitter
            posthist.append({'id': post.id, 'time': time.time(), 'length': len(proctext)}) # add to post history
            with open('posthist.json', 'w') as outfile: # save post history
                json.dump(posthist, outfile)
        if len(proctext) <= 50: # do nothing and wait for 24 hour window for API rate limit to shift
            break
        # if post is longer than possible API limits, search for a different post