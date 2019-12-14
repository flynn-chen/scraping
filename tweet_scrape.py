import tweepy
import csv
from argparse import ArgumentParser
import pandas as pd


def get_user_tweets(screen_name):

	#initialize a list to hold all the tweepy Tweets
	alltweets = []

	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)

	#save most recent tweets
	alltweets.extend(new_tweets)

	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1


	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print("getting tweets before %s" % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print("...%s tweets downloaded so far" % (len(alltweets)))

	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]

	#write the csv	
	with open('userTweets_%s.tsv' % screen_name, 'w') as f:
		writer = csv.writer(f, delimiter='\t')
		writer.writerow(["id","time_created","text"])
		writer.writerows(outtweets)

	pass

def search_terms(term):
	tweets = api.search(q=term,count=1000, since="2005-04-03")
 
	message,favorite_count,retweet_count,created_at,user_name,followers_count=[],[],[],[],[],[]
	for tweet in tweets:
	    message.append(tweet.text)
	    favorite_count.append(tweet.favorite_count)
	    retweet_count.append(tweet.retweet_count)
	    created_at.append(tweet.created_at)
	    user_name.append(tweet.user.name)
	    followers_count.append(tweet.user.followers_count)
	    
	df=pd.DataFrame({'Message':message,
	                'Favourite Count':favorite_count,
	                'Retweet Count':retweet_count,
	                'Created At':created_at,
	                'user_name':user_name,
	                'followers_count':followers_count})
	df.to_csv("search_%s.csv" % (term))
	print(df)

if __name__== "__main__":

	# Authenticate to Twitter
	auth = tweepy.OAuthHandler("", 
	    "")
	auth.set_access_token("", 
	    "")

	api = tweepy.API(auth)

	try:
	    api.verify_credentials()
	    print("Authentication OK")
	except:
	    print("Error during authentication")

	print("How would you like to do?")
	print("1. user")
	print("2. search")
	print("3. publish")

	action = input()
	if action == "user" or action == "1":
		print("please enter Twitter username:")
		name=input()
		get_user_tweets(name)

	if action == "search" or action == "2":
		print("please enter search term:")
		term=input()
		search_terms(term)

	if action == "publish" or action == "3":
		print("please enter content to be tweeted:")
		content=input()
		api.update_status(content)















