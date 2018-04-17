#!/usr/bin/python3
from flask import Flask, render_template, request, url_for
import pandas as pd
import tweepy as tw
import random
import json
import nltk
from googletrans import Translator
import re
tr = Translator()


# download vader data if not already done.
nltk.download("vader_lexicon")
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

iso = pd.read_csv("data/iso_codes.csv")[["Language name", "639-1"]]

application = Flask(__name__)


# Load auth file
login = json.load(open("auth.json"))

auth = tw.OAuthHandler(login["app_key"], login["app_secret"])
auth.set_access_token(login["auth_key"], login["auth_secret"])


api = tw.API(auth)


@application.route("/")
def main():
	return render_template("map.html")

@application.route("/query/", methods = ["POST"])
def query():
	lng    = float(request.form.get("lng", 0))
	lat    = float(request.form.get("lat", 0))
	radius = float(request.form.get("radius", 100))
	q      =       request.form.get("q", "*")
	n      =   int(request.form.get("n", 150))
	
	df = getTweets(lat, lng, radius, q, n)

	df = pd.merge(df, iso, left_on="lang", right_on="639-1")

	df["lang"] = df["Language name"]

	return df.to_json(orient = "records")

# Remove milliseconds from timestamp
# Use re to get rid of the milliseconds.
remove_ms = lambda x:re.sub("\+\d+\s","",x)

def getTweets(lat, lon, radius, q, n):

	geocode = ",".join([str(lat), str(lon), str(radius)+"km"])

	#tweets = api.search(q, geocode=geocode, count=n)

	tweets = [status for status in tw.Cursor(api.search, q=q, geocode=geocode).items(n)]

	out = pd.DataFrame()
	for tweet in tweets:
		try: 
			text_en = tr.translate(tweet.text).text
		except:
			text_en = ""

		created_at = remove_ms(str(tweet.created_at))

		out = out.append(pd.DataFrame({
				"tweet": [tweet.text],
				"tweet_en": [text_en],
				"time": [pd.to_datetime(created_at)], #, format="%a %b %d %H:%M:%S %Y")], 
				"sent": [sid.polarity_scores(text_en)["compound"]],
				"lang": [tweet.lang],
				"id":   [tweet.id]
			}), ignore_index=True)

	return out

if __name__ == "__main__":
	application.run(debug=True)

