#!/usr/bin/python3

from flask import Flask, render_template, request
import pandas as pd
import tweepy as tw
import random


app = Flask(__name__)


# auth = tw.OAuthHandler()
# auth.set_access_token()

# # print(auth.get_authorization_url())

# api = tw.API(auth)

# tweets = api.home_timeline()
# for tweet in public_tweets:
# 	print(tweet.text)



@app.route("/")
def main():
	return render_template("map.html")

@app.route("/query/", methods = ["POST"])
def query():
	lng = float(request.form.get("lng", 0))
	lat = float(request.form.get("lat", 0))
	radius = float(request.form.get("radius", 100))
	
	df = getTweets(lat, lng, radius)

	return df.to_json(orient = "records")

dates = [pd.Timestamp('2018-03-21'), pd.Timestamp("2018-02-01"), pd.Timestamp("2018-01-20")]

def getTweets(lat, lon, radius):
	out = pd.DataFrame({"tweet": ["I love afghanistan", "I hate afghanistan"],
						"time": [random.choice(dates), random.choice(dates)], 
						"sent": [random.random() * 6 - 3, random.random() * 6 - 3],
						"lang": ["en", "fa"],
						"id":   [random.random(), random.random()]
						})

	return out

app.run()