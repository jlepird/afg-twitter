#!/usr/bin/python3

from flask import Flask, render_template, request
import pandas as pd
import tweepy as tw
import random
import json



app = Flask(__name__)

login = json.load(open("auth.json"))

auth = tw.OAuthHandler(login["app_key"], login["app_secret"])
auth.set_access_token(login["auth_key"], login["auth_secret"])

api = tw.API(auth)


tweets = api.home_timeline()
for tweet in tweets:
 	print(tweet.text)



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

if __name__ == "__main__":
	app.run()