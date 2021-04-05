import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template, session, send_file
import tweepy
import io

app = Flask(__name__)
app.secret_key = 'akamsiA468'

consumer_key = "0GHBBLM1BImXSmUVI5hQP1bou"
consumer_secret = "a5OxetJT9q2jJFD5E8Jo0X8YGe88vgj0MaxLnJUc8tzA5jgtBp"
access_token = "61354924-E7l18ch4TOtARLGBAEJqRjg6SnM0mXOEAlEh4tEdX"
access_token_secret = "P5P096kCzSzX3Kab4uHxULVar4Jfpmi9oKHQjPOyKaEhq"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('home.html')

@app.route("/download", methods=["POST"])
def download():
    input = request.form
    text_query = input['tweet']
    count = int(input['tweet count'])
    # Creation of query method using parameters
    tweets = tweepy.Cursor(api.search,q=text_query).items(count)
        
    # Pulling information from tweets iterable object
    tweets_list = [[tweet.text] for tweet in tweets]
        
    # Creation of dataframe from tweets list
    tweets_df = pd.DataFrame(tweets_list, columns=['tweet'])
    
    #Clean the tweet
    tweets_df['tweet'] = tweets_df['tweet'].str.replace('RT', '')
    tweets_df['tweet'] = tweets_df['tweet'].str.replace('\@\w+\:', '', regex=True)
    tweets_df['tweet'] = tweets_df['tweet'].str.replace('\@\w+', '', regex=True)
    tweets_df['tweet'] = tweets_df['tweet'].str.replace('\d+\)', '', regex=True)
    tweets_df['tweet'] = tweets_df['tweet'].str.replace('\d+\.', '', regex=True)
    tweets_df['tweet'] = tweets_df['tweet'].str.replace('http\S+', '', regex=True)
    tweets_df['tweet'] = [i.lower() for i in tweets_df['tweet']]
    session["df"] = tweets_df.to_csv(index=False, header=True)

    # Get the CSV data as a string from the session
    csv = session["df"] if "df" in session else ""
    
    # Create a string buffer
    buf_str = io.StringIO(csv)

    # Create a bytes buffer from the string buffer
    buf_byt = io.BytesIO(buf_str.read().encode("utf-8"))
    
    # Return the CSV data as an attachment
    return send_file(buf_byt,
                     mimetype="text/csv",
                     as_attachment=True,
                     attachment_filename='{}.csv'.format(text_query))

if __name__ == "__main__":
    app.run(debug=True)